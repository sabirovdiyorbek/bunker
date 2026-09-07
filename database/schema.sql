-- Per-chat settings
CREATE TABLE IF NOT EXISTS chat_settings (
    chat_id             INTEGER PRIMARY KEY,
    lang                TEXT NOT NULL DEFAULT 'ru',
    recruit_time        INTEGER NOT NULL DEFAULT 60,
    discussion_time     INTEGER NOT NULL DEFAULT 60,
    voting_time         INTEGER NOT NULL DEFAULT 30
);

-- Global user stats (across all chats)
CREATE TABLE IF NOT EXISTS user_stats (
    user_id             INTEGER PRIMARY KEY,
    username            TEXT,
    full_name           TEXT,
    games_played        INTEGER NOT NULL DEFAULT 0,
    games_won           INTEGER NOT NULL DEFAULT 0
);

-- One row per game (for history / debugging, not strictly required by gameplay)
CREATE TABLE IF NOT EXISTS games (
    game_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id             INTEGER NOT NULL,
    started_at          TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at         TEXT,
    winners             TEXT
);
