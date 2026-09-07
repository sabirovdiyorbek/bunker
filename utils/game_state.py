"""
In-memory game state for the Bunker game.

Each chat has at most one active GameSession, kept in a global registry
(GameManager). Games are not persisted across bot restarts (only stats and
settings live in SQLite).
"""
from __future__ import annotations

import enum
import time
from dataclasses import dataclass, field

from config import TRAIT_ORDER


class GamePhase(str, enum.Enum):
    RECRUITING = "recruiting"
    DEALING = "dealing"
    ROUND_REVEAL = "round_reveal"
    DISCUSSION = "discussion"
    VOTING = "voting"
    FINISHED = "finished"


@dataclass
class Player:
    user_id: int
    username: str | None
    full_name: str
    lang: str = "ru"
    alive: bool = True
    has_dm: bool = True
    character: dict = field(default_factory=dict)  # trait_key -> value
    revealed: dict = field(default_factory=dict)    # trait_key -> True if revealed
    chosen_trait_this_round: str | None = None      # trait key player picked to reveal, this round

    def display_name(self) -> str:
        if self.username:
            return f"{self.full_name} (@{self.username})"
        return self.full_name

    def unrevealed_traits(self) -> list[str]:
        return [t for t in TRAIT_ORDER if not self.revealed.get(t)]


@dataclass
class GameSession:
    chat_id: int
    chat_title: str
    lang: str
    recruit_time: int
    discussion_time: int
    voting_time: int

    phase: GamePhase = GamePhase.RECRUITING
    players: dict[int, Player] = field(default_factory=dict)  # user_id -> Player
    round_number: int = 0
    catastrophe_text: str = ""
    bunker_info_text: str = ""

    # per-round transient state
    votes: dict[int, int] = field(default_factory=dict)          # voter_id -> target_id
    reveal_choices: dict[int, str] = field(default_factory=dict)  # user_id -> trait_key chosen this round

    recruit_message_id: int | None = None
    created_at: float = field(default_factory=time.time)

    # asyncio task handles, so they can be cancelled on /stop
    active_task: object = None

    def alive_players(self) -> list[Player]:
        return [p for p in self.players.values() if p.alive]

    def alive_count(self) -> int:
        return len(self.alive_players())

    def get_player(self, user_id: int) -> Player | None:
        return self.players.get(user_id)

    def add_player(self, player: Player) -> bool:
        if player.user_id in self.players:
            return False
        self.players[player.user_id] = player
        return True

    def remove_player(self, user_id: int) -> bool:
        if user_id in self.players:
            del self.players[user_id]
            return True
        return False


class GameManager:
    """Registry of active game sessions, keyed by chat_id."""

    def __init__(self):
        self._sessions: dict[int, GameSession] = {}

    def get(self, chat_id: int) -> GameSession | None:
        return self._sessions.get(chat_id)

    def create(self, session: GameSession) -> None:
        self._sessions[session.chat_id] = session

    def remove(self, chat_id: int) -> None:
        self._sessions.pop(chat_id, None)

    def exists(self, chat_id: int) -> bool:
        return chat_id in self._sessions


game_manager = GameManager()
