from __future__ import annotations

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ChatMemberAdministrator, ChatMemberOwner

from locales import t, LOCALES
from database import db as database
from utils.keyboards import settings_main_keyboard, settings_lang_keyboard, settings_time_keyboard

router = Router(name="settings")


async def is_chat_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))
    except Exception:
        return False


def _settings_overview_text(lang: str, settings: dict) -> str:
    lang_name = LOCALES[settings["lang"]]["lang_name"]
    lines = [
        t(lang, "settings_title"),
        "",
        t(lang, "settings_lang", lang=lang_name),
        t(lang, "settings_recruit_time", seconds=settings["recruit_time"]),
        t(lang, "settings_discussion_time", seconds=settings["discussion_time"]),
        t(lang, "settings_voting_time", seconds=settings["voting_time"]),
        "",
        t(lang, "settings_choose_option"),
    ]
    return "\n".join(lines)


@router.message(Command("settings"))
async def cmd_settings(message: Message, bot: Bot):
    if message.chat.type not in ("group", "supergroup"):
        settings = await database.get_chat_settings(message.chat.id)
        await message.answer(t(settings["lang"], "only_in_group"))
        return

    settings = await database.get_chat_settings(message.chat.id)
    lang = settings["lang"]

    is_admin = await is_chat_admin(bot, message.chat.id, message.from_user.id)
    if not is_admin:
        await message.answer(t(lang, "settings_only_admin"))
        return

    text = _settings_overview_text(lang, settings)
    kb = settings_main_keyboard(lang)
    await message.answer(text, reply_markup=kb)


async def _guard_admin(call: CallbackQuery, bot: Bot, lang: str) -> bool:
    is_admin = await is_chat_admin(bot, call.message.chat.id, call.from_user.id)
    if not is_admin:
        await call.answer(t(lang, "settings_only_admin"), show_alert=True)
        return False
    return True


@router.callback_query(F.data == "settings:lang")
async def cb_settings_lang_menu(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    await call.answer()
    await call.message.edit_text(t(lang, "settings_choose_lang"), reply_markup=settings_lang_keyboard(lang))


@router.callback_query(F.data.startswith("settings:setlang:"))
async def cb_settings_set_lang(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    new_lang = call.data.split(":")[2]
    await database.set_chat_setting(call.message.chat.id, "lang", new_lang)
    settings = await database.get_chat_settings(call.message.chat.id)
    await call.answer(t(new_lang, "settings_updated"))
    await call.message.edit_text(
        _settings_overview_text(new_lang, settings), reply_markup=settings_main_keyboard(new_lang)
    )


@router.callback_query(F.data.in_({"settings:recruit_time", "settings:discussion_time", "settings:voting_time"}))
async def cb_settings_time_menu(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    field = call.data.split(":")[1]
    await call.answer()
    await call.message.edit_text(
        t(lang, "settings_choose_time"), reply_markup=settings_time_keyboard(lang, field)
    )


@router.callback_query(F.data.startswith("settings:settime:"))
async def cb_settings_set_time(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    _, _, field, seconds_str = call.data.split(":")
    seconds = int(seconds_str)
    await database.set_chat_setting(call.message.chat.id, field, seconds)
    settings = await database.get_chat_settings(call.message.chat.id)
    await call.answer(t(lang, "settings_updated"))
    await call.message.edit_text(
        _settings_overview_text(lang, settings), reply_markup=settings_main_keyboard(lang)
    )


@router.callback_query(F.data == "settings:back")
async def cb_settings_back(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    await call.answer()
    await call.message.edit_text(
        _settings_overview_text(lang, settings), reply_markup=settings_main_keyboard(lang)
    )


@router.callback_query(F.data == "settings:close")
async def cb_settings_close(call: CallbackQuery, bot: Bot):
    settings = await database.get_chat_settings(call.message.chat.id)
    lang = settings["lang"]
    if not await _guard_admin(call, bot, lang):
        return
    await call.answer()
    try:
        await call.message.delete()
    except Exception:
        pass
