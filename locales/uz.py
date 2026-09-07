TEXTS = {
    "lang_name": "O'zbekcha",

    # --- Common ---
    "only_in_group": "❗ Bu buyruq faqat guruhlarda ishlaydi.",
    "not_enough_players": "❗ O'yinchilar yetarli emas. Kamida {min} o'yinchi kerak.",
    "already_max_players": "❗ Maksimal o'yinchilar soniga ({max}) yetildi.",
    "no_active_game": "❗ Hozir bu chatda faol o'yin yo'q.",
    "game_already_running": "❗ Bu chatda allaqachon o'yin yoki o'yinchilar yig'ilishi ketmoqda.",
    "not_admin": "❗ Bu buyruq faqat chat administratorlari uchun mavjud.",
    "unknown_error": "⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
    "back": "⬅️ Orqaga",
    "cancel": "❌ Bekor qilish",

    # --- Recruiting ---
    "recruit_start": (
        "🎮 <b>«Bunker» o'yiniga o'yinchilar yig'ilishi boshlandi!</b>\n\n"
        "Qo'shilish uchun pastdagi tugmani bosing.\n"
        "Kamida: {min}, ko'pi bilan: {max} o'yinchi.\n"
        "Yig'ish {seconds} soniyadan so'ng yoki administratorning /start buyrug'i bilan tugaydi.\n\n"
        "👥 O'yinchilar ({count}/{max}):\n{players}"
    ),
    "join_button": "✅ Qo'shilish",
    "leave_button": "🚪 Chiqish",
    "force_start_button": "▶️ Hozir boshlash",
    "cancel_recruit_button": "❌ Yig'ishni bekor qilish",
    "player_joined": "✅ {name} o'yinga qo'shildi!",
    "player_left": "🚪 {name} yig'ishdan chiqdi.",
    "already_joined": "❗ Siz allaqachon o'yindasiz.",
    "not_in_recruit": "❗ Siz yig'ishda ishtirok etmayapsiz.",
    "recruit_full": "❗ Yig'ish to'ldi.",
    "need_private_chat": (
        "⚠️ {name}, o'ynash uchun bot bilan shaxsiy chatni oching "
        "(@{bot_username} shaxsiy xabarida /start bosing), aks holda siz personaj kartochkasini "
        "olib bo'lmaysiz va o'yindan chiqarilasiz."
    ),
    "recruit_cancelled": "❌ O'yinchilar yig'ishi bekor qilindi.",
    "recruit_cancelled_by": "❌ O'yinchilar yig'ishi {name} administrator tomonidan bekor qilindi.",
    "recruit_timeout_not_enough": (
        "⏱ Yig'ish vaqti tugadi. O'yinni boshlash uchun o'yinchilar yetarli emas (kamida {min} kerak)."
    ),
    "recruit_success_starting": "✅ Yig'ish tugadi! O'yinchilar: {count}. O'yin boshlanmoqda...",
    "no_dm_kicked": (
        "❌ Quyidagi o'yinchilar bot bilan shaxsiy chatni ochmagani uchun o'yindan chiqarildi:\n{names}"
    ),
    "not_enough_after_dm_check": (
        "❗ Shaxsiy xabarlarni tekshirgandan so'ng o'yinchilar yetarli emas ({count}/{min}). O'yin bekor qilindi."
    ),

    # --- Game start / cards ---
    "cards_sent": "📨 Personaj kartochkalari barcha o'yinchilarga shaxsiy xabarda yuborildi!",
    "card_dm_intro": "🎴 <b>«Bunker» o'yinidagi sizning personajingiz</b>\n\nChat: {chat_title}\n\n{card}",
    "card_profession": "💼 <b>Kasb:</b> {value}",
    "card_bio": "🚻 <b>Jins/yosh:</b> {value}",
    "card_health": "❤️ <b>Sog'liq:</b> {value}",
    "card_hobby": "🎨 <b>Xobbi:</b> {value}",
    "card_phobia": "😱 <b>Fobiya:</b> {value}",
    "card_baggage": "🎒 <b>Yuk:</b> {value}",
    "card_fact": "📌 <b>Qo'shimcha fakt:</b> {value}",

    "catastrophe_title": "☄️ <b>OFAT</b>",
    "bunker_info_title": "🏚 <b>Bunker haqida ma'lumot</b>",

    "game_starting": "🎮 O'yin boshlanmoqda! Ishtirokchilar: {count}.",

    # --- Rounds ---
    "round_announce": (
        "🔄 <b>{round}-raund</b>\n"
        "Qolgan o'yinchilar: {alive}\n"
        "Bu raundda chiqib ketadi: 1 o'yinchi"
    ),
    "round1_forced": (
        "📢 Birinchi raundda barcha o'yinchilar o'zining <b>Kasbi</b>ni ochishi shart."
    ),
    "reveal_prompt_dm": (
        "🔄 <b>{round}-raund</b>\n\n"
        "«{chat_title}» chatida ochmoqchi bo'lgan xususiyatni tanlang.\n"
        "Sizda {seconds} soniya bor. Ulgurmasangiz — xususiyat ochilmaydi."
    ),
    "reveal_already_open": "Bu xususiyat allaqachon ochilgan.",
    "reveal_choice_saved": "✅ Siz tanladingiz: <b>{trait}</b>",
    "reveal_no_traits_left": "❗ Sizda boshqa ochilmagan xususiyat qolmadi.",
    "reveal_time_left": "⏳ Tanlash uchun {seconds} soniya qoldi.",

    "trait_profession": "Kasb",
    "trait_bio": "Jins/yosh",
    "trait_health": "Sog'liq",
    "trait_hobby": "Xobbi",
    "trait_phobia": "Fobiya",
    "trait_baggage": "Yuk",
    "trait_fact": "Qo'shimcha fakt",

    "reveal_results_title": "📖 <b>Ochilgan xususiyatlar — {round}-raund</b>",
    "reveal_none_chose": "😶 {name} xususiyat tanlashga ulgurmadi — hech narsa ochilmadi.",
    "reveal_player_line": "👤 <b>{name}</b>: {trait_name} — {value}",

    "discussion_start": (
        "💬 <b>Muhokama</b>\n"
        "Bunkerdan kimni chiqarish kerakligini muhokama qilish uchun {seconds} soniya vaqtingiz bor."
    ),
    "discussion_time_left": "⏳ Muhokama tugashiga {seconds} soniya qoldi.",

    "voting_start": (
        "🗳 <b>Ovoz berish — {round}-raund</b>\n\n"
        "Bunkerdan kimni chiqarishni tanlang. Ovoz berish ochiq.\n"
        "O'zingizga qarshi ovoz bera olmaysiz.\n"
        "Vaqt: {seconds} soniya."
    ),
    "voting_time_left": "⏳ Ovoz berish tugashiga {seconds} soniya qoldi.",
    "vote_registered": "🗳 {voter} {target}ga qarshi ovoz berdi",
    "vote_cannot_self": "❗ O'zingizga qarshi ovoz bera olmaysiz.",
    "vote_not_alive": "❗ Siz o'yindan chiqib ketgansiz va ovoz bera olmaysiz.",
    "vote_target_not_alive": "❗ Bu o'yinchi allaqachon chiqib ketgan.",
    "vote_changed": "🔄 {voter} ovozini o'zgartirdi: endi {target}ga qarshi",

    "voting_results_title": "📊 <b>Ovoz berish natijalari — {round}-raund</b>",
    "voting_results_line": "▪️ {name}: {votes} ovoz",
    "voting_no_votes": "😶 Bu raundda hech kim ovoz bermadi.",
    "voting_tie": "⚖️ Duranglik: {names}. Bu raundda hech kim bunkerni tark etmaydi.",
    "voting_eliminated": "❌ <b>{name}</b> eng ko'p ovoz to'plab, bunkerni tark etadi!",
    "eliminated_reveal": "🎴 {name}ning ochilmagan xususiyatlari:\n{traits}",

    "game_over_title": "🏆 <b>O'YIN TUGADI!</b>",
    "game_over_winners": "Bunkerda qolgan g'oliblar:",
    "winner_card": "👤 <b>{name}</b>\n{card}",
    "game_over_stats_updated": "📈 O'yinchilar statistikasi yangilandi. Tekshirish — /profile",

    "game_stopped": "🛑 O'yin {name} administrator tomonidan to'xtatildi.",
    "game_force_started": "▶️ O'yin {name} administrator tomonidan majburiy boshlandi.",

    "player_left_mid_game": "🚪 {name} o'yinni tark etdi va avtomatik ravishda bunkerdan chiqadi.",
    "not_enough_players_midgame": "❗ O'yinni davom ettirish uchun o'yinchilar yetarli emas. O'yin to'xtatildi.",

    # --- settings ---
    "settings_title": "⚙️ <b>Ushbu chat uchun «Bunker» o'yini sozlamalari</b>",
    "settings_lang": "🌐 Til: {lang}",
    "settings_recruit_time": "⏱ Yig'ish vaqti: {seconds} soniya",
    "settings_discussion_time": "💬 Muhokama vaqti: {seconds} soniya",
    "settings_voting_time": "🗳 Ovoz berish vaqti: {seconds} soniya",
    "settings_choose_option": "O'zgartirmoqchi bo'lgan narsangizni tanlang:",
    "settings_choose_lang": "Tilni tanlang:",
    "settings_choose_time": "Qiymatni tanlang (soniyalarda):",
    "settings_updated": "✅ Sozlamalar yangilandi.",
    "settings_only_admin": "❗ Sozlamalarni faqat chat administratori o'zgartira oladi.",
    "btn_change_lang": "🌐 Til",
    "btn_change_recruit_time": "⏱ Yig'ish vaqti",
    "btn_change_discussion_time": "💬 Muhokama vaqti",
    "btn_change_voting_time": "🗳 Ovoz berish vaqti",
    "btn_close": "✖️ Yopish",

    # --- help ---
    "help_text": (
        "📖 <b>«Bunker» o'yini qoidalari</b>\n\n"
        "Ofat sirtdagi dunyoni yo'q qildi. Bunkerda cheklangan joy bor. "
        "O'yinchilar — tasodifiy odamlar, har birining o'z xususiyatlari bor "
        "(kasb, biologiya, sog'liq, xobbi, fobiya, yuk, fakt).\n\n"
        "Har raundda o'yinchilar bitta xususiyatni ochadi, so'ngra muhokama va "
        "ochiq ovoz berish o'tkaziladi — kim bunkerni tark etishi kerak. Eng ko'p ovoz olgan o'yinchi "
        "chiqib ketadi. Durang bo'lsa, hech kim chiqmaydi.\n\n"
        "O'yin bunkerda 2 kishi qolgunicha davom etadi — ular g'olib bo'ladi.\n\n"
        "<b>Buyruqlar:</b>\n"
        "/game — o'yinchilar yig'ishni boshlash\n"
        "/start — o'yinni majburiy boshlash (agar o'yinchilar ≥ {min} bo'lsa)\n"
        "/stop — o'yinni to'xtatish (faqat admin)\n"
        "/leave — yig'ishdan chiqish\n"
        "/settings — chat sozlamalari (faqat admin)\n"
        "/profile — sizning statistikangiz\n"
        "/help — ushbu xabar"
    ),

    # --- profile ---
    "profile_title": "👤 <b>{name} statistikasi</b>",
    "profile_games": "🎮 O'ynalgan o'yinlar: {games}",
    "profile_wins": "🏆 G'alabalar: {wins}",
    "profile_winrate": "📊 G'alaba foizi: {winrate}%",
    "profile_no_games": "Sizda hali o'ynalgan o'yinlar yo'q. /game buyrug'i orqali o'yinga qo'shiling!",

    # --- misc / errors ---
    "dm_only_command": "❗ Bu buyruqni bot bilan shaxsiy xabarlarda ishlatish kerak.",
    "start_private": (
        "👋 Salom! Men «Bunker» o'yini uchun boshlovchi botman.\n\n"
        "Meni guruh chatiga qo'shing va o'yinni boshlash uchun /game buyrug'ini yuboring."
    ),
    "not_your_button": "❗ Bu tugma siz uchun emas.",
    "game_in_progress_wait": "❗ O'yin allaqachon davom etmoqda, tugashini kuting.",
}
