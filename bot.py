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
from aiogram.utils import exceptions

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7718919427:AAH0p85Lh_XFsc-2n0L8O956T8Xw68Y9NqE")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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

# --- 1. KITOOBLAR BAZASI (HECH NIMA O'CHIRILMADI) ---
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

BOOKS_ALL = [
    {"name": "📚 All Books (1-7)", "file_id": "BQACAgIAAxkBAAIDR2nOlaH2TdI0xcdn3sg8xJkeqLBIAAI0HwACIynpS2_wVwpElnx4OgQ"}
]

# --- 2. KINOLAR BAZASI (TO'LIQ) ---
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

# --- SHLYAPA GAPLARI (TO'LIQ) ---
SORTING_MESSAGES = [
    "🤔 *Hmmm... qiyin, juda qiyin.* \nKo'ryapman, bu yerda aql ham yetarli, iste'dod ham... va-a-ay, qanday ulkan xohish!",
    "🧐 *Iye, bu qanday sirli qalb?* \nAql bovar qilmaydigan jasorat, biroz makr... Ha, sen Hogvarts tarixini o'zgartira olasan!",
    "💭 *E-eh, men ko'ryapman...* \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan.",
    "🐍 *Qiziq, juda qiziq...* \nShon-shuhratga bo'lgan chanqoqlik, aqlli munosabat. Ha, sen buyuklikka loyiqsan!",
    "🦁 *Bu yerda nima bor?* \nYuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Ha, jasurlik sening qoningda!"
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

# --- 1-DETAL: GURUHDA STARTNI CHEKLASH ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    if message.chat.type != 'private':
        btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🤖 Botga o'tish", url=f"https://t.me/{bot.username}?start=true"))
        await message.reply("Assalomu alaykum! Kitoblar va kinolarni ko'rish uchun shaxsiy chatga o'ting.", reply_markup=btn)
        return

    register_user(message.from_user.id)
    in_ch, in_gr = await check_sub(message.from_user.id)
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1)
        if not in_ch: btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
        if not in_gr: btn.add(InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"))
        btn.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub_status"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo'ling:", reply_markup=btn)
        return
    await message.answer(f"Xush kelibsiz {message.from_user.first_name}! Bo'limni tanlang:", reply_markup=main_menu())

# --- 2-DETAL: SETWELCOME BUYRUG'I ---
@dp.message_handler(commands=["setwelcome"], user_id=ADMIN_ID)
async def set_welcome(message: types.Message):
    text = message.get_args()
    if not text:
        await message.reply("Foydalanish: `/setwelcome Salom {name}, xush kelibsiz!`\n\n*(Eslatma: {name} o'rniga foydalanuvchi ismi chiqadi)*", parse_mode="Markdown")
        return
    
    settings = load_data(WELCOME_FILE)
    settings[str(message.chat.id)] = text
    save_data(WELCOME_FILE, settings)
    await message.reply("✅ Kutib olish matni saqlandi.")

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: types.Message):
    settings = load_data(WELCOME_FILE)
    welcome_text = settings.get(str(message.chat.id), "Xush kelibsiz!")
    
    for user in message.new_chat_members:
        text = welcome_text.replace("{name}", user.first_name)
        await message.answer(text)

# --- REKLAMA YUBORISH (ASL HOLI) ---
@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def send_ads(message: types.Message):
    text = message.get_args()
    reply = message.reply_to_message
    if not text and not reply:
        await message.reply("Foydalanish: `/send xabar_matni` yoki reply qilib `/send` yozing.")
        return
    
    users = load_data(USERS_FILE)
    u_list = list(users.keys())
    total = len(u_list)
    status_msg = await message.answer(f"🚀 {total} ta foydalanuvchiga yuborish boshlandi...")
    
    count, blocked, errors = 0, 0, 0
    for uid in u_list:
        try:
            if reply: await reply.copy_to(int(uid))
            else: await bot.send_message(int(uid), text)
            count += 1
            if count % 10 == 0: await asyncio.sleep(1.5)
        except exceptions.BotBlocked: blocked += 1
        except Exception: errors += 1
            
    await status_msg.edit_text(f"✅ Yakunlandi!\n\nJami: {total}\nYetkazildi: {count}\nBlokladi: {blocked}\nXatoliklar: {errors}")

@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_menu_btn(message: types.Message):
    if message.chat.type != 'private': return
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    await message.answer("Kitoblar uchun tilni tanlang:", reply_markup=book_lang_menu())

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movie_menu_btn(message: types.Message):
    if message.chat.type != 'private': return
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    await message.answer("Kinolar uchun tilni tanlang:", reply_markup=movie_lang_menu())

@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    if message.chat.type != 'private': return
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    uid = str(message.from_user.id)
    data = load_data(HOUSES_FILE)
    intro_text = random.choice(SORTING_MESSAGES)
    if uid not in data:
        fname = random.choice(list(houses_dict.keys()))
        data[uid] = fname
        save_data(HOUSES_FILE, data)
    fname = data[uid]
    key_word = houses_dict[fname]
    house_emojis = {"Slytherin": "🐍", "Hufflepuff": "🦡", "Ravenclaw": "🦅", "Gryffindor": "🦁"}
    h_emoji = house_emojis[fname]
    text = (f"{intro_text}\n\n✨ Hamma narsa ayon! ✨\n\nSizning fakultetingiz: {h_emoji} **{fname}** {h_emoji}\n\n"
            f"🔑 Kalit so'zi: `{key_word}`\n\n*(Nusxa olish uchun ustiga bosing)*\nKalit so'zni shlyapaga yuboring 👇")
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapa bilan bog'lanish", url=f"https://t.me/{SHLYAPA_USER}"))
    await message.answer(text, reply_markup=btn, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback: types.CallbackQuery):
    uid = callback.message.chat.id
    user_name = callback.from_user.first_name
    
    if callback.data == "check_sub_status":
        in_ch, in_gr = await check_sub(callback.from_user.id)
        if in_ch and in_gr:
            await callback.message.delete()
            await bot.send_message(uid, f"Tabriklaymiz {user_name}, botdan foydalanishingiz mumkin. 🎉", reply_markup=main_menu())
        else: await callback.answer("Obuna bo'lmagansiz!", show_alert=True)

    elif callback.data == "back_to_main":
        await callback.message.delete()
        await bot.send_message(uid, "Asosiy menyu:", reply_markup=main_menu())

    elif callback.data == "lang_book_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"bk_uz_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kitoblar:", reply_markup=btn)

    elif callback.data == "lang_book_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_EN): btn.add(InlineKeyboardButton(b["name"], callback_data=f"bk_en_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇬🇧 English Books:", reply_markup=btn)

    elif callback.data == "lang_book_all":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_ALL): btn.add(InlineKeyboardButton(b["name"], callback_data=f"bk_all_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("📚 Hammasi birda:", reply_markup=btn)

    elif callback.data == "lang_movie_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_uz_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kinolar:", reply_markup=btn)

    elif callback.data == "lang_movie_ru":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_RU): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_ru_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇷🇺 Русские фильмы:", reply_markup=btn)

    elif callback.data == "lang_movie_en":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_EN): btn.add(InlineKeyboardButton(m["name"], callback_data=f"mv_en_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇬🇧 English Movies:", reply_markup=btn)

    elif callback.data.startswith("bk_"):
        parts = callback.data.split("_")
        lang, idx = parts[1], int(parts[2])
        if lang == "uz": await bot.send_document(uid, BOOKS_UZ[idx]["file_id"], caption=BOOKS_UZ[idx]["name"])
        elif lang == "en": await bot.send_document(uid, BOOKS_EN[idx]["file_id"], caption=BOOKS_EN[idx]["name"])
        elif lang == "all": await bot.send_document(uid, BOOKS_ALL[idx]["file_id"], caption=BOOKS_ALL[idx]["name"])

    elif callback.data.startswith("mv_"):
        parts = callback.data.split("_")
        lang, idx = parts[1], int(parts[2])
        if lang == "uz": await bot.send_video(uid, MOVIES_UZ[idx]["file_id"], caption=MOVIES_UZ[idx]["name"])
        elif lang == "ru": await bot.send_video(uid, MOVIES_RU[idx]["file_id"], caption=MOVIES_RU[idx]["name"])
        elif lang == "en": await bot.send_video(uid, MOVIES_EN[idx]["file_id"], caption=MOVIES_EN[idx]["name"])

    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
