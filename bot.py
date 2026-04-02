import json
import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727

if not API_TOKEN:
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- MA'LUMOTLAR ---
BOOKS = [
    {"name": "📖 1. Garri Potter va Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE"},
    {"name": "📖 2. Garri Potter va Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE"},
    {"name": "📖 3. Garri Potter va Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA"},
    {"name": "📖 4. Garri Potter va Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE"},
    {"name": "📖 5. Garri Potter va Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE"},
    {"name": "📖 6. Garri Potter va Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE"},
    {"name": "📖 7. Garri Potter va Ajal tuhfalari", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA"},
    {"name": "📖 8. Garri Potter va La'natlangan bola (1-qism)", "file_id": "BQACAgEAAxkBAANvacuw28JOcJ8hlcLe8Eq33Lr6FssAAuoAA2FcqEc7oEBDKKT05ToE"},
    {"name": "📖 9. Garri Potter va La'natlangan bola (2-qism)", "file_id": "BQACAgIAAxkBAANxacuxAAE5y-wWgOHjT2_RNea7LkjdAAKsAgACLVkpSLjOwEQYWEw-OgQ"},
]

BOOKS_EN = [
    {"name": "📖 1. Harry Potter and the Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIB6WnM3YhOigII0RaMjZJ_rbPkicpwAAL_AwACn_N4VR4lpjl-n1tZOgQ"},
    {"name": "📖 2. Harry Potter and the Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIB62nM3bq4yhvsHvz0t9cjEPQErxK1AAMEAAKf83hV774CCp3aF146BA"},
    {"name": "📖 3. Harry Potter and the Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIB7WnM3c8fCAkllWeUDg9A6EV62m7wAAL-AwACn_N4Vd-iiVWRVt-DOgQ"},
    {"name": "📖 4. Harry Potter and the Goblet of Fire", "file_id": "BQACAgUAAxkBAAIB72nM3eIgI5zSrNDhIaCUZdGkIoTTAAL7AwACn_N4VdM2NXmcWgR-OgQ"},
    {"name": "📖 5. Harry Potter and the Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIB8WnM3gABmckrvtxpTupJH0L-lcuaWQAC-QMAAp_zeFUBgn6058uhijoE"},
    {"name": "📖 6. Harry Potter and the Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIB82nM3h3geXzhJ5GrfbgtI6ON1eJ4AAL6AwACn_N4VWeuyWoTm2SnOgQ"},
    {"name": "📖 7. Harry Potter and the Deathly Hallows", "file_id": "BQACAgUAAxkBAAIB9WnM3jLrScbUoYxzoQo-lLudYog7AAL8AwACn_N4VdOVKXxjV5MlOgQ"},
]

BOOK_ALL_UZ_FILE_ID = "BQACAgIAAxkBAAIBuWnM173xiulzsDkkFRiIf8L4g_mAAAI0HwACIynpS2_wVwpElnx4OgQ"

MOVIES = [
    {"name": "🎬 1. Hikmatlar toshi (2:32:22)", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA"},
    {"name": "🎬 2. Maxfiy hujra (2:54:25)", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA"},
    {"name": "🎬 3. Azkoban maxbusi (2:21:43)", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 4. Alanga kubogi (2:31:27)", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
    {"name": "🎬 5. Feniks jamiyati (2:18:15)", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 6. Tilsim Shahzoda (2:33:32)", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA"},
    {"name": "🎬 7. Ajal tuhfasi 1-qism (2:26:06)", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA"},
    {"name": "🎬 8. Ajal tuhfalari 2-qism (2:10:28)", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
]

MOVIES_RU = [
    {"name": "🎬 1. Гарри Поттер и Философский камень", "file_id": "BAACAgIAAxkBAAIBvmnM2MMwJoOi8tKP6o8nVkgfp3l2AAIoCgACMf9ZSzgnWyRwYTsZOgQ"},
    {"name": "🎬 2. Гарри Поттер и Тайная комната", "file_id": "BAACAgIAAxkBAAIBwGnM2P43QkFy323mTK2S8pZERA0yAAImCgACMf9ZS8YV5UtV-2QLOgQ"},
    {"name": "🎬 3. Гарри Поттер и Узник Азкабана", "file_id": "BAACAgIAAxkBAAIBwmnM2SyNMO11UJG_LbZx7CWPQbZUAAInCgACMf9ZSxH4i6-D8wN7OgQ"},
    {"name": "🎬 4. Гарри Поттер и Кубок огня", "file_id": "BAACAgIAAxkBAAIBxGnM2U-fBe_RYpJ48-YrmEMECtXYAAIjCgACMf9ZS1Zt8gABJXZpWDoE"},
    {"name": "🎬 5. Гарри Поттер и Орден Феникса", "file_id": "BAACAgQAAxkBAAIBxmnM2XGIgqGS0YoPQZSXNXipEzncAAKgDAAC2L_JULzvFz_NQdPnOgQ"},
    {"name": "🎬 6. Гарри Поттер и Принц-полукровка", "file_id": "BAACAgIAAxkBAAIByGnM2ZnS2ESYT2YIMvnbA5i649jaAAIlCgACMf9ZS2Yi3TnE3abiOgQ"},
    {"name": "🎬 7. Гарри Поттер и Дары смерти. Часть 1", "file_id": "BAACAgIAAxkBAAIBymnM2bf5-fSPitGgisJPQURQN0BKAALpBAACKP2pSAiPJCewUqfUOgQ"},
    {"name": "🎬 8. Гарри Поттер и Дары смерти. Часть 2", "file_id": "BAACAgIAAxkBAAIBzGnM2dUyMVmgoG9FRp6wBIIaA91qAAJlBAACxKyhSM_1_EJMOAM3OgQ"},
]

MOVIES_EN = [
    {"name": "🎬 1. Harry Potter and the Philosopher's Stone", "file_id": "BAACAgQAAxkBAAIBzmnM2prddQGsn_WFum5_buhTq-K9AAJ_BwACrMaBUKRYUpDTm11oOgQ"},
    {"name": "🎬 2. Harry Potter and the Chamber of Secrets", "file_id": "BAACAgQAAxkBAAIB0GnM2rUafxltSMIOBOtLoPakjKM5AAKBBwACrMaBUM7959H4o01HOgQ"},
    {"name": "🎬 3. Harry Potter and the Prisoner of Azkaban", "file_id": "BAACAgQAAxkBAAIB0mnM2s0KamW9mD3wPNkGJt8qCjG2AAKHBwACrMaBUKP9MbVImI-uOgQ"},
    {"name": "🎬 4. Harry Potter and the Goblet of Fire", "file_id": "BAACAgQAAxkBAAIB1GnM2uGTCLbxz9w6sFvWwFHa_ax9AAKOBwACrMaBUNmv6Ega62iuOgQ"},
    {"name": "🎬 5. Harry Potter and the Order of the Phoenix", "file_id": "BAACAgQAAxkBAAIB1mnM2vO5FIB92X4figABr9BcQkSNiwAClQcAAqzGgVAu4jUB_j0KJDoE"},
    {"name": "🎬 6. Harry Potter and the Half-Blood Prince", "file_id": "BAACAgQAAxkBAAIB2GnM2w88YrYj8vTx63DKvjrTPqfhAAKNCAACqwKBUHgSmGHyOYgROgQ"},
    {"name": "🎬 7. Harry Potter and the Deathly Hallows Part 1", "file_id": "BAACAgQAAxkBAAIB2mnM2yJGuJ7O4wR5AtgZETHdqZFWAAKXCAACqwKBUMiAIxlbsJmOOgQ"},
    {"name": "🎬 8. Harry Potter and the Deathly Hallows Part 2", "file_id": "BAACAgQAAxkBAAIB3GnM2zY1caRIbVzD1WtN5O4zKYoFAAKkCAACqwKBUC733-s2FjB3OgQ"},
]

# --- SOZLAMALAR ---
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📚 Kitob"), KeyboardButton("🎬 Kino"))
menu.add(KeyboardButton("🎩 Saralovchi shlyapa"))

houses = ["🦁 Gryffindor", "🐍 Slytherin", "🦡 Hufflepuff", "🦅 Ravenclaw"]
HOUSE_KEYWORDS = {
    "🦁 Gryffindor": "qilich",
    "🐍 Slytherin": "ilon",
    "🦡 Hufflepuff": "aqil",
    "🦅 Ravenclaw": "burgut",
}
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}

USERS_FILE = "users.json"
HOUSES_FILE = "user_houses.json"

# --- FUNKSIYALAR ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

def get_all_users():
    return load_users()

def load_houses():
    if os.path.exists(HOUSES_FILE):
        with open(HOUSES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_house(user_id, house):
    data = load_houses()
    data[str(user_id)] = house
    with open(HOUSES_FILE, "w") as f:
        json.dump(data, f)

def get_user_house(user_id):
    return load_houses().get(str(user_id))

async def check_sub(user_id):
    try:
        member_ch = await bot.get_chat_member(CHANNEL, user_id)
        in_channel = member_ch.status in ACTIVE_STATUSES
    except:
        in_channel = False
    try:
        member_gr = await bot.get_chat_member(GROUP, user_id)
        in_group = member_gr.status in ACTIVE_STATUSES
    except:
        in_group = False
    return in_channel, in_group

async def send_not_subscribed(message, in_channel, in_group):
    btn = InlineKeyboardMarkup(row_width=1)
    text = "❗ Botdan foydalanish uchun quyidagilarga obuna bo'ling:\n"
    if not in_channel:
        btn.add(InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL[1:]}"))
    if not in_group:
        btn.add(InlineKeyboardButton("👥 Guruhga qo'shilish", url=f"https://t.me/{GROUP[1:]}"))
    await message.answer(text, reply_markup=btn)

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        await message.reply("🤖 Men ishlayapman! /hat buyrug'ini yozing.")
        return
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    save_user(message.from_user.id)
    name = message.from_user.first_name or "Sehrgar"
    await message.answer(f"🧙‍♂️ Salom, {name}! Xush kelibsiz!\nKerakli menyuni tanlang:", reply_markup=menu)

@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    count = len(get_all_users())
    await message.answer(f"🛡 Admin panel\n\n👥 Foydalanuvchilar: {count}", parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "📚 Kitob")
async def books_menu(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="book_lang_uz"),
            InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="book_lang_en"))
    btn.add(InlineKeyboardButton("📦 Hammasi birda", callback_data="book_all_uz"))
    await message.answer("📚 Kitob tilini tanlang:", reply_markup=btn)

@dp.message_handler(lambda m: m.text == "🎬 Kino")
async def movies_menu(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="movie_lang_uz"),
            InlineKeyboardButton("🇷🇺 Rus tili", callback_data="movie_lang_ru"))
    btn.add(InlineKeyboardButton("🇬🇧 Ingliz tili", callback_data="movie_lang_en"))
    await message.answer("🎬 Kino tilini tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == "book_lang_uz")
async def books_list_uz(callback: types.CallbackQuery):
    btn = InlineKeyboardMarkup(row_width=1)
    for i, b in enumerate(BOOKS):
        btn.add(InlineKeyboardButton(b["name"], callback_data=f"bookuz_{i}"))
    await callback.message.edit_text("📚 Kitob tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == "movie_lang_uz")
async def movies_list_uz(callback: types.CallbackQuery):
    btn = InlineKeyboardMarkup(row_width=1)
    for i, m in enumerate(MOVIES):
        btn.add(InlineKeyboardButton(m["name"], callback_data=f"movieuz_{i}"))
    await callback.message.edit_text("🎬 Kino tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith("bookuz_"))
async def send_book_uz(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    b = BOOKS[idx]
    await callback.message.answer_document(b["file_id"], caption=b["name"])
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("movieuz_"))
async def send_movie_uz(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    m = MOVIES[idx]
    await callback.message.answer_video(m["file_id"], caption=m["name"])
    await callback.answer()

@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def hat(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    uid = message.from_user.id
    saved = get_user_house(uid)
    if saved:
        kw = HOUSE_KEYWORDS[saved]
        await message.answer(f"🎩 Fakultetingiz: {saved}\n🔑 Kalit so'z: {kw}")
    else:
        res = random.choice(houses)
        save_house(uid, res)
        kw = HOUSE_KEYWORDS[res]
        await message.answer(f"🎩 Saralovchi shlyapa tanladi: {res}\n🔑 Kalit so'z: {kw}")

@dp.message_handler(commands=["hat"])
async def hat_group(message: types.Message):
    uid = message.from_user.id
    saved = get_user_house(uid)
    if saved:
        await message.reply(f"🎩 Fakultet: {saved}")
    else:
        res = random.choice(houses)
        save_house(uid, res)
        await message.reply(f"🎩 Tanlandi: {res}")

@dp.message_handler(content_types=["document", "video"])
async def get_ids(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    fid = message.document.file_id if message.document else message.video.file_id
    await message.reply(f"🔑 file_id:\n<code>{fid}</code>", parse_mode="HTML")

async def on_startup(_):
    await bot.set_my_commands([BotCommand("start", "Botni ishga tushirish")])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
