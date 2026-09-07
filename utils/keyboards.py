from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from locales import t
from config import (
    RECRUIT_TIME_OPTIONS, DISCUSSION_TIME_OPTIONS, VOTING_TIME_OPTIONS,
    TRAIT_ORDER,
)
from locales import SUPPORTED_LANGS, LOCALES


def recruit_keyboard(lang: str, chat_id: int, allow_force_start: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "join_button"), callback_data=f"recruit_join:{chat_id}")
    b.button(text=t(lang, "leave_button"), callback_data=f"recruit_leave:{chat_id}")
    row_sizes = [2]
    if allow_force_start:
        b.button(text=t(lang, "force_start_button"), callback_data=f"recruit_forcestart:{chat_id}")
        row_sizes.append(1)
    b.button(text=t(lang, "cancel_recruit_button"), callback_data=f"recruit_cancel:{chat_id}")
    row_sizes.append(1)
    b.adjust(*row_sizes)
    return b.as_markup()


def reveal_trait_keyboard(lang: str, chat_id: int, unrevealed: list[str]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for trait in TRAIT_ORDER:
        if trait in unrevealed:
            b.button(
                text=t(lang, f"trait_{trait}"),
                callback_data=f"reveal:{chat_id}:{trait}",
            )
    b.adjust(2)
    return b.as_markup()


def voting_keyboard(lang: str, chat_id: int, candidates: list, vote_counts: dict[int, int] | None = None) -> InlineKeyboardMarkup:
    """candidates: list of Player objects (alive players eligible to be voted for)."""
    b = InlineKeyboardBuilder()
    vote_counts = vote_counts or {}
    for p in candidates:
        count = vote_counts.get(p.user_id, 0)
        label = p.full_name
        if count:
            label = f"{label} ({count})"
        b.button(text=label, callback_data=f"vote:{chat_id}:{p.user_id}")
    b.adjust(1)
    return b.as_markup()


def settings_main_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_change_lang"), callback_data="settings:lang")
    b.button(text=t(lang, "btn_change_recruit_time"), callback_data="settings:recruit_time")
    b.button(text=t(lang, "btn_change_discussion_time"), callback_data="settings:discussion_time")
    b.button(text=t(lang, "btn_change_voting_time"), callback_data="settings:voting_time")
    b.button(text=t(lang, "btn_close"), callback_data="settings:close")
    b.adjust(1)
    return b.as_markup()


def settings_lang_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for code in SUPPORTED_LANGS:
        name = LOCALES[code]["lang_name"]
        b.button(text=name, callback_data=f"settings:setlang:{code}")
    b.button(text=t(lang, "back"), callback_data="settings:back")
    b.adjust(1)
    return b.as_markup()


def settings_time_keyboard(lang: str, field: str) -> InlineKeyboardMarkup:
    options_map = {
        "recruit_time": RECRUIT_TIME_OPTIONS,
        "discussion_time": DISCUSSION_TIME_OPTIONS,
        "voting_time": VOTING_TIME_OPTIONS,
    }
    options = options_map[field]
    b = InlineKeyboardBuilder()
    for seconds in options:
        b.button(text=f"{seconds} сек / sek / sec", callback_data=f"settings:settime:{field}:{seconds}")
    b.button(text=t(lang, "back"), callback_data="settings:back")
    b.adjust(3)
    return b.as_markup()
