import json
import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa" # Saralovchi shlyapa username

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- 1. ESKI IDlar (O'ZBEKCHA) ---
BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE"},
    {"name": "📖 7. Ajal tuhfalari", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA"},
    {"name": "📖 8. La'natlangan bola 1", "file_id": "BQACAgEAAxkBAANvacuw28JOcJ8hlcLe8Eq33Lr6FssAAuoAA2FcqEc7oEBDKKT05ToE"},
    {"name": "📖 9. La'natlangan bola 2", "file_id": "BQACAgIAAxkBAANxacuxAAE5y-wWgOHjT2_RNea7LkjdAAKsAgACLVkpSLjOwEQYWEw-OgQ"},
]

MOVIES_UZ = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA"},
    {"name": "🎬 2. Maxfiy hujra", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA"},
    {"name": "🎬 3. Azkoban maxbusi", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 4. Alanga kubogi", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
    {"name": "🎬 5. Feniks jamiyati", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 6. Tilsim Shahzoda", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA"},
    {"name": "🎬 7. Ajal tuhfasi 1", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA"},
    {"name": "🎬 8. Ajal tuhfalari 2", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
]

# --- 2. INGLIZCHA MA'LUMOTLAR (MENYULI QILINDI) ---
BOOKS_EN = [
    {"name": "📖 HP 1: Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ"},
    {"name": "📖 HP 2: Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA"},
    {"name": "📖 HP 3: Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ"},
    {"name": "📖 HP 4: Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ"},
    {"name": "📖 HP 5: Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ"},
    {"name": "📖 HP 6: Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ"},
    {"name": "📖 HP 7: Deathly Hallows", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ"}
]

MOVIES_EN = [
    {"name": "🎬 Movie 1 (EN)", "file_id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ"},
    {"name": "🎬 Movie 2 (EN)", "file_id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ"},
    {"name": "🎬 Movie 3 (EN)", "file_id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ"},
    {"name": "🎬 Movie 4 (EN)", "file_id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ"},
    {"name": "🎬 Movie 5 (EN)", "file_id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ"},
    {"name": "🎬 Movie 6 (EN)", "file_id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ"},
    {"name": "🎬 Movie 7 (EN)", "file_id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ"},
    {"name": "🎬 Movie 8 (EN)", "file_id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ"}
]

MOVIES_RU = [
    {"name": "🎬 Фильм 1 (RU)", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE"},
    {"name": "🎬 Фильм 2 (RU)", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ"},
    {"name": "🎬 Фильм 3 (RU)", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ"},
    {"name": "🎬 Фильм 4 (RU)", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE"},
    {"name": "🎬 Фильм 5 (RU)", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ"},
    {"name": "🎬 Фильм 6 (RU)", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ"},
    {"name": "🎬 Фильм 7 (RU)", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ"},
    {"name": "🎬 Фильм 8 (RU)", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE"}
]

ALL_IN_ONE_BOOK = "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ"

# --- 3. MENYULAR ---
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

houses = ["🦁 Gryffindor", "🐍 Slytherin", "🦡 Hufflepuff", "🦅 Ravenclaw"]
HOUSES_FILE = "user_houses.json"
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}

# --- BAZA ---
def load_houses():
    if os.path.exists(HOUSES_FILE):
        with open(HOUSES_FILE, "r") as f: return json.load(f)
    return {}

def save_house(user_id, house):
    data = load_houses()
    data[str(user_id)] = house
    with open(HOUSES_FILE, "w") as f: json.dump(data, f)

async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        return m_ch.status in ACTIVE_STATUSES, m_gr.status in ACTIVE_STATUSES
    except: return False, False

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    in_ch, in_gr = await check_sub(message.from_user.id)
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1)
        if not in_ch: btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
        if not in_gr: btn.add(InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo'ling:", reply_markup=btn)
        return
    
    # ISM BILAN SALOMLASHISH
    user_name = message.from_user.first_name
    await message.answer(f"Xush kelibsiz {user_name}! Kerakli bo'limni tanlang:", reply_markup=main_menu())

@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def show_book_langs(message: types.Message):
    await message.answer("Kitoblar uchun tilni tanlang:", reply_markup=book_lang_menu())

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def show_movie_langs(message: types.Message):
    await message.answer("Kinolar uchun tilni tanlang:", reply_markup=movie_lang_menu())

# --- CALLBACKLAR ---
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback: types.CallbackQuery):
    uid = callback.message.chat.id
    
    if callback.data == "back_to_main":
        await callback.message.delete()
        await bot.send_message(uid, "Asosiy menyu:", reply_markup=main_menu())

    # --- KITOB MENYULARI ---
    elif callback.data == "lang_book_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"uzbook_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="lang_book_menu_back"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kitoblar:", reply_markup=btn)

    elif callback.data == "lang_book_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_EN): btn.add(InlineKeyboardButton(b["name"], callback_data=f"enbook_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="lang_book_menu_back"))
        await callback.message.edit_text("🇬🇧 English Books:", reply_markup=btn)

    elif callback.data == "lang_book_all":
        await bot.send_document(uid, ALL_IN_ONE_BOOK)

    # --- KINO MENYULARI ---
    elif callback.data == "lang_movie_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"uzmovie_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="lang_movie_menu_back"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kinolar:", reply_markup=btn)

    elif callback.data == "lang_movie_ru":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_RU): btn.add(InlineKeyboardButton(m["name"], callback_data=f"rumovie_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="lang_movie_menu_back"))
        await callback.message.edit_text("🇷🇺 Русские фильмы:", reply_markup=btn)

    elif callback.data == "lang_movie_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_EN): btn.add(InlineKeyboardButton(m["name"], callback_data=f"enmovie_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="lang_movie_menu_back"))
        await callback.message.edit_text("🇬🇧 English Movies:", reply_markup=btn)

    # --- FAYL YUBORISH ---
    elif callback.data.startswith("uzbook_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_document(uid, BOOKS_UZ[idx]["file_id"], caption=BOOKS_UZ[idx]["name"])
    elif callback.data.startswith("enbook_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_document(uid, BOOKS_EN[idx]["file_id"], caption=BOOKS_EN[idx]["name"])
    elif callback.data.startswith("uzmovie_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_video(uid, MOVIES_UZ[idx]["file_id"], caption=MOVIES_UZ[idx]["name"])
    elif callback.data.startswith("rumovie_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_video(uid, MOVIES_RU[idx]["file_id"], caption=MOVIES_RU[idx]["name"])
    elif callback.data.startswith("enmovie_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_video(uid, MOVIES_EN[idx]["file_id"], caption=MOVIES_EN[idx]["name"])

    elif callback.data == "lang_book_menu_back":
        await callback.message.edit_text("Kitoblar uchun tilni tanlang:", reply_markup=book_lang_menu())
    elif callback.data == "lang_movie_menu_back":
        await callback.message.edit_text("Kinolar uchun tilni tanlang:", reply_markup=movie_lang_menu())

    await callback.answer()

# --- SHLYAPA (KALIT SO'ZLAR VA USERNAME BILAN) ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    uid = str(message.from_user.id)
    data = load_houses()
    
    # Kalit so'zlar (Eski kodda bo'lgan matnlar)
    intro_text = (
        "🔍 Men sening xarakteringni o'rganib chiqdim...\n"
        "✨ Qalbingdagi yashirin kuchlarni ko'ryapman.\n"
        "🧙‍♂️ Qaysi fakultet senga munosib ekanini aniqladim!"
    )
    
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("🎩 Shlyapa bilan bog'lanish", url=f"https://t.me/{SHLYAPA_USER}"))

    if uid in data:
        await message.answer(f"{intro_text}\n\nSiz allaqachon saralangansiz! Fakultetingiz: **{data[uid]}**", reply_markup=btn, parse_mode="Markdown")
    else:
        res = random.choice(houses)
        save_house(uid, res)
        await message.answer(f"{intro_text}\n\nSaralovchi shlyapa tanlovi: **{res}**!", reply_markup=btn, parse_mode="Markdown")

# Admin uchun ID olish funksiyasi saqlandi
@dp.message_handler(content_types=["document", "video"])
async def get_ids(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        fid = message.document.file_id if message.document else message.video.file_id
        await message.reply(f"🔑 file_id: <code>{fid}</code>", parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
