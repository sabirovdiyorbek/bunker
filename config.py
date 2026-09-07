import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8803052135:AAEpGmYoblA0GXjaX0kprowMuh6Tp9CYd0w")

DB_PATH = os.environ.get("BUNKER_DB_PATH", "bunker.db")

MIN_PLAYERS = 4
MAX_PLAYERS = 8

DEFAULT_LANG = "ru"

# Default timings (seconds) - can be overridden per-chat via /settings
DEFAULT_RECRUIT_TIME = 60
DEFAULT_DISCUSSION_TIME = 60
DEFAULT_VOTING_TIME = 30
DEFAULT_REVEAL_TIME = 45  # time given to each player in DM to choose a trait to reveal

# Selectable options offered in /settings menus (seconds)
RECRUIT_TIME_OPTIONS = [30, 45, 60, 90, 120]
DISCUSSION_TIME_OPTIONS = [30, 45, 60, 90, 120, 180]
VOTING_TIME_OPTIONS = [15, 20, 30, 45, 60]

TRAIT_ORDER = ["profession", "bio", "health", "hobby", "phobia", "baggage", "fact"]
