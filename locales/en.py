TEXTS = {
    "lang_name": "English",

    # --- Common ---
    "only_in_group": "❗ This command only works in group chats.",
    "not_enough_players": "❗ Not enough players. Minimum is {min}.",
    "already_max_players": "❗ Maximum number of players ({max}) reached.",
    "no_active_game": "❗ There is no active game in this chat right now.",
    "game_already_running": "❗ A game or player recruitment is already running in this chat.",
    "not_admin": "❗ This command is only available to chat admins.",
    "unknown_error": "⚠️ An error occurred. Please try again.",
    "back": "⬅️ Back",
    "cancel": "❌ Cancel",

    # --- Recruiting ---
    "recruit_start": (
        "🎮 <b>Player recruitment for «Bunker» has started!</b>\n\n"
        "Tap the button below to join.\n"
        "Minimum players: {min}, maximum: {max}.\n"
        "Recruitment ends in {seconds} sec. or via /start from an admin.\n\n"
        "👥 Players ({count}/{max}):\n{players}"
    ),
    "join_button": "✅ Join",
    "leave_button": "🚪 Leave",
    "force_start_button": "▶️ Start now",
    "cancel_recruit_button": "❌ Cancel recruitment",
    "player_joined": "✅ {name} joined the game!",
    "player_left": "🚪 {name} left the recruitment.",
    "already_joined": "❗ You already joined the game.",
    "not_in_recruit": "❗ You are not part of the recruitment.",
    "recruit_full": "❗ Recruitment is full.",
    "need_private_chat": (
        "⚠️ {name}, to play you need to open a private chat with the bot "
        "(press /start in a DM with @{bot_username}), otherwise you won't be able to receive your "
        "character card and will be removed from the game."
    ),
    "recruit_cancelled": "❌ Player recruitment cancelled.",
    "recruit_cancelled_by": "❌ Player recruitment cancelled by admin {name}.",
    "recruit_timeout_not_enough": (
        "⏱ Recruitment time is up. Not enough players to start the game (need at least {min})."
    ),
    "recruit_success_starting": "✅ Recruitment complete! Players: {count}. Starting the game...",
    "no_dm_kicked": (
        "❌ The following players were removed from the game because they haven't opened a private chat with the bot:\n{names}"
    ),
    "not_enough_after_dm_check": (
        "❗ Not enough players left after the private chat check ({count}/{min}). Game cancelled."
    ),

    # --- Game start / cards ---
    "cards_sent": "📨 Character cards have been sent to all players via DM!",
    "card_dm_intro": "🎴 <b>Your character in the «Bunker» game</b>\n\nChat: {chat_title}\n\n{card}",
    "card_profession": "💼 <b>Profession:</b> {value}",
    "card_bio": "🚻 <b>Gender/age:</b> {value}",
    "card_health": "❤️ <b>Health:</b> {value}",
    "card_hobby": "🎨 <b>Hobby:</b> {value}",
    "card_phobia": "😱 <b>Phobia:</b> {value}",
    "card_baggage": "🎒 <b>Baggage:</b> {value}",
    "card_fact": "📌 <b>Extra fact:</b> {value}",

    "catastrophe_title": "☄️ <b>CATASTROPHE</b>",
    "bunker_info_title": "🏚 <b>Bunker information</b>",

    "game_starting": "🎮 The game is starting! Participants: {count}.",

    # --- Rounds ---
    "round_announce": (
        "🔄 <b>Round {round}</b>\n"
        "Players remaining: {alive}\n"
        "Eliminated this round: 1 player"
    ),
    "round1_forced": (
        "📢 In round one, all players must reveal their <b>Profession</b>."
    ),
    "reveal_prompt_dm": (
        "🔄 <b>Round {round}</b>\n\n"
        "Choose which trait to reveal in chat «{chat_title}».\n"
        "You have {seconds} sec. If you don't choose in time, no trait will be revealed."
    ),
    "reveal_already_open": "This trait has already been revealed.",
    "reveal_choice_saved": "✅ You chose to reveal: <b>{trait}</b>",
    "reveal_no_traits_left": "❗ You have no unrevealed traits left.",
    "reveal_time_left": "⏳ {seconds} sec. left to choose.",

    "trait_profession": "Profession",
    "trait_bio": "Gender/age",
    "trait_health": "Health",
    "trait_hobby": "Hobby",
    "trait_phobia": "Phobia",
    "trait_baggage": "Baggage",
    "trait_fact": "Extra fact",

    "reveal_results_title": "📖 <b>Revealed traits — Round {round}</b>",
    "reveal_none_chose": "😶 {name} didn't choose in time — nothing was revealed.",
    "reveal_player_line": "👤 <b>{name}</b>: {trait_name} — {value}",

    "discussion_start": (
        "💬 <b>Discussion</b>\n"
        "You have {seconds} sec. to discuss and decide who to remove from the bunker."
    ),
    "discussion_time_left": "⏳ {seconds} sec. left until the end of discussion.",

    "voting_start": (
        "🗳 <b>Voting — Round {round}</b>\n\n"
        "Choose who to remove from the bunker. Voting is open.\n"
        "You cannot vote against yourself.\n"
        "Time: {seconds} sec."
    ),
    "voting_time_left": "⏳ {seconds} sec. left until the end of voting.",
    "vote_registered": "🗳 {voter} voted against {target}",
    "vote_cannot_self": "❗ You cannot vote against yourself.",
    "vote_not_alive": "❗ You have been eliminated and cannot vote.",
    "vote_target_not_alive": "❗ This player has already been eliminated.",
    "vote_changed": "🔄 {voter} changed their vote: now against {target}",

    "voting_results_title": "📊 <b>Voting results — Round {round}</b>",
    "voting_results_line": "▪️ {name}: {votes} vote(s)",
    "voting_no_votes": "😶 No one voted this round.",
    "voting_tie": "⚖️ Tie between: {names}. No one leaves the bunker this round.",
    "voting_eliminated": "❌ <b>{name}</b> received the most votes and leaves the bunker!",
    "eliminated_reveal": "🎴 {name}'s unrevealed traits:\n{traits}",

    "game_over_title": "🏆 <b>GAME OVER!</b>",
    "game_over_winners": "Winners remaining in the bunker:",
    "winner_card": "👤 <b>{name}</b>\n{card}",
    "game_over_stats_updated": "📈 Player stats updated. Check them with /profile",

    "game_stopped": "🛑 The game was stopped by admin {name}.",
    "game_force_started": "▶️ The game was force-started by admin {name}.",

    "player_left_mid_game": "🚪 {name} left the game and is automatically eliminated from the bunker.",
    "not_enough_players_midgame": "❗ Not enough players to continue the game. The game has been stopped.",

    # --- settings ---
    "settings_title": "⚙️ <b>«Bunker» game settings for this chat</b>",
    "settings_lang": "🌐 Language: {lang}",
    "settings_recruit_time": "⏱ Recruitment time: {seconds} sec.",
    "settings_discussion_time": "💬 Discussion time: {seconds} sec.",
    "settings_voting_time": "🗳 Voting time: {seconds} sec.",
    "settings_choose_option": "Choose what to change:",
    "settings_choose_lang": "Choose a language:",
    "settings_choose_time": "Choose a value (in seconds):",
    "settings_updated": "✅ Settings updated.",
    "settings_only_admin": "❗ Only a chat admin can change the settings.",
    "btn_change_lang": "🌐 Language",
    "btn_change_recruit_time": "⏱ Recruitment time",
    "btn_change_discussion_time": "💬 Discussion time",
    "btn_change_voting_time": "🗳 Voting time",
    "btn_close": "✖️ Close",

    # --- help ---
    "help_text": (
        "📖 <b>«Bunker» game rules</b>\n\n"
        "A catastrophe has destroyed the world on the surface. The bunker has a limited number of spots. "
        "Players are random people, each with their own traits "
        "(profession, biology, health, hobby, phobia, baggage, fact).\n\n"
        "Each round, players reveal one trait, followed by a discussion and an "
        "open vote on who should leave the bunker. The player with the most votes "
        "is eliminated. In case of a tie, no one is eliminated.\n\n"
        "The game continues until 2 players remain in the bunker — they become the winners.\n\n"
        "<b>Commands:</b>\n"
        "/game — start player recruitment\n"
        "/start — force-start the game (if players ≥ {min})\n"
        "/stop — stop the game (admin only)\n"
        "/leave — leave the recruitment\n"
        "/settings — chat settings (admin only)\n"
        "/profile — your stats\n"
        "/help — this message"
    ),

    # --- profile ---
    "profile_title": "👤 <b>{name}'s stats</b>",
    "profile_games": "🎮 Games played: {games}",
    "profile_wins": "🏆 Wins: {wins}",
    "profile_winrate": "📊 Win rate: {winrate}%",
    "profile_no_games": "You haven't played any games yet. Join a game with /game!",

    # --- misc / errors ---
    "dm_only_command": "❗ This command must be used in a private chat with the bot.",
    "start_private": (
        "👋 Hi! I'm the host bot for the «Bunker» game.\n\n"
        "Add me to a group chat and use /game there to start a game."
    ),
    "not_your_button": "❗ This button isn't for you.",
    "game_in_progress_wait": "❗ A game is already in progress, please wait for it to finish.",
}
