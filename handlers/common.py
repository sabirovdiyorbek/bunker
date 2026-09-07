from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import MIN_PLAYERS
from locales import t
from database import db as database

router = Router(name="common")


@router.message(Command("start"), F.chat.type == "private")
async def cmd_start_private(message: Message):
    # In private chat, /start just greets the user (used mainly for DM access checks).
    await message.answer(t("ru", "start_private") + "\n\n" + t("en", "start_private") + "\n\n" + t("uz", "start_private"))


@router.message(Command("help"))
async def cmd_help(message: Message):
    if message.chat.type in ("group", "supergroup"):
        settings = await database.get_chat_settings(message.chat.id)
        lang = settings["lang"]
    else:
        lang = "ru"
    await message.answer(t(lang, "help_text", min=MIN_PLAYERS))


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    if message.chat.type in ("group", "supergroup"):
        settings = await database.get_chat_settings(message.chat.id)
        lang = settings["lang"]
    else:
        lang = "ru"

    user = message.from_user
    stats = await database.get_user_stats(user.id)

    if not stats or stats["games_played"] == 0:
        await message.answer(t(lang, "profile_no_games"))
        return

    games = stats["games_played"]
    wins = stats["games_won"]
    winrate = round((wins / games) * 100, 1) if games else 0

    lines = [
        t(lang, "profile_title", name=user.full_name),
        t(lang, "profile_games", games=games),
        t(lang, "profile_wins", wins=wins),
        t(lang, "profile_winrate", winrate=winrate),
    ]
    await message.answer("\n".join(lines))
