from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery

from locales import t
from utils.game_state import GamePhase, game_manager
from utils.keyboards import voting_keyboard

router = Router(name="gameplay")


# ------------------------------------------------------------------
# Trait reveal choice (sent via DM)
# ------------------------------------------------------------------

@router.callback_query(F.data.startswith("reveal:"))
async def cb_reveal_choice(call: CallbackQuery):
    _, chat_id_str, trait = call.data.split(":")
    chat_id = int(chat_id_str)

    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.ROUND_REVEAL:
        await call.answer()
        return

    player = session.get_player(call.from_user.id)
    if player is None or not player.alive:
        await call.answer(t(session.lang, "vote_not_alive"), show_alert=True)
        return

    if player.revealed.get(trait):
        await call.answer(t(player.lang, "reveal_already_open"), show_alert=True)
        return

    session.reveal_choices[player.user_id] = trait
    player.chosen_trait_this_round = trait

    trait_label = t(player.lang, f"trait_{trait}")
    await call.answer(t(player.lang, "reveal_choice_saved", trait=trait_label), show_alert=False)
    try:
        await call.message.edit_text(
            t(player.lang, "reveal_choice_saved", trait=trait_label),
        )
    except Exception:
        pass


# ------------------------------------------------------------------
# Voting (sent in the group chat, open voting with live counters)
# ------------------------------------------------------------------

@router.callback_query(F.data.startswith("vote:"))
async def cb_vote(call: CallbackQuery):
    _, chat_id_str, target_id_str = call.data.split(":")
    chat_id = int(chat_id_str)
    target_id = int(target_id_str)

    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.VOTING:
        await call.answer()
        return

    lang = session.lang
    voter = session.get_player(call.from_user.id)
    if voter is None or not voter.alive:
        await call.answer(t(lang, "vote_not_alive"), show_alert=True)
        return

    target = session.get_player(target_id)
    if target is None or not target.alive:
        await call.answer(t(lang, "vote_target_not_alive"), show_alert=True)
        return

    if voter.user_id == target_id:
        await call.answer(t(lang, "vote_cannot_self"), show_alert=True)
        return

    previous_vote = session.votes.get(voter.user_id)
    session.votes[voter.user_id] = target_id

    await call.answer()

    if previous_vote is not None and previous_vote != target_id:
        await call.message.answer(
            t(lang, "vote_changed", voter=voter.full_name, target=target.full_name)
        )
    else:
        await call.message.answer(
            t(lang, "vote_registered", voter=voter.full_name, target=target.full_name)
        )

    # refresh keyboard with live vote counts
    tally: dict[int, int] = {}
    for tid in session.votes.values():
        tally[tid] = tally.get(tid, 0) + 1

    candidates = session.alive_players()
    kb = voting_keyboard(lang, chat_id, candidates, tally)
    try:
        await call.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        pass
