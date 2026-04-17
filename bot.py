import json
import logging
import os
import random
import asyncio
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
    ChatPermissions
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ==========================================
# ⚙️ SOZLAMALAR VA KONFIGURATSIYA
# ==========================================
# Yangi token muvaffaqiyatli o'rnatildi
API_TOKEN = "8754136836:AAE10PBmNVqEYlJqb8gPxqzHey445m0lBKw"
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7821230725
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# --- ADMIN HOLATLARI ---
class AdminStates(StatesGroup):
    waiting_for_ad = State()
    waiting_for_welcome = State()
    waiting_for_getid = State()

# --- MA'LUMOTLAR BAZASI FAYLLARI ---
FILES = {
    "houses": "user_houses.json",
    "users": "users_list.json",
    "welcome": "welcome_settings.json",
    "banned": "banned_users.json"
}

def load_data(key):
    file = FILES[key]
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_data(key, data):
    with open(FILES[key], "w", encoding="utf-8") as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)

# ==========================================
# 📚 KITOBLAR BAZASI (TO'LIQ)
# ==========================================
BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE", "caption": "📚 <b>Garri Potter va Falsafiy tosh</b>\n\nGarri o'zining sehrgar ekanligini bilib oladi va Hogwartsga yo'l oladi.\n\n#kitob #uzbek #falsafiy_tosh\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE", "caption": "📚 <b>Garri Potter va Maxfiy hujra</b>\n\nHogwartsda dahshatli maxluq paydo bo'ldi. Sirlar ochilishi kerak.\n\n#kitob #uzbek #maxfiy_hujra\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA", "caption": "📚 <b>Garri Potter va Azkaban mahbusi</b>\n\nSirius Black qamoqdan qochdi. Garri o'tmishi haqida yangi haqiqatlarni bilib oladi.\n\n#kitob #uzbek #azkaban\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE", "caption": "📚 <b>Garri Potter va Otashli jom</b>\n\nUch sehrgar turniri va Qora lordning qaytishi.\n\n#kitob #uzbek #otashli_jom\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE", "caption": "📚 <b>Garri Potter va Kaknus ordeni</b>\n\nDambldor armiyasi tuziladi va vazirlik bilan kurash boshlanadi.\n\n#kitob #uzbek #kaknus_ordeni\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE", "caption": "📚 <b>Garri Potter va Chalazot shahzoda</b>\n\nLord Voldemortning o'tmishi va xo'rjuinlarning siri.\n\n#kitob #uzbek #shahzoda\n⚡️ @harry_potter_fans_uz"},
    {"name": "📖 7. Ajal tuhfalari 1", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA", "caption": "📚 <b>Garri Potter va Ajal tuhfalari</b>\n\nSo'nggi kurash boshlanmoqda. Do'stlar xavfli sayohatda.\n\n#kitob #uzbek #ajal_tuhfalari\n⚡️ @harry_potter_fans_uz"}
]

BOOKS_EN = [
    {"name": "📖 1. Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ", "caption": "📚 <b>Harry Potter and the Philosopher's Stone</b>\n\nLanguage: English 🇬🇧\nThe boy who lived begins his journey.\n\n#books #english #HP1\n✨ @harry_potter_fans_uz"},
    {"name": "📖 2. Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA", "caption": "📚 <b>Harry Potter and the Chamber of Secrets</b>\n\nLanguage: English 🇬🇧\nSomething is attacking students in Hogwarts.\n\n#books #english #HP2\n✨ @harry_potter_fans_uz"},
    {"name": "📖 3. Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ", "caption": "📚 <b>Harry Potter and the Prisoner of Azkaban</b>\n\nLanguage: English 🇬🇧\nA dangerous prisoner escaped from Azkaban.\n\n#books #english #HP3\n✨ @harry_potter_fans_uz"},
    {"name": "📖 4. Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ", "caption": "📚 <b>Harry Potter and the Goblet of Fire</b>\n\nLanguage: English 🇬🇧\nThe Triwizard Tournament is here.\n\n#books #english #HP4\n✨ @harry_potter_fans_uz"},
    {"name": "📖 5. Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ", "caption": "📚 <b>Harry Potter and the Order of the Phoenix</b>\n\nLanguage: English 🇬🇧\nDark times have arrived.\n\n#books #english #HP5\n✨ @harry_potter_fans_uz"},
    {"name": "📖 6. Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ", "caption": "📚 <b>Harry Potter and the Half-Blood Prince</b>\n\nLanguage: English 🇬🇧\nSecrets of the past and the future.\n\n#books #english #HP6\n✨ @harry_potter_fans_uz"},
    {"name": "📖 7. Deathly Hallows", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📚 <b>Harry Potter and the Deathly Hallows</b>\n\nLanguage: English 🇬🇧\nThe final hunt for Horcruxes.\n\n#books #english #HP7\n✨ @harry_potter_fans_uz"}
]

# ==========================================
# 🎬 KINOLAR BAZASI (TO'LIQ)
# ==========================================
MOVIES_RU = [
    {"name": "🎬 1. Философский камень", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE", "caption": "🎬 <b>Гарри Поттер 1: Философский камень</b>\n\nЯзык: Русский 🇷🇺\nКачество: HD\n\n#кино #гаррипоттер #HP1\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 2. Тайная комната", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ", "caption": "🎬 <b>Гарри Поттер 2: Тайная комната</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP2\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 3. Узник Азкабана", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ", "caption": "🎬 <b>Гарри Поттер 3: Узник Азкабана</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP3\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 4. Кубок огня", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE", "caption": "🎬 <b>Гарри Поттер 4: Кубок огня</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP4\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 5. Орден Феникса", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ", "caption": "🎬 <b>Гарри Поттер 5: Орден Феникса</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP5\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 6. Принц-полукровка", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ", "caption": "🎬 <b>Гарри Поттер 6: Принц-полукровка</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP6\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 7. Дары Смерти 1", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ", "caption": "🎬 <b>Гарри Поттер 7: Дары Смерти 1</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP7\n🎬 @harry_potter_fans_uz"},
    {"name": "🎬 8. Дары Смерти 2", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE", "caption": "🎬 <b>Гарри Поттер 8: Дары Смерти 2</b>\n\nЯзык: Русский 🇷🇺\n\n#кино #HP8\n🎬 @harry_potter_fans_uz"}
]

MOVIES_UZ = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA", "caption": "🎬 <b>Гарri Potter 1: Hikmatlar toshi</b>\n\nTil: O'zbekcha 🇺🇿\n\n#kino #uzbek #HP1\n🎬 @harry_potter_fans_uz"}
]

# ==========================================
# 🎩 SARALOVCHI SHLYAPA FRAZALARI
# ==========================================
HOUSES_DETAILS = {
    "Gryffindor": {
        "emoji": "🦁", "kalit": "jasorat",
        "txt": "🦁 <b>Yuraging to'la qo'rqmaslik!</b>\n\nMen sendagi cheksiz jasoratni ko'ryapman. Sen do'stlaring uchun olovga ham kirasan. Jasurlik sening qoningda bor. Sening manziling jasurlar makoni — Gryffindor!"
    },
    "Slytherin": {
        "emoji": "🐍", "kalit": "ilon",
        "txt": "🐍 <b>Makr va buyuklikka intilish!</b>\n\nSen aqlli, uddaburon va maqsading yo'lida hech narsadan qaytmaysan. Sening o'tkir aqling va strategik fikrlashing seni buyuklikka yetaklaydi. Manziling — Slytherin!"
    },
    "Hufflepuff": {
        "emoji": "🦡", "kalit": "aql",
        "txt": "🦡 <b>Sadoqat va halol mehnat!</b>\n\nSen juda sadoqatli, sabrli va mehnatkashsan. Sendagi samimiylik hamma narsadan ustun. Sening qadrdonlaring — Hufflepuffda kutmoqda!"
    },
    "Ravenclaw": {
        "emoji": "🦅", "kalit": "burgut",
        "txt": "🦅 <b>O'tkir zehn va donolik!</b>\n\nBilimga chanqoqlik, mantiqiy fikrlash va har qanday jumboqning yechimini topish — sening uslubing. Dunyoni aqling bilan zabt etasan. Sening uying — Ravenclaw!"
    }
}

# --- YORDAMCHI FUNKSIYALAR ---
def get_mention(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        valid = ['member', 'administrator', 'creator']
        return (m_ch.status in valid) and (m_gr.status in valid)
    except: return False

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

async def delete_after_delay(message: types.Message, delay: int):
    await asyncio.sleep(delay)
    try: await message.delete()
    except: pass

# ==========================================
# 🛑 ADMIN VA BAN TIZIMI
# ==========================================

@dp.message_handler(lambda m: str(m.from_user.id) in load_data("banned"))
async def is_banned(m: types.Message): return

@dp.message_handler(commands=["admins"], user_id=ADMIN_ID)
async def admin_panel(message: types.Message):
    txt = ("🧙‍♂️ <b>Hogwarts Admin Paneli:</b>\n\n"
           "🔸 /send - Reklama (barchaga yuborish)\n"
           "🔸 /getid - Media (fayl, rasm, video) ID sini olish\n"
           "🔸 /setwelcome - Guruhda kutib olishni sozlash\n"
           "🔸 /ban [ID] - Foydalanuvchini bloklash")
    await message.answer(txt)

@dp.message_handler(commands=["getid"], user_id=ADMIN_ID)
async def get_id_cmd(message: types.Message):
    await message.reply("📸 Media (rasm, video yoki fayl) yuboring, men uning ID sini beraman:")
    await AdminStates.waiting_for_getid.set()

@dp.message_handler(state=AdminStates.waiting_for_getid, content_types=types.ContentTypes.ANY)
async def get_id_res(message: types.Message, state: FSMContext):
    fid = "Noma'lum"
    if message.photo: fid = message.photo[-1].file_id
    elif message.video: fid = message.video.file_id
    elif message.document: fid = message.document.file_id
    elif message.audio: fid = message.audio.file_id
    await message.reply(f"📁 <b>File ID:</b>\n<code>{fid}</code>")
    await state.finish()

@dp.message_handler(commands=["ban"], user_id=ADMIN_ID)
async def ban_cmd(message: types.Message):
    uid = message.get_args()
    if uid:
        bans = load_data("banned")
        bans[uid] = True
        save_data("banned", bans)
        await message.reply(f"🚫 Foydalanuvchi (ID: {uid}) botdan butunlay haydaldi!")
    else:
        await message.reply("ID ni yozing. Masalan: /ban 1234567")

@dp.message_handler(commands=["setwelcome"], user_id=ADMIN_ID)
async def set_welcome(message: types.Message):
    await message.reply("Guruhga yangi kelganlarni qanday kutib olay? Rasm yoki Video yuboring va captioniga matn yozing.\nIsm o'rniga <b>{name}</b> deb yozing.")
    await AdminStates.waiting_for_welcome.set()

@dp.message_handler(state=AdminStates.waiting_for_welcome, content_types=types.ContentTypes.ANY)
async def welcome_res(message: types.Message, state: FSMContext):
    data = load_data("welcome")
    ftype = "photo" if message.photo else "video" if message.video else "text"
    fid = message.photo[-1].file_id if message.photo else message.video.file_id if message.video else None
    data[str(message.chat.id)] = {"f_id": fid, "f_type": ftype, "text": message.caption or message.text}
    save_data("welcome", data)
    await message.reply("✅ Ushbu guruh uchun kutib olish xabari muvaffaqiyatli saqlandi!")
    await state.finish()

@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def send_ads(message: types.Message):
    await message.reply("Reklama xabarini yuboring (xohlagan formatda):")
    await AdminStates.waiting_for_ad.set()

@dp.message_handler(state=AdminStates.waiting_for_ad, content_types=types.ContentTypes.ANY)
async def ad_proc(message: types.Message, state: FSMContext):
    users = load_data("users")
    c = 0
    for u in users:
        try:
            await message.copy_to(u)
            c += 1
            await asyncio.sleep(0.05)
        except: pass
    await message.answer(f"✅ Reklama {c} ta foydalanuvchiga yuborildi.")
    await state.finish()

# ==========================================
# 🧙‍♂️ ASOSIY FOYDALANUVCHI INTERFEYSI
# ==========================================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    users = load_data("users")
    users[str(message.from_user.id)] = message.from_user.first_name
    save_data("users", users)
    
    if not await check_sub(message.from_user.id):
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
            InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="recheck_sub")
        )
        return await message.answer(f"Salom {get_mention(message.from_user)}!\nHogwartsga kirish uchun avval kanal va guruhimizga a'zo bo'ling.", reply_markup=btn)
    
    await message.answer(f"Salom {get_mention(message.from_user)}! Siz allaqachon Hogwarts talabasisiz. Nima qilamiz?", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "recheck_sub")
async def recheck(c: types.CallbackQuery):
    if await check_sub(c.from_user.id):
        await c.message.delete()
        await bot.send_message(c.message.chat.id, "Tabriklayman! Endi botdan foydalanishingiz mumkin.", reply_markup=main_menu())
    else: 
        await c.answer("Hali a'zo emassiz! Iltimos, kanalga kiring.", show_alert=True)

# --- MEDIA HANDLERS ---
@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def books_main(m: types.Message):
    btn = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("📚 Barcha qismlar (1-7)", callback_data="get_all_books"),
        InlineKeyboardButton("🇺🇿 O'zbekcha kitoblar", callback_data="b_uz"),
        InlineKeyboardButton("🇬🇧 Inglizcha kitoblar", callback_data="b_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="home")
    )
    await m.answer("Qaysi tildagi kitoblarni qidiryapsiz?", reply_markup=btn)

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movies_main(m: types.Message):
    btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="m_uz"),
        InlineKeyboardButton("🇷🇺 Ruscha", callback_data="m_ru"),
        InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="m_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="home")
    )
    await m.answer("Qaysi tildagi filmlarni tomosha qilasiz?", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith(("b_", "m_", "home", "get_")))
async def media_process(c: types.CallbackQuery):
    if c.data == "home":
        await c.message.delete()
        return await bot.send_message(c.message.chat.id, "Asosiy menyuga qaytdik:", reply_markup=main_menu())
    
    if c.data == "get_all_books":
        await bot.send_document(c.message.chat.id, "BQACAgIAAxkBAAIDvWnOr_Z5zZ9Xj_vOL8p9R-Z8o8aLAAIqAAIx_1lLYm3f_zJ7z5M6BA", caption="📚 <b>Barcha qismlar jamlanmasi!</b>\n\n📢 @harry_potter_fans_uz")
        return await c.answer()

    btn = InlineKeyboardMarkup(row_width=1)
    d = c.data
    
    # Kitoblar ro'yxati
    if d == "b_uz":
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"get_buz_{i}"))
    elif d == "b_en":
        for i, b in enumerate(BOOKS_EN): btn.add(InlineKeyboardButton(b["name"], callback_data=f"get_ben_{i}"))
    # Kinolar ro'yxati
    elif d == "m_ru":
        for i, m in enumerate(MOVIES_RU): btn.add(InlineKeyboardButton(m["name"], callback_data=f"get_mru_{i}"))
    elif d == "m_uz":
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"get_muz_{i}"))

    btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="home"))
    
    if not d.startswith("get_"):
        await c.message.edit_text("Kerakli qismni tanlang:", reply_markup=btn)
    else:
        # Fayl yuborish
        parts = d.split("_")
        code, idx = parts[1], int(parts[2])
        if code == "buz": item = BOOKS_UZ[idx]; f = bot.send_document
        elif code == "ben": item = BOOKS_EN[idx]; f = bot.send_document
        elif code == "mru": item = MOVIES_RU[idx]; f = bot.send_video
        elif code == "muz": item = MOVIES_UZ[idx]; f = bot.send_video
        
        await f(c.message.chat.id, item["file_id"], caption=item["caption"])
        await c.answer("Yuborildi!")

# ==========================================
# 🎩 SHLYAPA VA GURUH INTERAKTIVLARI
# ==========================================

@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def hat_handler(m: types.Message):
    data = load_data("houses")
    uid = str(m.from_user.id)
    if uid not in data: 
        data[uid] = random.choice(list(HOUSES_DETAILS.keys()))
        save_data("houses", data)
    
    h = HOUSES_DETAILS[data[uid]]
    msg = await m.answer("🧐 <b>Shlyapa sizning xarakteringizni o'rganmoqda...</b>")
    await asyncio.sleep(2.5)
    
    txt = f"{h['txt']}\n\n<b>Fakultet:</b> {h['emoji']} <b>{data[uid]}</b>\n<b>Xususiyat:</b> <code>{h['kalit']}</code>"
    await msg.edit_text(txt, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🎓 Guruhga kirish", url=f"https://t.me/{SHLYAPA_USER}")))

@dp.message_handler(commands=["mute"])
async def mute_user(m: types.Message):
    if not (await m.chat.get_member(m.from_user.id)).is_chat_admin(): return
    if m.reply_to_message:
        await m.chat.restrict(m.reply_to_message.from_user.id, permissions=ChatPermissions(can_send_messages=False), until_date=int(time.time())+300)
        await m.answer(f"🙊 {get_mention(m.reply_to_message.from_user)} haddidan oshgani uchun 5 daqiqaga sehrlandi (mute).")

# --- KUTIB OLISH (WELCOME) ---
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_bot(m: types.Message):
    w = load_data("welcome").get(str(m.chat.id))
    if w:
        for u in m.new_chat_members:
            cap = w['text'].replace("{name}", get_mention(u))
            btn = InlineKeyboardMarkup().add(InlineKeyboardButton("📢 Rasmiy Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
            
            if w['f_type'] == "photo": res = await bot.send_photo(m.chat.id, w['f_id'], caption=cap, reply_markup=btn)
            elif w['f_type'] == "video": res = await bot.send_video(m.chat.id, w['f_id'], caption=cap, reply_markup=btn)
            else: res = await bot.send_message(m.chat.id, cap, reply_markup=btn)
            
            # Xabarni 10 daqiqadan keyin o'chirish
            asyncio.create_task(delete_after_delay(res, 600))

# ==========================================
# 🚀 ISHGA TUSHIRISH
# ==========================================
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
