"""
Static content pools used to generate random character cards and catastrophes
for the Bunker game, in three languages: ru, uz, en.
"""
import random

CATASTROPHES = {
    "ru": [
        "☄️ Огромный астероид врезался в Землю, подняв в атмосферу тонны пыли и пепла. Солнечный свет "
        "больше не достигает поверхности, температура стремительно падает.",
        "🦠 По планете стремительно распространяется неизвестный вирус, вызывающий необратимые "
        "мутации у заражённых. Целые города опустели за несколько недель.",
        "☢️ Каскад аварий на атомных станциях по всему миру привёл к глобальному радиоактивному "
        "заражению атмосферы и почвы.",
        "🌋 Супервулкан Йеллоустоун проснулся. Пепельное облако накрыло целые континенты, начался "
        "вулканическая зима.",
        "🌊 Из-за резкого таяния ледников уровень мирового океана поднялся на 60 метров, "
        "затопив большинство прибрежных городов планеты.",
        "🤖 Искусственный интеллект, управлявший военной инфраструктурой, вышел из-под контроля "
        "и начал уничтожать города автономным оружием.",
        "👽 Внеземной корабль-матка появился на орбите и начал распылять токсичный газ, "
        "смертельный для всего живого на поверхности.",
        "🧟 В результате биологической утечки из секретной лаборатории началась эпидемия, "
        "превращающая заражённых в агрессивных нежить-подобных существ.",
        "🌪️ Климатический коллапс вызвал одновременное появление сотен мегаторнадо и ураганов "
        "по всей планете, сделав поверхность непригодной для жизни.",
        "💥 Ядерная война между крупнейшими державами привела к обмену боеголовками и "
        "многолетней ядерной зиме.",
        "🌞 Мощнейшая солнечная вспышка вывела из строя всю электронику планеты и вызвала "
        "аномальное повышение температуры на поверхности.",
        "🕳️ Загадочный разлом в земной коре начал выпускать ядовитые газы, отравляющие "
        "атмосферу планеты.",
    ],
    "uz": [
        "☄️ Ulkan asteroid Yerga urilib, atmosferaga tonnalab chang va kul ko'tardi. Quyosh nuri "
        "endi yer yuzasiga yetib bormaydi, harorat tez sur'atda pasaymoqda.",
        "🦠 Sayyora bo'ylab noma'lum virus tez tarqalmoqda, u yuqtirgan odamlarda qaytarib bo'lmas "
        "mutatsiyalarga sabab bo'lmoqda. Butun shaharlar bir necha haftada bo'shab qoldi.",
        "☢️ Dunyo bo'ylab atom stansiyalarida ketma-ket avariyalar sodir bo'lib, atmosfera va "
        "tuproqning global radioaktiv ifloslanishiga olib keldi.",
        "🌋 Yellowstone superyonqin otildi. Kul buluti butun qit'alarni qopladi, vulqon qishi boshlandi.",
        "🌊 Muzliklarning keskin erishi natijasida jahon okeani sathi 60 metrga ko'tarildi va "
        "sayyoradagi aksariyat qirg'oq shaharlarini suv bosdi.",
        "🤖 Harbiy infratuzilmani boshqarayotgan sun'iy intellekt nazoratdan chiqib, avtonom qurollar "
        "yordamida shaharlarni yo'q qila boshladi.",
        "👽 Orbitada begona sayyoralik ona-kema paydo bo'lib, yer yuzidagi barcha tirik mavjudotlar "
        "uchun zaharli gaz purkay boshladi.",
        "🧟 Maxfiy laboratoriyadan biologik sizib chiqish natijasida yuqtirganlarni tajovuzkor "
        "zombi-o'xshash mavjudotlarga aylantiruvchi epidemiya boshlandi.",
        "🌪️ Iqlim inqirozi butun sayyora bo'ylab yuzlab mega-tornado va bo'ronlarning bir vaqtda "
        "paydo bo'lishiga sabab bo'lib, yer yuzini yashash uchun yaroqsiz qildi.",
        "💥 Yirik davlatlar o'rtasidagi yadroviy urush boshboshdoqlik bilan boshlandi va "
        "ko'p yillik yadroviy qishga olib keldi.",
        "🌞 Kuchli quyosh chaqnashi sayyoradagi barcha elektronikani ishdan chiqardi va "
        "yer yuzasida g'ayritabiiy harorat ko'tarilishiga sabab bo'ldi.",
        "🕳️ Yer po'stlog'idagi sirli yoriq atmosferani zaharlaydigan zaharli gazlarni "
        "chiqara boshladi.",
    ],
    "en": [
        "☄️ A massive asteroid struck Earth, throwing tons of dust and ash into the atmosphere. "
        "Sunlight no longer reaches the surface, and temperatures are dropping rapidly.",
        "🦠 An unknown virus is spreading rapidly across the planet, causing irreversible mutations "
        "in those infected. Entire cities emptied out within weeks.",
        "☢️ A cascade of failures at nuclear plants worldwide has caused global radioactive "
        "contamination of the atmosphere and soil.",
        "🌋 The Yellowstone supervolcano has erupted. Ash clouds have covered entire continents, "
        "triggering a volcanic winter.",
        "🌊 Rapid glacial melting has raised sea levels by 60 meters, flooding most of the "
        "planet's coastal cities.",
        "🤖 An artificial intelligence controlling military infrastructure went rogue and started "
        "destroying cities with autonomous weapons.",
        "👽 An extraterrestrial mothership appeared in orbit and began releasing a toxic gas "
        "lethal to all surface life.",
        "🧟 A biological leak from a secret laboratory has caused an epidemic that turns "
        "the infected into aggressive undead-like creatures.",
        "🌪️ Climate collapse triggered hundreds of simultaneous mega-tornadoes and hurricanes "
        "across the planet, making the surface uninhabitable.",
        "💥 A nuclear war between major world powers led to an exchange of warheads and "
        "years of nuclear winter.",
        "🌞 A massive solar flare knocked out all electronics on the planet and caused "
        "an abnormal rise in surface temperature.",
        "🕳️ A mysterious rift in the Earth's crust began releasing toxic gases that are "
        "poisoning the planet's atmosphere.",
    ],
}

# Extra info about the bunker itself (size, food, duration) - flavor text
BUNKER_INFO = {
    "ru": [
        "Бункер рассчитан на {n} человек. Запасов еды и воды хватит на 6 месяцев. "
        "Предположительное время пребывания под землёй — 2 года.",
        "Убежище имеет {n} спальных мест. Автономная система жизнеобеспечения работает "
        "на дизельном генераторе, топлива хватит на 1 год.",
        "В бункере есть место для {n} человек. Присутствует небольшая оранжерея и "
        "медицинский отсек с ограниченным запасом лекарств.",
    ],
    "uz": [
        "Bunker {n} kishiga mo'ljallangan. Oziq-ovqat va suv zaxirasi 6 oyga yetadi. "
        "Yer ostida taxminiy qolish vaqti — 2 yil.",
        "Boshpanada {n} ta uxlash o'rni bor. Avtonom hayot ta'minoti tizimi dizel generatorida "
        "ishlaydi, yoqilg'i 1 yilga yetadi.",
        "Bunkerda {n} kishi uchun joy bor. Kichik issiqxona va cheklangan dori zaxirasiga ega "
        "tibbiy bo'lim mavjud.",
    ],
    "en": [
        "The bunker is designed for {n} people. Food and water supplies will last 6 months. "
        "Estimated time underground: 2 years.",
        "The shelter has {n} sleeping spots. The autonomous life-support system runs on a "
        "diesel generator, with fuel for 1 year.",
        "The bunker has room for {n} people. There is a small greenhouse and a medical bay "
        "with a limited supply of medicine.",
    ],
}

PROFESSIONS = {
    "ru": [
        "Врач-хирург", "Инженер-строитель", "Учитель начальных классов", "Программист",
        "Повар", "Военный снайпер", "Фермер", "Электрик", "Психолог", "Полицейский",
        "Биолог-генетик", "Пожарный", "Юрист", "Механик", "Агроном", "Ветеринар",
        "Медсестра", "Плотник", "Химик", "Водопроводчик", "Учёный-физик",
        "Пилот вертолёта", "Радист", "Оружейник", "Актёр", "Журналист",
    ],
    "uz": [
        "Jarroh shifokor", "Qurilish muhandisi", "Boshlang'ich sinf o'qituvchisi", "Dasturchi",
        "Oshpaz", "Harbiy snayper", "Fermer", "Elektrik", "Psixolog", "Politsiyachi",
        "Genetik biolog", "O'tchi", "Yurist", "Mexanik", "Agronom", "Veterinar",
        "Hamshira", "Duradgor", "Kimyogar", "Santexnik", "Fizik olim",
        "Vertolyot uchuvchisi", "Radist", "Qurolsoz", "Aktyor", "Jurnalist",
    ],
    "en": [
        "Surgeon", "Civil Engineer", "Elementary School Teacher", "Software Developer",
        "Chef", "Military Sniper", "Farmer", "Electrician", "Psychologist", "Police Officer",
        "Geneticist", "Firefighter", "Lawyer", "Mechanic", "Agronomist", "Veterinarian",
        "Nurse", "Carpenter", "Chemist", "Plumber", "Physicist",
        "Helicopter Pilot", "Radio Operator", "Gunsmith", "Actor", "Journalist",
    ],
}

GENDERS = {
    "ru": ["Мужчина", "Женщина"],
    "uz": ["Erkak", "Ayol"],
    "en": ["Male", "Female"],
}

AGE_RANGE = (18, 70)

HEALTH = {
    "ru": [
        "Полностью здоров(а)", "Хроническая астма", "Аллергия на пыльцу", "Слабое зрение (-4 диоптрии)",
        "Порок сердца (компенсированный)", "Диабет 2 типа", "Полностью здоров(а), отличная физическая форма",
        "Инвалидность (одна нога)", "Хроническая мигрень", "Здоров(а), но склонность к простудам",
        "Проблемы со слухом на одно ухо", "Здоров(а), бывший спортсмен",
    ],
    "uz": [
        "To'liq sog'lom", "Surunkali astma", "Gulchang'ga allergiya", "Zaif ko'rish (-4 diоptriya)",
        "Yurak nuqsoni (kompensatsiyalangan)", "2-toifa qandli diabet", "To'liq sog'lom, ajoyib jismoniy shakl",
        "Nogironlik (bir oyoq)", "Surunkali migren", "Sog'lom, lekin shamollashga moyil",
        "Bir qulog'ida eshitish muammosi", "Sog'lom, sobiq sportchi",
    ],
    "en": [
        "Perfectly healthy", "Chronic asthma", "Pollen allergy", "Poor eyesight (-4 diopters)",
        "Heart defect (compensated)", "Type 2 diabetes", "Perfectly healthy, excellent physical shape",
        "Disability (one leg)", "Chronic migraines", "Healthy but prone to colds",
        "Hearing issue in one ear", "Healthy, former athlete",
    ],
}

HOBBIES = {
    "ru": [
        "Игра на гитаре", "Шахматы", "Рисование", "Скалолазание", "Кулинария",
        "Разведение растений", "Ремонт техники", "Охота", "Рыбалка", "Йога",
        "Чтение книг", "Программирование в свободное время", "Фотография",
        "Боевые искусства", "Танцы", "Резьба по дереву", "Астрономия",
    ],
    "uz": [
        "Gitara chalish", "Shaxmat", "Rasm chizish", "Tog'ga chiqish", "Pazandachilik",
        "O'simlik yetishtirish", "Texnika ta'mirlash", "Ov qilish", "Baliq ovlash", "Yoga",
        "Kitob o'qish", "Bo'sh vaqtda dasturlash", "Fotografiya",
        "Jang san'ati", "Raqs", "Yog'ochni o'ymakorlik qilish", "Astronomiya",
    ],
    "en": [
        "Playing guitar", "Chess", "Painting", "Rock climbing", "Cooking",
        "Growing plants", "Fixing appliances", "Hunting", "Fishing", "Yoga",
        "Reading books", "Coding as a hobby", "Photography",
        "Martial arts", "Dancing", "Woodcarving", "Astronomy",
    ],
}

PHOBIAS = {
    "ru": [
        "Клаустрофобия (боязнь замкнутых пространств)", "Арахнофобия (боязнь пауков)",
        "Аэрофобия (боязнь полётов)", "Никтофобия (боязнь темноты)",
        "Социофобия (боязнь общества)", "Гемофобия (боязнь крови)",
        "Танатофобия (боязнь смерти)", "Агорафобия (боязнь открытых пространств)",
        "Мизофобия (боязнь грязи и микробов)", "Офидиофобия (боязнь змей)",
        "Никакой фобии", "Акрофобия (боязнь высоты)",
    ],
    "uz": [
        "Klaustrofobiya (yopiq joylardan qo'rqish)", "Araxnofobiya (o'rgimchaklardan qo'rqish)",
        "Aerofobiya (uchishdan qo'rqish)", "Niktofobiya (qorong'ilikdan qo'rqish)",
        "Sotsiofobiya (jamiyatdan qo'rqish)", "Gemofobiya (qondan qo'rqish)",
        "Tanatofobiya (o'limdan qo'rqish)", "Agorafobiya (ochiq joylardan qo'rqish)",
        "Mizofobiya (kir va mikroblardan qo'rqish)", "Ofidiofobiya (ilonlardan qo'rqish)",
        "Fobiya yo'q", "Akrofobiya (balandlikdan qo'rqish)",
    ],
    "en": [
        "Claustrophobia (fear of enclosed spaces)", "Arachnophobia (fear of spiders)",
        "Aerophobia (fear of flying)", "Nyctophobia (fear of darkness)",
        "Social phobia (fear of social situations)", "Hemophobia (fear of blood)",
        "Thanatophobia (fear of death)", "Agoraphobia (fear of open spaces)",
        "Mysophobia (fear of germs and dirt)", "Ophidiophobia (fear of snakes)",
        "No phobia", "Acrophobia (fear of heights)",
    ],
}

BAGGAGE = {
    "ru": [
        "Аптечка первой помощи", "Ящик с инструментами", "Мешок с семенами растений",
        "Портативная рация", "Охотничье ружьё и патроны", "Стопка книг по выживанию",
        "Генератор на солнечных батареях", "Запас консервов на месяц", "Набор для рыбалки",
        "Швейная машинка", "Ноутбук с офлайн-базой знаний", "Музыкальный инструмент",
        "Канистра с бензином", "Палатка и спальный мешок",
    ],
    "uz": [
        "Birinchi yordam sumkasi", "Asboblar qutisi", "O'simlik urug'lari xaltasi",
        "Portativ ratsiya", "Ov miltig'i va patronlar", "Omon qolish bo'yicha kitoblar to'plami",
        "Quyosh batareyali generator", "Bir oylik konservalar zaxirasi", "Baliq ovlash to'plami",
        "Tikuv mashinasi", "Oflayn bilimlar bazasi bo'lgan noutbuk", "Musiqa asbobi",
        "Benzin kanistri", "Chodir va uxlash xaltasi",
    ],
    "en": [
        "First aid kit", "Toolbox", "Bag of plant seeds",
        "Portable radio", "Hunting rifle and ammunition", "Stack of survival books",
        "Solar-powered generator", "A month's supply of canned food", "Fishing kit",
        "Sewing machine", "Laptop with offline knowledge base", "Musical instrument",
        "Canister of gasoline", "Tent and sleeping bag",
    ],
}

FACTS = {
    "ru": [
        "Бывший заключённый, отсидел 3 года за экономическое преступление",
        "Тайно ведёт дневник обо всех участниках", "Не спал уже двое суток",
        "Является дальним родственником одного из других игроков (неизвестно, кого)",
        "Раньше служил в спецназе", "Панически боится потерять контроль над ситуацией",
        "Тайно влюблён(а) в одного из участников", "Страдает бессонницей на нервной почве",
        "Является атеистом в семье глубоко верующих людей", "Умеет читать по губам",
        "Владеет тремя иностранными языками", "Ранее уже выживал(а) в экстремальной ситуации",
        "Скрывает, что раньше был(а) знаменитостью", "Является донором редкой группы крови",
    ],
    "uz": [
        "Sobiq mahbus, iqtisodiy jinoyat uchun 3 yil o'tirgan",
        "Barcha ishtirokchilar haqida yashirincha kundalik yuritadi", "Ikki kundan beri uxlamagan",
        "Boshqa o'yinchilardan birining uzoq qarindoshi (kimligi noma'lum)",
        "Ilgari maxsus kuchlarda xizmat qilgan", "Vaziyat nazoratini yo'qotishdan qattiq qo'rqadi",
        "Ishtirokchilardan biriga yashirincha oshiq", "Asabiylashish tufayli uyqusizlikdan aziyat chekadi",
        "Chuqur diniy oiladagi ateist", "Lablardan o'qishni biladi",
        "Uch xorijiy tilni biladi", "Ilgari ekstremal vaziyatda omon qolgan",
        "Ilgari mashhur bo'lganini yashiradi", "Kamyob qon guruhining donori",
    ],
    "en": [
        "Former convict, served 3 years for an economic crime",
        "Secretly keeps a diary about all the other participants", "Hasn't slept in two days",
        "Is a distant relative of one of the other players (unknown which one)",
        "Former special forces soldier", "Panics at the thought of losing control of a situation",
        "Secretly in love with one of the participants", "Suffers from stress-induced insomnia",
        "An atheist in a deeply religious family", "Can read lips",
        "Speaks three foreign languages", "Has survived an extreme situation before",
        "Hides the fact that they used to be a celebrity", "Is a donor of a rare blood type",
    ],
}


def random_catastrophe(lang: str) -> str:
    return random.choice(CATASTROPHES.get(lang, CATASTROPHES["ru"]))


def random_bunker_info(lang: str, capacity: int) -> str:
    template = random.choice(BUNKER_INFO.get(lang, BUNKER_INFO["ru"]))
    return template.format(n=capacity)


def generate_character(lang: str) -> dict:
    """Generate a random full character trait set for one player."""
    lang = lang if lang in PROFESSIONS else "ru"
    gender = random.choice(GENDERS[lang])
    age = random.randint(*AGE_RANGE)
    return {
        "profession": random.choice(PROFESSIONS[lang]),
        "bio": f"{gender}, {age}",
        "health": random.choice(HEALTH[lang]),
        "hobby": random.choice(HOBBIES[lang]),
        "phobia": random.choice(PHOBIAS[lang]),
        "baggage": random.choice(BAGGAGE[lang]),
        "fact": random.choice(FACTS[lang]),
    }
