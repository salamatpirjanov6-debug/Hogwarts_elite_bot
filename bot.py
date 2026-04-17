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

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

# --- TO'LIQ KITOOBLAR BAZASI ---
BOOKS = {
    "uz": [
        {"name": "📖 1. Falsafiy tosh", "id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE"},
        {"name": "📖 2. Maxfiy xujra", "id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE"},
        {"name": "📖 3. Azkaban maxbusi", "id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA"},
        {"name": "📖 4. Otashli jom", "id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE"},
        {"name": "📖 5. Kaknus ordeni", "id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE"},
        {"name": "📖 6. Chalazot shaxzoda", "id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE"},
        {"name": "📖 7. Ajal tuhfalari", "id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA"},
    ],
    "en": [
        {"name": "📖 1. Philosopher's Stone", "id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ"},
        {"name": "📖 2. Chamber of Secrets", "id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA"},
        {"name": "📖 3. Prisoner of Azkaban", "id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ"},
        {"name": "📖 4. Goblet of Fire", "id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ"},
        {"name": "📖 5. Order of the Phoenix", "id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ"},
        {"name": "📖 6. Half-Blood Prince", "id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ"},
        {"name": "📖 7. Deathly Hallows", "id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ"},
    ],
    "all": [{"name": "📚 Hammasi birda (1-7)", "id": "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ"}]
}

# --- TO'LIQ KINOLAR BAZASI ---
MOVIES = {
    "uz": [
        {"name": "🎬 1. Hikmatlar toshi", "id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA"},
        {"name": "🎬 2. Maxfiy hujra", "id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA"},
        {"name": "🎬 3. Azkoban maxbusi", "id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
        {"name": "🎬 4. Alanga kubogi", "id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZF9wiu0Drs6BA"},
        {"name": "🎬 5. Feniks jamiyati", "id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
        {"name": "🎬 6. Tilsim Shahzoda", "id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA"},
        {"name": "🎬 7. Ajal tuhfasi 1", "id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA"},
        {"name": "🎬 8. Ajal tuhfalari 2", "id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
    ],
    "ru": [
        {"name": "🎬 1. Философский камень", "id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE"},
        {"name": "🎬 2. Тайная комната", "id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ"},
        {"name": "🎬 3. Узник Азкабана", "id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ"},
        {"name": "🎬 4. Кубок огня", "id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE"},
        {"name": "🎬 5. Орден Феникса", "id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ"},
        {"name": "🎬 6. Принц-полукровка", "id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ"},
        {"name": "🎬 7. Дары Смерти 1", "id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ"},
        {"name": "🎬 8. Дары Смерти 2", "id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE"},
    ],
    "en": [
        {"name": "🎬 1. Sorcerer's Stone", "id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ"},
        {"name": "🎬 2. Chamber of Secrets", "id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ"},
        {"name": "🎬 3. Prisoner of Azkaban", "id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ"},
        {"name": "🎬 4. Goblet of Fire", "id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ"},
        {"name": "🎬 5. Order of the Phoenix", "id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ"},
        {"name": "🎬 6. Half-Blood Prince", "id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ"},
        {"name": "🎬 7. Deathly Hallows 1", "id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ"},
        {"name": "🎬 8. Deathly Hallows 2", "id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ"},
    ]
}

# --- SHLYAPA FRAZALARI ---
SORTING_PHRASES = [
    "🤔 *Hmmm... qiyin, juda qiyin.* \nKo'ryapman, bu yerda aql ham yetarli, iste'dod ham... va-a-ay, qanday ulkan xohish!",
    "🧐 *Iye, bu qanday sirli qalb?* \nAql bovar qilmaydigan jasorat, biroz makr... Ha, sen Hogvarts tarixini o'zgartira olasan!",
    "💭 *E-eh, men ko'ryapman...* \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan.",
    "🐍 *Qiziq, juda qiziq...* \nShon-shuhratga bo'lgan chanqoqlik, aqlli munosabat. Ha, sen buyuklikka loyiqsan!",
    "🦁 *Bu yerda nima bor?* \nYuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Ha, jasurlik sening qoningda!"
]

HOUSES = {
    "Gryffindor": "🦁 Gryffindor!", "Slytherin": "🐍 Slytherin!", 
    "Hufflepuff": "🦡 Hufflepuff!", "Ravenclaw": "🦅 Ravenclaw!"
}

# --- MENYULAR ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

def lang_menu(mode):
    btn = InlineKeyboardMarkup(row_width=2)
    if mode == 'book':
        btn.add(
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="books_uz"),
            InlineKeyboardButton("🇬🇧 English", callback_data="books_en"),
            InlineKeyboardButton("📚 Hammasi birda", callback_data="books_all")
        )
    else:
        btn.add(
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="movies_uz"),
            InlineKeyboardButton("🇷🇺 Ruscha", callback_data="movies_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="movies_en")
        )
    btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
    return btn

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    mention = f"<a href='tg://user?id={user_id}'>{name}</a>"
    
    await message.answer(
        f"Xush kelibsiz {mention}!\n\nHogvarts olamiga kirishga tayyormisiz? Bo'limni tanlang:",
        reply_markup=main_menu(), parse_mode="HTML"
    )

@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_start(message: types.Message):
    await message.answer("Kitob tili va turini tanlang:", reply_markup=lang_menu('book'))

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movie_start(message: types.Message):
    await message.answer("Kino tilini tanlang:", reply_markup=lang_menu('movie'))

@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    data = load_data(HOUSES_FILE)
    uid = str(message.from_user.id)
    phrase = random.choice(SORTING_PHRASES)
    msg = await message.answer(phrase, parse_mode="Markdown")
    await asyncio.sleep(2)
    
    if uid not in data:
        data[uid] = random.choice(list(HOUSES.keys()))
        save_data(HOUSES_FILE, data)
    
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapa yuborish", url=f"https://t.me/{SHLYAPA_USER}"))
    await msg.edit_text(f"{phrase}\n\n✨ Fakultetingiz: **{HOUSES[data[uid]]}**", reply_markup=btn, parse_mode="Markdown")

# --- CALLBACKS ---
@dp.callback_query_handler(lambda c: True)
async def callback_handler(c: types.CallbackQuery):
    if c.data == "back_to_main":
        await c.message.delete()
    elif c.data.startswith("books_"):
        lang = c.data.split("_")[1]
        btn = InlineKeyboardMarkup(row_width=1)
        for i, item in enumerate(BOOKS[lang]):
            btn.add(InlineKeyboardButton(item["name"], callback_data=f"send_b_{lang}_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await c.message.edit_text(f"📖 Tanlang ({lang}):", reply_markup=btn)
    elif c.data.startswith("movies_"):
        lang = c.data.split("_")[1]
        btn = InlineKeyboardMarkup(row_width=1)
        for i, item in enumerate(MOVIES[lang]):
            btn.add(InlineKeyboardButton(item["name"], callback_data=f"send_m_{lang}_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await c.message.edit_text(f"🎬 Tanlang ({lang}):", reply_markup=btn)
    elif c.data.startswith("send_"):
        _, type_char, lang, idx = c.data.split("_")
        idx = int(idx)
        try:
            if type_char == 'b':
                item = BOOKS[lang][idx]
                await bot.send_document(c.message.chat.id, item["id"], caption=f"{item['name']}\n@harry_potter_fans_uz")
            else:
                item = MOVIES[lang][idx]
                await bot.send_video(c.message.chat.id, item["id"], caption=f"{item['name']}\n@harry_potter_fans_uz")
        except:
            await c.answer("Faylni yuborishda xato!", show_alert=True)
    await c.answer()

# --- ADMIN: SET WELCOME (TUZATILGAN) ---
@dp.message_handler(commands=["setwelcome"], user_id=ADMIN_ID)
async def set_welcome_init(message: types.Message):
    await message.answer("Yangi a'zolar uchun xabar (rasm, video yoki matn) yuboring:")
    dp.register_message_handler(save_welcome_final, user_id=ADMIN_ID, content_types=types.ContentTypes.ANY)

async def save_welcome_final(message: types.Message):
    if message.text and message.text.startswith("/"): return
    chat_id = str(message.chat.id)
    text = message.caption if message.caption else message.text
    if not text: text = "Xush kelibsiz, {name}!"
    
    f_id, f_type = "None", "text"
    if message.photo: f_id, f_type = message.photo[-1].file_id, "photo"
    elif message.video: f_id, f_type = message.video.file_id, "video"
    elif message.animation: f_id, f_type = message.animation.file_id, "animation"

    data = load_data(WELCOME_FILE)
    data[chat_id] = {"text": text, "file_id": f_id, "file_type": f_type}
    save_data(WELCOME_FILE, data)
    dp.message_handlers.unregister(save_welcome_final)
    await message.reply(f"✅ Saqlandi! Turi: {f_type}")

# --- KUTIB OLISH ---
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    settings = load_data(WELCOME_FILE)
    chat_id = str(message.chat.id)
    if chat_id in settings:
        conf = settings[chat_id]
        user = message.new_chat_members[0]
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        cap = conf['text'].replace("{name}", mention)
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
        
        try:
            if conf['file_type'] == "photo": await bot.send_photo(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            elif conf['file_type'] == "video": await bot.send_video(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            elif conf['file_type'] == "animation": await bot.send_animation(chat_id, conf['file_id'], caption=cap, reply_markup=btn, parse_mode="HTML")
            else: await bot.send_message(chat_id, cap, reply_markup=btn, parse_mode="HTML")
        except: pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
