import os
import aiosqlite
from contextlib import asynccontextmanager

from config import (
    DB_PATH, DEFAULT_LANG, DEFAULT_RECRUIT_TIME,
    DEFAULT_DISCUSSION_TIME, DEFAULT_VOTING_TIME,
)

_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
        await db.executescript(schema)
        await db.commit()


@asynccontextmanager
async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


# ------------------------------------------------------------------
# Chat settings
# ------------------------------------------------------------------

async def get_chat_settings(chat_id: int) -> dict:
    async with get_db() as db:
        cur = await db.execute(
            "SELECT * FROM chat_settings WHERE chat_id = ?", (chat_id,)
        )
        row = await cur.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO chat_settings (chat_id, lang, recruit_time, discussion_time, voting_time) "
                "VALUES (?, ?, ?, ?, ?)",
                (chat_id, DEFAULT_LANG, DEFAULT_RECRUIT_TIME, DEFAULT_DISCUSSION_TIME, DEFAULT_VOTING_TIME),
            )
            await db.commit()
            return {
                "chat_id": chat_id,
                "lang": DEFAULT_LANG,
                "recruit_time": DEFAULT_RECRUIT_TIME,
                "discussion_time": DEFAULT_DISCUSSION_TIME,
                "voting_time": DEFAULT_VOTING_TIME,
            }
        return dict(row)


async def set_chat_setting(chat_id: int, field: str, value) -> None:
    assert field in ("lang", "recruit_time", "discussion_time", "voting_time")
    await get_chat_settings(chat_id)  # ensure row exists
    async with get_db() as db:
        await db.execute(
            f"UPDATE chat_settings SET {field} = ? WHERE chat_id = ?", (value, chat_id)
        )
        await db.commit()


# ------------------------------------------------------------------
# User stats
# ------------------------------------------------------------------

async def ensure_user(user_id: int, username: str | None, full_name: str) -> None:
    async with get_db() as db:
        await db.execute(
            "INSERT INTO user_stats (user_id, username, full_name, games_played, games_won) "
            "VALUES (?, ?, ?, 0, 0) "
            "ON CONFLICT(user_id) DO UPDATE SET username=excluded.username, full_name=excluded.full_name",
            (user_id, username, full_name),
        )
        await db.commit()


async def get_user_stats(user_id: int) -> dict | None:
    async with get_db() as db:
        cur = await db.execute("SELECT * FROM user_stats WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def record_game_result(user_id: int, username: str | None, full_name: str, won: bool) -> None:
    await ensure_user(user_id, username, full_name)
    async with get_db() as db:
        if won:
            await db.execute(
                "UPDATE user_stats SET games_played = games_played + 1, games_won = games_won + 1 "
                "WHERE user_id = ?", (user_id,),
            )
        else:
            await db.execute(
                "UPDATE user_stats SET games_played = games_played + 1 WHERE user_id = ?", (user_id,),
            )
        await db.commit()


# ------------------------------------------------------------------
# Game history (optional, informational)
# ------------------------------------------------------------------

async def create_game_record(chat_id: int) -> int:
    async with get_db() as db:
        cur = await db.execute("INSERT INTO games (chat_id) VALUES (?)", (chat_id,))
        await db.commit()
        return cur.lastrowid


async def finish_game_record(game_id: int, winners: str) -> None:
    async with get_db() as db:
        await db.execute(
            "UPDATE games SET finished_at = datetime('now'), winners = ? WHERE game_id = ?",
            (winners, game_id),
        )
        await db.commit()
