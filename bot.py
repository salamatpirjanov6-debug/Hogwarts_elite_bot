import json
import logging
import os
import random
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
)

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7718919427:AAH0p85L_XFsc-2n0L8O956T8Xw68Y9NqE")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa"
BOT_USERNAME = "Hogwarts_elite_bot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
USERS_FILE = "bot_users.json"
WELCOME_FILE = "welcome_settings.json"
FORCED_CHANNELS_FILE = "forced_channels.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

def register_user(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) not in users:
        users[str(user_id)] = True
        save_data(USERS_FILE, users)

# --- MA'LUMOTLAR BAZASI (ORIGINAL IZOHLAR BILAN) ---
BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE", "caption": "📖 Nomi: Garri Potter va Falsafiy tosh\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE", "caption": "📖 Nomi: Garri Potter va Maxfiy hujra\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA", "caption": "📖 Nomi: Garri Potter va Azkaban mahbusi\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE", "caption": "📖 Nomi: Garri Potter va Otashli jom\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE", "caption": "📖 Nomi: Garri Potter va Kaknus ordeni\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE", "caption": "📖 Nomi: Garri Potter va Chalazot shahzoda\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 7. Ajal tuhfalari", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA", "caption": "📖 Nomi: Garri Potter va Ajal tuhfalari\n\nKanal: @harry_potter_fans_uz"},
]

BOOKS_EN = [
    {"name": "📖 1. Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ", "caption": "📖 Name: Harry Potter and the Philosopher's Stone\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 2. Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA", "caption": "📖 Name: Harry Potter and the Chamber of Secrets\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 3. Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ", "caption": "📖 Name: Harry Potter and the Prisoner of Azkaban\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 4. Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ", "caption": "📖 Name: Harry Potter and the Goblet of Fire\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 5. Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ", "caption": "📖 Name: Harry Potter and the Order of the Phoenix\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 6. Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ", "caption": "📖 Name: Harry Potter and the Half-Blood Prince\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 7. Deathly Hallows", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Name: Harry Potter and the Deathly Hallows\n\nChannel: @harry_potter_fans_uz"},
]

BOOKS_ALL = [{"name": "📚 All Books (1-7)", "file_id": "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ", "caption": "📚 Harry Potter All Books (1-7)\n\nChannel: @harry_potter_fans_uz"}]

MOVIES_UZ = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA", "caption": "1. 🎬 Nomi: HP 1: Hikmatlar toshi\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:32:22\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 2. Maxfiy hujra", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA", "caption": "2. 🎬 Nomi: HP 2: Maxfiy hujra\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:54:25\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 3. Azkoban maxbusi", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "3. 🎬 Nomi: HP 3: Azkoban maxbusi\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:21:43\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 4. Alanga kubogi", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "4. 🎬 Nomi: HP 4: Alanga kubogi\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:31:27\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 5. Feniks jamiyati", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "5. 🎬 Nomi: HP 5: Feniks jamiyati\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:18:15\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 6. Tilsim Shahzoda", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA", "caption": "6. 🎬 Nomi: HP 6: Tilsim Shahzoda\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:33:32\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 7. Ajal tuhfasi 1", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA", "caption": "7. 🎬 Nomi: HP 7: Ajal tuhfasi 1-qism\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:26:06\n\nKanal: @harry_potter_fans_uz"},
    {"name": "🎬 8. Ajal tuhfalari 2", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "8. 🎬 Nomi: HP 8: Ajal tuhfalari 2-qism\n\n🌎 Davlati: Buyuk Britaniya\n💽 Formati: 720p HD\n🇺🇿 Tili: Oʻzbek tili\n⌚️ Davomiyligi: 2:10:28\n\nKanal: @harry_potter_fans_uz"},
]

MOVIES_RU = [
    {"name": "🎬 1. Философский камень", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE", "caption": "1. 🎬 Название: ГП 1: Философский камень\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:32:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 2. Тайная комната", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ", "caption": "2. 🎬 Название: ГП 2: Тайная комната\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:41:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 3. Узник Азкабана", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ", "caption": "3. 🎬 Название: ГП 3: Узник Азкабана\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:22:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 4. Кубок огня", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE", "caption": "4. 🎬 Название: ГП 4: Кубок огня\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:37:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 5. Финикс ордени", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ", "caption": "5. 🎬 Название: ГП 5: Орден Феникса\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:18:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 6. Принц-полукровка", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ", "caption": "6. 🎬 Название: ГП 6: Принц-полукровка\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:33:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 7. Дары Смерти 1", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ", "caption": "7. 🎬 Название: ГП 7: Дары Смерти: Часть 1\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:26:00\n\nКанал: @harry_potter_fans_uz"},
    {"name": "🎬 8. Дары Смерти 2", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE", "caption": "8. 🎬 Название: ГП 8: Дары Смерти: Часть 2\n\n🌎 Страна: Великобритания\n💽 Формат: 720p HD\n🇷🇺 Язык: Русский дубляж\n⌚️ Длительность: 2:10:00\n\nКанал: @harry_potter_fans_uz"},
]

MOVIES_EN = [
    {"name": "🎬 1. Sorcerer's Stone", "file_id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ", "caption": "1. 🎬 Name: HP 1: Sorcerer's Stone\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:32:21\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 2. Chamber of Secrets", "file_id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ", "caption": "2. 🎬 Name: HP 2: Chamber of Secrets\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:40:55\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 3. Prisoner of Azkaban", "file_id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ", "caption": "3. 🎬 Name: HP 3: Prisoner of Azkaban\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:21:41\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 4. Goblet of Fire", "file_id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ", "caption": "4. 🎬 Name: HP 4: Goblet of Fire\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:37:05\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 5. Order of the Phoenix", "file_id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ", "caption": "5. 🎬 Name: HP 5: Order of the Phoenix\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:18:14\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 6. Half-Blood Prince", "file_id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ", "caption": "6. 🎬 Name: HP 6: Half-Blood Prince\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:33:30\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 7. Deathly Hallows 1", "file_id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ", "caption": "7. 🎬 Name: HP 7: Deathly Hallows Part 1\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:26:05\n\nChannel: @harry_potter_fans_uz"},
    {"name": "🎬 8. Deathly Hallows 2", "file_id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ", "caption": "8. 🎬 Name: HP 8: Deathly Hallows Part 2\n\n🌎 Country: United Kingdom\n💽 Format: 720p HD\n🇬🇧 Language: English\n⌚️ Duration: 2:10:26\n\nChannel: @harry_potter_fans_uz"},
]

SORTING_MESSAGES = [
    "🤔 *Hmmm... qiyin, juda qiyin.* \nKo'ryapman, bu yerda aql ham yetarli, iste'dod ham... va-a-ay, qanday ulkan xohish!",
    "🧐 *Iye, bu qanday sirli qalb?* \nAql bovar qilmaydigan jasorat, biroz makr... Ha, sen Hogvarts tarixini o'zgartira olasan!",
    "💭 *E-eh, men ko'ryapman...* \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan.",
    "🐍 *Qiziq, juda qiziq...* \nShon-shuhratga bo'lgan chanqoqlik, aqlli munosabat. Ha, sen buyuklikka loyiqsan!",
    "🦁 *Bu yerda nima bor?* \nYuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Ha, jasurlik sening qoningda!"
]

houses_dict = {"Slytherin": "ilon", "Hufflepuff": "aql", "Ravenclaw": "burgut", "Gryffindor": "jasorat"}
house_emojis = {"Slytherin": "🐍", "Hufflepuff": "🦡", "Ravenclaw": "🦅", "Gryffindor": "🦁"}
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}

# --- QO'SHIMCHA FUNKSIYALAR ---
async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        return m_ch.status in ACTIVE_STATUSES, m_gr.status in ACTIVE_STATUSES
    except: return False, False

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

def book_lang_menu():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_book_uz"),
        InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="lang_book_en"),
        InlineKeyboardButton("📚 Hammasi birda", callback_data="lang_book_all"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    return btn

def movie_lang_menu():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_movie_uz"),
        InlineKeyboardButton("🇷🇺 Rus tili", callback_data="lang_movie_ru"),
        InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="lang_movie_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    return btn

# --- MODERATORLIK BUYRUQLARI ---
@dp.message_handler(commands=["mute"])
async def mute_user(message: types.Message):
    if message.chat.type == 'private': return
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin(): return await message.reply("❌ Faqat adminlar!")
    if not message.reply_to_message: return await message.reply("⚠️ Reply qiling!")
    args = message.get_args().split()
    mute_time = int(args[0]) if args and args[0].isdigit() else 15
    until_date = int(asyncio.get_event_loop().time()) + (mute_time * 60)
    await message.chat.restrict(message.reply_to_message.from_user.id, permissions=types.ChatPermissions(can_send_messages=False), until_date=until_date)
    await message.answer(f"🙊 {message.reply_to_message.from_user.first_name} {mute_time} daqiqaga mute qilindi.")

@dp.message_handler(commands=["unmute"])
async def unmute_user(message: types.Message):
    if message.chat.type == 'private': return
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin(): return
    if not message.reply_to_message: return
    await message.chat.restrict(message.reply_to_message.from_user.id, permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
    await message.answer(f"🔊 {message.reply_to_message.from_user.first_name} mutedan olindi.")

# --- START BUYRUG'I ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    register_user(message.from_user.id)
    in_ch, in_gr = await check_sub(message.from_user.id)
    user_mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1)
        btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
                InlineKeyboardButton("👥 Guruhga qo'shilish", url=f"https://t.me/{GROUP[1:]}"),
                InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub_status"))
        return await message.answer(f"Salom {user_mention}! ❗ Botdan foydalanish uchun obuna bo'ling:", reply_markup=btn, parse_mode="HTML")
        
    await message.answer(f"Xush kelibsiz {user_mention}! ✨\n\nHogvarts olamiga kirishga tayyormisiz? Bo'limni tanlang:", reply_markup=main_menu(), parse_mode="HTML")

# --- SHLYAPA HANDLER ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    uid = str(message.from_user.id)
    data = load_data(HOUSES_FILE)
    intro_text = random.choice(SORTING_MESSAGES)
    
    if uid not in data:
        fname = random.choice(list(houses_dict.keys()))
        data[uid] = fname
        save_data(HOUSES_FILE, data)
    
    fname = data[uid]
    key_word = houses_dict[fname]
    emoji = house_emojis[fname]
    
    text = (f"{intro_text}\n\n✨ Hamma narsa ayon! ✨\n\n"
            f"Sizning fakultetingiz: {emoji} **{fname}** {emoji}\n\n"
            f"🔑 Kalit so'zi: `{key_word}`\n\n"
            f"Kalit so'zni shlyapaga yuboring 👇")
    
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapaga yuborish", url=f"https://t.me/{SHLYAPA_USER}"))
    await message.answer(text, reply_markup=btn, parse_mode="Markdown")

# --- ASOSIY MENYU HANDLERLARI ---
@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_menu_handler(message: types.Message):
    await message.answer("Kitoblar uchun tilni tanlang:", reply_markup=book_lang_menu())

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movie_menu_handler(message: types.Message):
    await message.answer("Kinolar uchun tilni tanlang:", reply_markup=movie_lang_menu())

# --- CALLBACK HANDLER ---
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback: types.CallbackQuery):
    uid = callback.message.chat.id
    data = callback.data
    
    if data == "check_sub_status":
        in_ch, in_gr = await check_sub(callback.from_user.id)
        if in_ch and in_gr:
            await callback.message.delete()
            await bot.send_message(uid, "Obuna tasdiqlandi! Bo'limni tanlang:", reply_markup=main_menu())
        else: await callback.answer("Hali obuna bo'lmadingiz!", show_alert=True)
    
    elif data == "back_to_main":
        await callback.message.delete()
        await bot.send_message(uid, "Asosiy menyu:", reply_markup=main_menu())
    
    elif data.startswith("lang_"):
        mode = data.split("_")[1]
        lang = data.split("_")[2]
        btn = InlineKeyboardMarkup(row_width=1)
        if mode == "book":
            if lang == "all": return await bot.send_document(uid, BOOKS_ALL[0]["file_id"], caption=BOOKS_ALL[0]["caption"])
            source = BOOKS_UZ if lang == "uz" else BOOKS_EN
            for i, item in enumerate(source): btn.add(InlineKeyboardButton(item["name"], callback_data=f"bk_{lang}_{i}"))
        else:
            source = MOVIES_UZ if lang == "uz" else (MOVIES_RU if lang == "ru" else MOVIES_EN)
            for i, item in enumerate(source): btn.add(InlineKeyboardButton(item["name"], callback_data=f"mv_{lang}_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("Tanlang:", reply_markup=btn)
        
    elif data.startswith("bk_"):
        _, l, idx = data.split("_"); idx = int(idx)
        item = BOOKS_UZ[idx] if l == "uz" else BOOKS_EN[idx]
        await bot.send_document(uid, item["file_id"], caption=item["caption"])
    
    elif data.startswith("mv_"):
        _, l, idx = data.split("_"); idx = int(idx)
        if l == "uz": item = MOVIES_UZ[idx]
        elif l == "ru": item = MOVIES_RU[idx]
        else: item = MOVIES_EN[idx]
        await bot.send_video(uid, item["file_id"], caption=item["caption"])
    
    await callback.answer()

# --- SET WELCOME & KUTIB OLISH ---
@dp.message_handler(commands=["setwelcome"], user_id=ADMIN_ID)
async def set_welcome_init(message: types.Message):
    await message.reply("Kutib olish xabari (rasm/video/matn) yuboring:")
    dp.register_message_handler(save_welcome_final, user_id=ADMIN_ID, content_types=types.ContentTypes.ANY)

async def save_welcome_final(message: types.Message):
    if message.text and message.text.startswith("/"): return
    text = message.caption if message.caption else (message.text if message.text else "Xush kelibsiz!")
    f_id, f_type = "None", "text"
    if message.photo: f_id, f_type = message.photo[-1].file_id, "photo"
    elif message.video: f_id, f_type = message.video.file_id, "video"
    elif message.animation: f_id, f_type = message.animation.file_id, "animation"
    
    data = load_data(WELCOME_FILE)
    data[str(message.chat.id)] = {"text": text, "file_id": f_id, "file_type": f_type}
    save_data(WELCOME_FILE, data)
    dp.message_handlers.unregister(save_welcome_final)
    await message.reply(f"✅ Saqlandi! Turi: {f_type}")

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_handler(message: types.Message):
    settings = load_data(WELCOME_FILE)
    chat_id = str(message.chat.id)
    if chat_id in settings:
        conf = settings[chat_id]
        mention = f"<a href='tg://user?id={message.new_chat_members[0].id}'>{message.new_chat_members[0].first_name}</a>"
        cap = conf['text'].replace("{name}", mention)
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
            InlineKeyboardButton("🎩 Fakultet tanlash", url=f"https://t.me/{BOT_USERNAME}?start=start")
        )
        try:
            if conf['file_type'] == "photo": await bot.send_photo(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            elif conf['file_type'] == "video": await bot.send_video(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            elif conf['file_type'] == "animation": await bot.send_animation(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            else: await bot.send_message(chat_id, cap, reply_markup=btn, parse_mode="HTML")
        except: pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
