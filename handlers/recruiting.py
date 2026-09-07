from __future__ import annotations

import asyncio
import logging

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ChatMemberAdministrator, ChatMemberOwner

from config import MIN_PLAYERS, MAX_PLAYERS
from locales import t
from database import db as database
from utils.game_state import GameSession, GamePhase, Player, game_manager
from utils.keyboards import recruit_keyboard
from utils.formatting import format_players_list
from utils.game_engine import GameEngine, safe_send

logger = logging.getLogger(__name__)
router = Router(name="recruiting")


async def is_group_chat(message: Message) -> bool:
    return message.chat.type in ("group", "supergroup")


async def is_chat_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))
    except Exception:
        return False


def _build_recruit_text(lang: str, session: GameSession) -> str:
    players_list = format_players_list(list(session.players.values()))
    return t(
        lang, "recruit_start",
        min=MIN_PLAYERS, max=MAX_PLAYERS,
        seconds=session.recruit_time,
        count=len(session.players), players=players_list,
    )


async def _refresh_recruit_message(bot: Bot, session: GameSession):
    if session.recruit_message_id is None:
        return
    text = _build_recruit_text(session.lang, session)
    allow_force = len(session.players) >= MIN_PLAYERS
    kb = recruit_keyboard(session.lang, session.chat_id, allow_force)
    try:
        await bot.edit_message_text(
            text, chat_id=session.chat_id, message_id=session.recruit_message_id,
            reply_markup=kb,
        )
    except Exception:
        pass


# ------------------------------------------------------------------
# /game - start recruiting
# ------------------------------------------------------------------

@router.message(Command("game"))
async def cmd_game(message: Message, bot: Bot):
    if not await is_group_chat(message):
        settings = await database.get_chat_settings(message.chat.id)
        await message.answer(t(settings["lang"], "only_in_group"))
        return

    settings = await database.get_chat_settings(message.chat.id)
    lang = settings["lang"]

    if game_manager.exists(message.chat.id):
        await message.answer(t(lang, "game_already_running"))
        return

    session = GameSession(
        chat_id=message.chat.id,
        chat_title=message.chat.title or "Bunker",
        lang=lang,
        recruit_time=settings["recruit_time"],
        discussion_time=settings["discussion_time"],
        voting_time=settings["voting_time"],
        phase=GamePhase.RECRUITING,
    )
    game_manager.create(session)

    text = _build_recruit_text(lang, session)
    kb = recruit_keyboard(lang, session.chat_id, allow_force_start=False)
    msg = await message.answer(text, reply_markup=kb)
    session.recruit_message_id = msg.message_id

    task = asyncio.create_task(_recruit_timeout_task(bot, session))
    session.active_task = task


async def _recruit_timeout_task(bot: Bot, session: GameSession):
    try:
        await asyncio.sleep(session.recruit_time)
    except asyncio.CancelledError:
        return

    if session.phase != GamePhase.RECRUITING:
        return

    if len(session.players) < MIN_PLAYERS:
        await safe_send(
            bot, session.chat_id,
            t(session.lang, "recruit_timeout_not_enough", min=MIN_PLAYERS),
        )
        game_manager.remove(session.chat_id)
        return

    await _launch_game(bot, session)


async def _launch_game(bot: Bot, session: GameSession):
    session.phase = GamePhase.DEALING
    await safe_send(
        bot, session.chat_id,
        t(session.lang, "recruit_success_starting", count=len(session.players)),
    )
    engine = GameEngine(bot, session)
    task = asyncio.create_task(engine.run())
    session.active_task = task


# ------------------------------------------------------------------
# Recruiting callbacks: join / leave / cancel / force start
# ------------------------------------------------------------------

@router.callback_query(F.data.startswith("recruit_join:"))
async def cb_recruit_join(call: CallbackQuery, bot: Bot):
    chat_id = int(call.data.split(":")[1])
    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.RECRUITING:
        await call.answer(t("ru", "no_active_game"), show_alert=True)
        return

    lang = session.lang
    user = call.from_user

    if session.get_player(user.id):
        await call.answer(t(lang, "already_joined"), show_alert=True)
        return

    if len(session.players) >= MAX_PLAYERS:
        await call.answer(t(lang, "already_max_players", max=MAX_PLAYERS), show_alert=True)
        return

    player = Player(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        lang=lang,
    )
    session.add_player(player)
    await database.ensure_user(user.id, user.username, user.full_name)

    await call.answer(t(lang, "player_joined", name=user.full_name))
    await _refresh_recruit_message(bot, session)


@router.callback_query(F.data.startswith("recruit_leave:"))
async def cb_recruit_leave(call: CallbackQuery, bot: Bot):
    chat_id = int(call.data.split(":")[1])
    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.RECRUITING:
        await call.answer(t("ru", "no_active_game"), show_alert=True)
        return

    lang = session.lang
    user = call.from_user

    if not session.get_player(user.id):
        await call.answer(t(lang, "not_in_recruit"), show_alert=True)
        return

    session.remove_player(user.id)
    await call.answer(t(lang, "player_left", name=user.full_name))
    await _refresh_recruit_message(bot, session)


@router.callback_query(F.data.startswith("recruit_cancel:"))
async def cb_recruit_cancel(call: CallbackQuery, bot: Bot):
    chat_id = int(call.data.split(":")[1])
    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.RECRUITING:
        await call.answer(t("ru", "no_active_game"), show_alert=True)
        return

    lang = session.lang
    user = call.from_user
    is_admin = await is_chat_admin(bot, chat_id, user.id)
    is_creator_like = session.get_player(user.id) is not None

    if not (is_admin or is_creator_like):
        await call.answer(t(lang, "not_admin"), show_alert=True)
        return

    if session.active_task:
        session.active_task.cancel()
    game_manager.remove(chat_id)
    await call.answer()

    if is_admin:
        await call.message.edit_text(t(lang, "recruit_cancelled_by", name=user.full_name))
    else:
        await call.message.edit_text(t(lang, "recruit_cancelled"))


@router.callback_query(F.data.startswith("recruit_forcestart:"))
async def cb_recruit_forcestart(call: CallbackQuery, bot: Bot):
    chat_id = int(call.data.split(":")[1])
    session = game_manager.get(chat_id)
    if session is None or session.phase != GamePhase.RECRUITING:
        await call.answer(t("ru", "no_active_game"), show_alert=True)
        return

    lang = session.lang
    user = call.from_user
    is_admin = await is_chat_admin(bot, chat_id, user.id)

    if not is_admin:
        await call.answer(t(lang, "not_admin"), show_alert=True)
        return

    if len(session.players) < MIN_PLAYERS:
        await call.answer(t(lang, "not_enough_players", min=MIN_PLAYERS), show_alert=True)
        return

    await call.answer()
    if session.active_task:
        session.active_task.cancel()

    await call.message.edit_text(
        _build_recruit_text(lang, session), reply_markup=None,
    )
    await safe_send(bot, chat_id, t(lang, "game_force_started", name=user.full_name))
    await _launch_game(bot, session)


# ------------------------------------------------------------------
# /start (force start), /stop, /leave
# ------------------------------------------------------------------

@router.message(Command("start"), F.chat.type.in_({"group", "supergroup"}))
async def cmd_start_group(message: Message, bot: Bot):
    session = game_manager.get(message.chat.id)
    settings = await database.get_chat_settings(message.chat.id)
    lang = settings["lang"] if session is None else session.lang

    if session is None:
        await message.answer(t(lang, "no_active_game"))
        return

    if session.phase != GamePhase.RECRUITING:
        await message.answer(t(lang, "game_in_progress_wait"))
        return

    is_admin = await is_chat_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer(t(lang, "not_admin"))
        return

    if len(session.players) < MIN_PLAYERS:
        await message.answer(t(lang, "not_enough_players", min=MIN_PLAYERS))
        return

    if session.active_task:
        session.active_task.cancel()

    try:
        await bot.edit_message_reply_markup(
            chat_id=session.chat_id, message_id=session.recruit_message_id, reply_markup=None,
        )
    except Exception:
        pass

    await message.answer(t(lang, "game_force_started", name=message.from_user.full_name))
    await _launch_game(bot, session)


@router.message(Command("stop"))
async def cmd_stop(message: Message, bot: Bot):
    if not await is_group_chat(message):
        settings = await database.get_chat_settings(message.chat.id)
        await message.answer(t(settings["lang"], "only_in_group"))
        return

    session = game_manager.get(message.chat.id)
    settings = await database.get_chat_settings(message.chat.id)
    lang = settings["lang"] if session is None else session.lang

    if session is None:
        await message.answer(t(lang, "no_active_game"))
        return

    is_admin = await is_chat_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer(t(lang, "not_admin"))
        return

    if session.active_task:
        session.active_task.cancel()
    session.phase = GamePhase.FINISHED
    game_manager.remove(message.chat.id)

    await message.answer(t(lang, "game_stopped", name=message.from_user.full_name))


@router.message(Command("leave"))
async def cmd_leave(message: Message, bot: Bot):
    if not await is_group_chat(message):
        settings = await database.get_chat_settings(message.chat.id)
        await message.answer(t(settings["lang"], "only_in_group"))
        return

    session = game_manager.get(message.chat.id)
    if session is None:
        settings = await database.get_chat_settings(message.chat.id)
        await message.answer(t(settings["lang"], "no_active_game"))
        return

    lang = session.lang
    player = session.get_player(message.from_user.id)

    if session.phase == GamePhase.RECRUITING:
        if not player:
            await message.answer(t(lang, "not_in_recruit"))
            return
        session.remove_player(message.from_user.id)
        await message.answer(t(lang, "player_left", name=message.from_user.full_name))
        await _refresh_recruit_message(bot, session)
        return

    # Mid-game leave: mark player eliminated instead of removing them outright,
    # so round logic (votes, reveal state) referencing them doesn't break.
    if session.phase == GamePhase.FINISHED:
        await message.answer(t(lang, "no_active_game"))
        return

    if not player or not player.alive:
        await message.answer(t(lang, "not_in_recruit"))
        return

    player.alive = False
    await message.answer(t(lang, "player_left_mid_game", name=player.full_name))

    if session.alive_count() < 2:
        if session.active_task:
            session.active_task.cancel()
        session.phase = GamePhase.FINISHED
        game_manager.remove(message.chat.id)
        await message.answer(t(lang, "not_enough_players_midgame"))
