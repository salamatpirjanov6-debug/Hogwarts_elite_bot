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

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa" # Siz aytgan username

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

MOVIES = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA"},
    {"name": "🎬 2. Maxfiy hujra", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA"},
    {"name": "🎬 3. Azkoban maxbusi", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 4. Alanga kubogi", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
    {"name": "🎬 5. Feniks jamiyati", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA"},
    {"name": "🎬 6. Tilsim Shahzoda", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA"},
    {"name": "🎬 7. Ajal tuhfasi 1-qism", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA"},
    {"name": "🎬 8. Ajal tuhfalari 2-qism", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA"},
]

# Asosiy menyu
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📚 Kitob"), KeyboardButton("🎬 Kino"))
menu.add(KeyboardButton("🎩 Saralovchi shlyapa"))

houses = ["🦁 Gryffindor", "🐍 Slytherin", "🦡 Hufflepuff", "🦅 Ravenclaw"]
HOUSE_KEYWORDS = {
    "🦁 Gryffindor": "qilich",
    "🐍 Slytherin": "ilon",
    "🦡 Hufflepuff": "aql",
    "🦅 Ravenclaw": "burgut",
}
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}

USERS_FILE = "users.json"
HOUSES_FILE = "user_houses.json"

# --- FUNKSIYALAR ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f: return json.load(f)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f: json.dump(users, f)

def load_houses():
    if os.path.exists(HOUSES_FILE):
        with open(HOUSES_FILE, "r") as f: return json.load(f)
    return {}

def save_house(user_id, house):
    data = load_houses()
    data[str(user_id)] = house
    with open(HOUSES_FILE, "w") as f: json.dump(data, f)

def get_user_house(user_id):
    return load_houses().get(str(user_id))

async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        return m_ch.status in ACTIVE_STATUSES, m_gr.status in ACTIVE_STATUSES
    except: return False, False

async def send_not_subscribed(message, in_channel, in_group):
    btn = InlineKeyboardMarkup(row_width=1)
    if not in_channel: btn.add(InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL[1:]}"))
    if not in_group: btn.add(InlineKeyboardButton("👥 Guruhga qo'shilish", url=f"https://t.me/{GROUP[1:]}"))
    await message.answer("❗ Botdan foydalanish uchun quyidagilarga obuna bo'ling:", reply_markup=btn)

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    save_user(message.from_user.id)
    await message.answer(f"🧙‍♂️ Salom! Xush kelibsiz!\nKerakli menyuni tanlang:", reply_markup=menu)

@dp.message_handler(lambda m: m.text == "📚 Kitob")
async def books_menu(message: types.Message):
    btn = InlineKeyboardMarkup(row_width=1)
    for i, b in enumerate(BOOKS):
        btn.add(InlineKeyboardButton(b["name"], callback_data=f"bookuz_{i}"))
    await message.answer("📚 Kitob tanlang:", reply_markup=btn)

@dp.message_handler(lambda m: m.text == "🎬 Kino")
async def movies_menu(message: types.Message):
    btn = InlineKeyboardMarkup(row_width=1)
    for i, m in enumerate(MOVIES):
        btn.add(InlineKeyboardButton(m["name"], callback_data=f"movieuz_{i}"))
    await message.answer("🎬 Kino tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith("bookuz_"))
async def send_book(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    await callback.message.answer_document(BOOKS[idx]["file_id"], caption=BOOKS[idx]["name"])
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("movieuz_"))
async def send_movie(callback: types.CallbackQuery):
    idx = int(callback.data.split("_")[1])
    await callback.message.answer_video(MOVIES[idx]["file_id"], caption=MOVIES[idx]["name"])
    await callback.answer()

# --- SIZ AYTGAN ASOSIY O'ZGARISH ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def hat(message: types.Message):
    in_channel, in_group = await check_sub(message.from_user.id)
    if not in_channel or not in_group:
        await send_not_subscribed(message, in_channel, in_group)
        return
    
    uid = message.from_user.id
    saved = get_user_house(uid)
    
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text="🎩 Shlyapaga yozish", url=f"https://t.me/{SHLYAPA_USER}")
    markup.add(btn)

    if saved:
        kw = HOUSE_KEYWORDS[saved]
        text = (
            f"🎩 <b>Siz allaqachon saralangansiz!</b>\n\n"
            f"Sizning fakultetingiz: {saved}\n"
            f"🔑 Kalit so'zingiz: <code>{kw}</code>\n\n"
            f"Kalit so'zni bosib copy qiling va shlyapaga yuboring!"
        )
    else:
        res = random.choice(houses)
        save_house(uid, res)
        kw = HOUSE_KEYWORDS[res]
        text = (
            f"🎩 <b>Saralovchi shlyapa tanladi:</b> {res}\n"
            f"🔑 Kalit so'z: <code>{kw}</code>\n\n"
            f"Kalit so'zni bosib copy qiling va shlyapaga yuboring!"
        )
    
    await message.answer(text, parse_mode="HTML", reply_markup=markup)

@dp.message_handler(content_types=["document", "video"])
async def get_ids(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        fid = message.document.file_id if message.document else message.video.file_id
        await message.reply(f"🔑 file_id: <code>{fid}</code>", parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
        
