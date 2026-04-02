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
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- MA'LUMOTLAR BAZASI (IDLAR) ---
# Siz bergan yangi IDlar joylashtirildi
ENGLISH_BOOKS_IDS = [
    "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ",
    "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA",
    "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ",
    "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ",
    "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAL5AwACn_N4VQGCfrTny6GKOgQ",
    "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ",
    "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ"
]

ALL_IN_ONE_BOOK = "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ"

RUSSIAN_MOVIES_IDS = [
    "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE",
    "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ",
    "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ",
    "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE",
    "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ",
    "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ",
    "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ",
    "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE"
]

ENGLISH_MOVIES_IDS = [
    "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ",
    "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ",
    "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ",
    "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ",
    "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ",
    "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ",
    "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ",
    "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ"
]

# --- MENYULAR ---
def get_main_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    menu.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return menu

def get_book_inline():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="books_uz"),
        InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="books_en"),
        InlineKeyboardButton("📚 Hammasi birda", callback_data="books_all"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    return btn

def get_movie_inline():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="movies_uz"),
        InlineKeyboardButton("🇷🇺 Rus tili", callback_data="movies_ru"),
        InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="movies_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    return btn

houses = ["🦁 Gryffindor", "🐍 Slytherin", "🦡 Hufflepuff", "🦅 Ravenclaw"]
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}
HOUSES_FILE = "user_houses.json"

# --- DB FUNKSIYALAR ---
def load_houses():
    if os.path.exists(HOUSES_FILE):
        with open(HOUSES_FILE, "r") as f: return json.load(f)
    return {}

def save_house(user_id, house):
    data = load_houses()
    data[str(user_id)] = house
    with open(HOUSES_FILE, "w") as f: json.dump(data, f)

# --- YORDAMCHI ---
async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        return m_ch.status in ACTIVE_STATUSES, m_gr.status in ACTIVE_STATUSES
    except: return False, False

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        # Obuna xabari (eski mantiq saqlandi)
        btn = InlineKeyboardMarkup(row_width=1)
        if not in_channel: btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
        if not in_group: btn.add(InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"))
        await message.answer("❗ Avval a'zo bo'ling:", reply_markup=btn)
        return
    
    # Username orqali salomlashish (Yangi talab)
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    await message.answer(f"Xush kelibsiz {username}! Menyulardan birini tanlang:", reply_markup=get_main_menu())

@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def books_main(message: types.Message):
    await message.answer("Qaysi tildagi kitoblarni qidiryapsiz?", reply_markup=get_book_inline())

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movies_main(message: types.Message):
    await message.answer("Qaysi tildagi kinolarni ko'rmoqchisiz?", reply_markup=get_movie_inline())

# --- CALLBACKLAR (IDlar bilan ishlash) ---
@dp.callback_query_handler(lambda c: True)
async def process_callbacks(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    
    if callback.data == "back_to_main":
        await callback.message.delete()
        await bot.send_message(user_id, "Asosiy menyu:", reply_markup=get_main_menu())

    elif callback.data == "books_en":
        for fid in ENGLISH_BOOKS_IDS:
            await bot.send_document(user_id, fid)
    
    elif callback.data == "books_all":
        await bot.send_document(user_id, ALL_IN_ONE_BOOK)

    elif callback.data == "movies_ru":
        for fid in RUSSIAN_MOVIES_IDS:
            await bot.send_video(user_id, fid)

    elif callback.data == "movies_en":
        for fid in ENGLISH_MOVIES_IDS:
            await bot.send_video(user_id, fid)

    elif callback.data in ["books_uz", "movies_uz"]:
        await callback.answer("Hozircha bu bo'limda ma'lumot yo'q.", show_alert=True)
    
    await callback.answer()

# --- SHLYAPA (O'zgarmas fakultet) ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def hat_logic(message: types.Message):
    uid = str(message.from_user.id)
    data = load_houses()
    
    if uid in data:
        faculty = data[uid]
        await message.answer(f"Siz allaqachon saralangansiz! Sizning fakultetingiz: **{faculty}**", parse_mode="Markdown")
    else:
        res = random.choice(houses)
        save_house(uid, res)
        await message.answer(f"Shlyapa o'ylab ko'rib, qaror qabul qildi: **{res}**!", parse_mode="Markdown")

# Admin uchun ID olish (Eski funksiya)
@dp.message_handler(content_types=["document", "video"])
async def get_ids(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        fid = message.document.file_id if message.document else message.video.file_id
        await message.reply(f"🔑 file_id: <code>{fid}</code>", parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
