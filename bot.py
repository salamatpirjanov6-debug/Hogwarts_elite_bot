from PIL import Image, ImageDraw, ImageFont
import io
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
    ReplyKeyboardRemove,
)
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7718919427:AAH0p85Lh_XFsc-2n0L8O956T8Xw68Y9NqE")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa"
BOT_USERNAME = "Hogwarts_elite_bot"

WELCOME_IMAGE_BASE = "hogwarts_blank.jpg"
FONT_FILE = "font.ttf"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
USERS_FILE = "bot_users.json"
WELCOME_FILE = "welcome_settings.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f: return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f)

def register_user(user_id):
    users = load_data(USERS_FILE)
    if str(user_id) not in users:
        users[str(user_id)] = True
        save_data(USERS_FILE, users)

# --- TO'G'RILANGAN RASM FUNKSIYASI ---
def create_welcome_image(user_name):
    try:
        if not os.path.exists(WELCOME_IMAGE_BASE): return None
        base_img = Image.open(WELCOME_IMAGE_BASE).convert("RGB")
        draw = ImageDraw.Draw(base_img)
        font_path = os.path.join(os.getcwd(), FONT_FILE)
        
        # O'zbekcha harflar uchun xavfsiz matn
        clean_name = user_name.replace("‘", "'").replace("’", "'").replace("ʻ", "'").replace("`", "'")
        
        try:
            font = ImageFont.truetype(font_path, 48)
        except:
            font = ImageFont.load_default()
            
        # Ism chiziq ustiga tushishi uchun koordinata (Siz yuborgan rasm asosida)
        draw.text((280, 465), clean_name, font=font, fill=(30, 30, 30))
        
        img_byte_arr = io.BytesIO()
        img_byte_arr.name = 'welcome.jpg'
        base_img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        return img_byte_arr
    except Exception as e:
        logging.error(f"Rasmda xato: {e}")
        return None

# --- BARCHA MA'LUMOTLAR RO'YXATI ---
BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE"},
    {"name": "📖 7. Ajal tuhfalari", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA"},
]

BOOKS_EN = [
    {"name": "📖 1. Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ"},
    {"name": "📖 2. Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA"},
    {"name": "📖 3. Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ"},
    {"name": "📖 4. Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ"},
    {"name": "📖 5. Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ"},
    {"name": "📖 6. Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ"},
    {"name": "📖 7. Deathly Hallows", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ"},
]

BOOKS_ALL = [{"name": "📚 All Books (1-7)", "file_id": "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ"}]

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

MOVIES_RU = [
    {"name": "🎬 1. Философский камень", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE"},
    {"name": "🎬 2. Тайная комната", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ"},
    {"name": "🎬 3. Узник Азкабана", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ"},
    {"name": "🎬 4. Кубок огня", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE"},
    {"name": "🎬 5. Орден Феникса", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ"},
    {"name": "🎬 6. Принц-полукровка", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ"},
    {"name": "🎬 7. Дары Смерти 1", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ"},
    {"name": "🎬 8. Дары Смерти 2", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE"},
]

MOVIES_EN = [
    {"name": "🎬 1. Sorcerer's Stone", "file_id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ"},
    {"name": "🎬 2. Chamber of Secrets", "file_id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ"},
    {"name": "🎬 3. Prisoner of Azkaban", "file_id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ"},
    {"name": "🎬 4. Goblet of Fire", "file_id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ"},
    {"name": "🎬 5. Order of the Phoenix", "file_id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ"},
    {"name": "🎬 6. Half-Blood Prince", "file_id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ"},
    {"name": "🎬 7. Deathly Hallows 1", "file_id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ"},
    {"name": "🎬 8. Deathly Hallows 2", "file_id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ"},
]

SORTING_MESSAGES = [
    "🤔 *Hmmm... qiyin, juda qiyin.* \nKo'ryapman, bu yerda aql ham yetarli, iste'dod ham... va-a-ay, qanday ulkan xohish!",
    "🧐 *Iye, bu qanday sirli qalb?* \nAql bovar qilmaydigan jasorat, biroz makr... Ha, sen Hogvarts tarixini o'zgartira olasan!",
    "🦁 *Jasurlik sening qoningda!*"
]

# --- MENYULAR ---
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

houses_dict = {"Slytherin": "ilon", "Hufflepuff": "aql", "Ravenclaw": "burgut", "Gryffindor": "jasorat"}
ACTIVE_STATUSES = {"creator", "administrator", "member", "restricted"}

async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        return m_ch.status in ACTIVE_STATUSES, m_gr.status in ACTIVE_STATUSES
    except: return False, False

# --- HANDLERLAR ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    register_user(message.from_user.id)
    in_ch, in_gr = await check_sub(message.from_user.id)
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1)
        btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
                InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"),
                InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub_status"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo'ling:", reply_markup=btn)
        return
    await message.answer(f"Xush kelibsiz! Bo'limni tanlang:", reply_markup=main_menu())

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_handler(message: types.Message):
    for user in message.new_chat_members:
        user_name = user.first_name
        photo = create_welcome_image(user_name)
        text = f"Xush kelibsiz <a href='tg://user?id={user.id}'>{user_name}</a>!"
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Fakultet tanlash", url=f"https://t.me/{BOT_USERNAME}?start=start"))
        if photo: 
            await bot.send_photo(message.chat.id, photo, caption=text, reply_markup=btn, parse_mode="HTML")
        else: 
            await message.answer(text, reply_markup=btn, parse_mode="HTML")

@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def send_ads(message: types.Message):
    args = message.get_args()
    if not args: return await message.answer("Format: /send matn")
    users = load_data(USERS_FILE)
    count = 0
    for uid in users.keys():
        try:
            await bot.send_message(int(uid), args)
            count += 1
            if count % 25 == 0: await asyncio.sleep(1)
        except: continue
    await message.answer(f"✅ {count} ta foydalanuvchiga yuborildi.")

@dp.message_handler(lambda m: m.text in ["📚 Kitoblar", "🎬 Kinolar", "🎩 Saralovchi shlyapa"])
async def private_menus(message: types.Message):
    if message.text == "📚 Kitoblar":
        await message.answer("Kitoblar tilini tanlang:", reply_markup=book_lang_menu())
    elif message.text == "🎬 Kinolar":
        await message.answer("Kinolar tilini tanlang:", reply_markup=movie_lang_menu())
    elif message.text == "🎩 Saralovchi shlyapa":
        await message.answer("Fakultetingizni aniqlash uchun shlyapa botiga o'ting:", 
                             reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapa bot", url=f"https://t.me/{SHLYAPA_USER}")))

# --- CALLBACKLAR (HAMMASI OCHIQ) ---
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback: types.CallbackQuery):
    uid = callback.message.chat.id
    d = callback.data
    
    if d == "check_sub_status":
        in_ch, in_gr = await check_sub(callback.from_user.id)
        if in_ch and in_gr:
            await callback.message.delete()
            await bot.send_message(uid, "Xush kelibsiz!", reply_markup=main_menu())
        else: await callback.answer("Obuna bo'lmadingiz!", show_alert=True)
        
    elif d == "back_to_main":
        await callback.message.edit_text("Asosiy menyu:", reply_markup=main_menu())

    # KITOOBLAR SECTION
    elif d == "lang_book_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"bk_uz_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kitoblar:", reply_markup=btn)
        
    elif d == "lang_book_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_EN): btn.add(InlineKeyboardButton(b["name"], callback_data=f"bk_en_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇬🇧 English books:", reply_markup=btn)
        
    elif d == "lang_book_all":
        btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(BOOKS_ALL[0]["name"], callback_data="bk_all_0"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("📚 Hammasi birda:", reply_markup=btn)

    # KINOLAR SECTION
    elif d == "lang_movie_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_uz_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kinolar:", reply_markup=btn)
        
    elif d == "lang_movie_ru":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_RU): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_ru_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇷🇺 Ruscha kinolar:", reply_markup=btn)
        
    elif d == "lang_movie_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_EN): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_en_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇬🇧 English movies:", reply_markup=btn)

    # SENDING FILES
    elif d.startswith("bk_"):
        p = d.split("_")
        if p[1] == "uz": await bot.send_document(uid, BOOKS_UZ[int(p[2])]["file_id"])
        elif p[1] == "en": await bot.send_document(uid, BOOKS_EN[int(p[2])]["file_id"])
        elif p[1] == "all": await bot.send_document(uid, BOOKS_ALL[0]["file_id"])
        
    elif d.startswith("mv_"):
        p = d.split("_")
        if p[1] == "uz": await bot.send_video(uid, MOVIES_UZ[int(p[2])]["file_id"])
        elif p[1] == "ru": await bot.send_video(uid, MOVIES_RU[int(p[2])]["file_id"])
        elif p[1] == "en": await bot.send_video(uid, MOVIES_EN[int(p[2])]["file_id"])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
