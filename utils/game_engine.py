"""
Core game engine: orchestrates recruiting -> dealing -> rounds (reveal, discussion,
voting) -> game over. Designed to run as a single asyncio task per chat.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from config import MIN_PLAYERS, DEFAULT_REVEAL_TIME
from locales import t
from database import db as database
from utils.game_state import GameSession, GamePhase, game_manager
from utils.keyboards import reveal_trait_keyboard, voting_keyboard
from utils.formatting import format_full_card, format_unrevealed_card
from utils import game_content

logger = logging.getLogger(__name__)


async def safe_send(bot: Bot, chat_id: int, text: str, **kwargs):
    try:
        return await bot.send_message(chat_id, text, **kwargs)
    except (TelegramForbiddenError, TelegramBadRequest) as e:
        logger.warning("Failed to send message to %s: %s", chat_id, e)
        return None


async def safe_send_dm(bot: Bot, user_id: int, text: str, **kwargs) -> bool:
    try:
        await bot.send_message(user_id, text, **kwargs)
        return True
    except (TelegramForbiddenError, TelegramBadRequest):
        return False


class GameEngine:
    def __init__(self, bot: Bot, session: GameSession):
        self.bot = bot
        self.session = session

    @property
    def lang(self):
        return self.session.lang

    async def run(self):
        """Main game flow, called after recruiting has finished with enough players."""
        session = self.session
        try:
            await self._check_dm_access()
            if session.phase == GamePhase.FINISHED:
                return  # cancelled during DM check due to insufficient players

            await self._deal_cards()
            await self._announce_catastrophe()

            round_num = 0
            while session.alive_count() > 2:
                round_num += 1
                session.round_number = round_num
                await self._run_round(round_num)
                if session.phase == GamePhase.FINISHED:
                    return  # stopped mid-round

            await self._announce_game_over()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Unhandled error in game engine for chat %s", session.chat_id)
            await safe_send(self.bot, session.chat_id, t(self.lang, "unknown_error"))
        finally:
            game_manager.remove(session.chat_id)

    # ------------------------------------------------------------------
    # Setup phase
    # ------------------------------------------------------------------

    async def _check_dm_access(self):
        """Verify every player can receive DMs; kick those who can't."""
        session = self.session
        kicked = []
        for player in list(session.players.values()):
            ok = await safe_send_dm(
                self.bot, player.user_id,
                t(player.lang, "start_private"),
            )
            player.has_dm = ok
            if not ok:
                kicked.append(player)

        for player in kicked:
            session.remove_player(player.user_id)

        if kicked:
            names = "\n".join(f"• {p.full_name}" for p in kicked)
            await safe_send(self.bot, session.chat_id, t(self.lang, "no_dm_kicked", names=names))

        if len(session.players) < MIN_PLAYERS:
            await safe_send(
                self.bot, session.chat_id,
                t(self.lang, "not_enough_after_dm_check", count=len(session.players), min=MIN_PLAYERS),
            )
            session.phase = GamePhase.FINISHED
            game_manager.remove(session.chat_id)

    async def _deal_cards(self):
        session = self.session
        session.phase = GamePhase.DEALING

        capacity = session.alive_count() - 2 if session.alive_count() > 2 else 1
        session.catastrophe_text = game_content.random_catastrophe(session.lang)
        session.bunker_info_text = game_content.random_bunker_info(session.lang, capacity)

        for player in session.players.values():
            player.character = game_content.generate_character(player.lang)
            card_text = format_full_card(player.lang, player)
            full_text = t(
                player.lang, "card_dm_intro",
                chat_title=session.chat_title, card=card_text,
            )
            await safe_send_dm(self.bot, player.user_id, full_text)

        await safe_send(self.bot, session.chat_id, t(self.lang, "cards_sent"))

    async def _announce_catastrophe(self):
        session = self.session
        text = (
            f"{t(self.lang, 'catastrophe_title')}\n\n{session.catastrophe_text}\n\n"
            f"{t(self.lang, 'bunker_info_title')}\n{session.bunker_info_text}"
        )
        await safe_send(self.bot, session.chat_id, text)
        await safe_send(
            self.bot, session.chat_id,
            t(self.lang, "game_starting", count=session.alive_count()),
        )
        await asyncio.sleep(2)

    # ------------------------------------------------------------------
    # Round flow
    # ------------------------------------------------------------------

    async def _run_round(self, round_num: int):
        session = self.session
        session.phase = GamePhase.ROUND_REVEAL
        session.votes.clear()
        session.reveal_choices.clear()
        for p in session.players.values():
            p.chosen_trait_this_round = None

        await safe_send(
            self.bot, session.chat_id,
            t(self.lang, "round_announce", round=round_num, alive=session.alive_count()),
        )

        if round_num == 1:
            await self._forced_profession_reveal()
        else:
            await self._free_reveal_phase(round_num)

        if session.phase == GamePhase.FINISHED:
            return

        await self._discussion_phase()
        if session.phase == GamePhase.FINISHED:
            return

        await self._voting_phase(round_num)

    async def _forced_profession_reveal(self):
        session = self.session
        await safe_send(self.bot, session.chat_id, t(self.lang, "round1_forced"))
        await asyncio.sleep(1.5)

        lines = [t(self.lang, "reveal_results_title", round=1)]
        for player in session.alive_players():
            player.revealed["profession"] = True
            value = player.character["profession"]
            lines.append(
                t(self.lang, "reveal_player_line", name=player.full_name,
                  trait_name=t(self.lang, "trait_profession"), value=value)
            )
        await safe_send(self.bot, session.chat_id, "\n".join(lines))

    async def _free_reveal_phase(self, round_num: int):
        session = self.session
        alive = session.alive_players()

        # Send DM prompts to everyone who still has unrevealed traits.
        prompts_sent = []
        for player in alive:
            unrevealed = player.unrevealed_traits()
            if not unrevealed:
                continue
            kb = reveal_trait_keyboard(player.lang, session.chat_id, unrevealed)
            text = t(
                player.lang, "reveal_prompt_dm",
                round=round_num, chat_title=session.chat_title,
                seconds=DEFAULT_REVEAL_TIME,
            )
            ok = await safe_send_dm(self.bot, player.user_id, text, reply_markup=kb)
            if ok:
                prompts_sent.append(player)

        await safe_send(
            self.bot, session.chat_id,
            t(self.lang, "reveal_time_left", seconds=DEFAULT_REVEAL_TIME),
        )

        await asyncio.sleep(DEFAULT_REVEAL_TIME)

        # Apply choices (or lack thereof)
        lines = [t(self.lang, "reveal_results_title", round=round_num)]
        for player in alive:
            if not player.alive:
                continue
            trait = session.reveal_choices.get(player.user_id)
            if trait and not player.revealed.get(trait):
                player.revealed[trait] = True
                value = player.character[trait]
                lines.append(
                    t(self.lang, "reveal_player_line", name=player.full_name,
                      trait_name=t(self.lang, f"trait_{trait}"), value=value)
                )
            else:
                if player.unrevealed_traits() or trait:
                    lines.append(t(self.lang, "reveal_none_chose", name=player.full_name))
        await safe_send(self.bot, session.chat_id, "\n".join(lines))

    async def _discussion_phase(self):
        session = self.session
        session.phase = GamePhase.DISCUSSION
        await safe_send(
            self.bot, session.chat_id,
            t(self.lang, "discussion_start", seconds=session.discussion_time),
        )
        remaining = session.discussion_time
        # Send a mid-point reminder if the discussion is long enough
        if remaining > 30:
            await asyncio.sleep(remaining - 15)
            if session.phase == GamePhase.FINISHED:
                return
            await safe_send(self.bot, session.chat_id, t(self.lang, "discussion_time_left", seconds=15))
            await asyncio.sleep(15)
        else:
            await asyncio.sleep(remaining)

    async def _voting_phase(self, round_num: int):
        session = self.session
        session.phase = GamePhase.VOTING
        session.votes.clear()

        candidates = session.alive_players()
        kb = voting_keyboard(self.lang, session.chat_id, candidates)
        msg = await safe_send(
            self.bot, session.chat_id,
            t(self.lang, "voting_start", round=round_num, seconds=session.voting_time),
            reply_markup=kb,
        )
        self.session.recruit_message_id = msg.message_id if msg else None

        remaining = session.voting_time
        if remaining > 20:
            await asyncio.sleep(remaining - 10)
            if session.phase == GamePhase.FINISHED:
                return
            await safe_send(self.bot, session.chat_id, t(self.lang, "voting_time_left", seconds=10))
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(remaining)

        if session.phase == GamePhase.FINISHED:
            return

        await self._resolve_voting(round_num, msg)

    async def _resolve_voting(self, round_num: int, vote_message):
        session = self.session
        tally: dict[int, int] = {}
        for target_id in session.votes.values():
            tally[target_id] = tally.get(target_id, 0) + 1

        lines = [t(self.lang, "voting_results_title", round=round_num)]
        if not tally:
            lines.append(t(self.lang, "voting_no_votes"))
            await safe_send(self.bot, session.chat_id, "\n".join(lines))
        else:
            for uid, count in sorted(tally.items(), key=lambda x: -x[1]):
                p = session.get_player(uid)
                name = p.full_name if p else str(uid)
                lines.append(t(self.lang, "voting_results_line", name=name, votes=count))
            await safe_send(self.bot, session.chat_id, "\n".join(lines))

            max_votes = max(tally.values())
            top = [uid for uid, c in tally.items() if c == max_votes]

            if len(top) > 1:
                names = ", ".join(
                    session.get_player(uid).full_name for uid in top if session.get_player(uid)
                )
                await safe_send(self.bot, session.chat_id, t(self.lang, "voting_tie", names=names))
            else:
                eliminated_id = top[0]
                player = session.get_player(eliminated_id)
                if player:
                    player.alive = False
                    await safe_send(
                        self.bot, session.chat_id,
                        t(self.lang, "voting_eliminated", name=player.full_name),
                    )
                    unrevealed_text = format_unrevealed_card(self.lang, player)
                    await safe_send(
                        self.bot, session.chat_id,
                        t(self.lang, "eliminated_reveal", name=player.full_name, traits=unrevealed_text),
                    )

        # try to remove the inline keyboard from the vote message
        if vote_message:
            try:
                await vote_message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Game over
    # ------------------------------------------------------------------

    async def _announce_game_over(self):
        session = self.session
        winners = session.alive_players()

        await safe_send(self.bot, session.chat_id, t(self.lang, "game_over_title"))
        await safe_send(self.bot, session.chat_id, t(self.lang, "game_over_winners"))

        for w in winners:
            card = format_full_card(self.lang, w)
            await safe_send(
                self.bot, session.chat_id,
                t(self.lang, "winner_card", name=w.full_name, card=card),
            )

        winner_ids = {w.user_id for w in winners}
        for player in session.players.values():
            await database.record_game_result(
                player.user_id, player.username, player.full_name,
                won=player.user_id in winner_ids,
            )

        await safe_send(self.bot, session.chat_id, t(self.lang, "game_over_stats_updated"))
        session.phase = GamePhase.FINISHED
