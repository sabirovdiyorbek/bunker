from locales import t
from config import TRAIT_ORDER
from utils.game_state import Player

TRAIT_TO_CARD_KEY = {
    "profession": "card_profession",
    "bio": "card_bio",
    "health": "card_health",
    "hobby": "card_hobby",
    "phobia": "card_phobia",
    "baggage": "card_baggage",
    "fact": "card_fact",
}


def format_full_card(lang: str, player: Player) -> str:
    """Full character card text (all traits), used in DM and for winners at the end."""
    lines = []
    for trait in TRAIT_ORDER:
        key = TRAIT_TO_CARD_KEY[trait]
        value = player.character.get(trait, "-")
        lines.append(t(lang, key, value=value))
    return "\n".join(lines)


def format_revealed_card(lang: str, player: Player) -> str:
    """Only the traits the player has revealed so far."""
    lines = []
    for trait in TRAIT_ORDER:
        if player.revealed.get(trait):
            key = TRAIT_TO_CARD_KEY[trait]
            value = player.character.get(trait, "-")
            lines.append(t(lang, key, value=value))
    if not lines:
        return "-"
    return "\n".join(lines)


def format_unrevealed_card(lang: str, player: Player) -> str:
    """Traits the player never revealed (shown when eliminated / at game end)."""
    lines = []
    for trait in TRAIT_ORDER:
        if not player.revealed.get(trait):
            key = TRAIT_TO_CARD_KEY[trait]
            value = player.character.get(trait, "-")
            lines.append(t(lang, key, value=value))
    if not lines:
        return "-"
    return "\n".join(lines)


def format_players_list(players, joined_symbol="•") -> str:
    if not players:
        return "-"
    return "\n".join(f"{joined_symbol} {p.full_name}" for p in players)
