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
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# --- SOZLAMALAR ---
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7718919427:AAH0p85L_XFsc-2n0L8O956T8Xw68Y9NqE")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class AdminStates(StatesGroup):
    waiting_for_file = State()

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
WELCOME_FILE = "welcome_settings.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

# --- MA'LUMOTLAR BAZASI (KITOBLAR) ---
BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE", "caption": "📖 Nomi: Garri Potter va Falsafiy tosh\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE", "caption": "📖 Nomi: Garri Potter va Maxfiy hujra\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA", "caption": "📖 Nomi: Garri Potter va Azkaban mahbusi\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE", "caption": "📖 Nomi: Garri Potter va Otashli jom\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE", "caption": "📖 Nomi: Garri Potter va Kaknus ordeni\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE", "caption": "📖 Nomi: Garri Potter va Chalazot shahzoda\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 7. Ajal tuhfalari 1", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA", "caption": "📖 Nomi: Garri Potter va Ajal tuhfalari 1\n\nKanal: @harry_potter_fans_uz"},
    {"name": "📖 8. Ajal tuhfalari 2", "file_id": "BQACAgIAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Nomi: Garri Potter va Ajal tuhfalari 2\n\nKanal: @harry_potter_fans_uz"},
]

BOOKS_EN = [
    {"name": "📖 1. Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ", "caption": "📖 Name: Harry Potter 1\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 2. Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA", "caption": "📖 Name: Harry Potter 2\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 3. Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ", "caption": "📖 Name: Harry Potter 3\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 4. Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ", "caption": "📖 Name: Harry Potter 4\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 5. Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ", "caption": "📖 Name: Harry Potter 5\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 6. Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ", "caption": "📖 Name: Harry Potter 6\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 7. Deathly Hallows 1", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Name: Harry Potter 7\n\nChannel: @harry_potter_fans_uz"},
    {"name": "📖 8. Deathly Hallows 2", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Name: Harry Potter 8\n\nChannel: @harry_potter_fans_uz"},
]

# --- MA'LUMOTLAR BAZASI (KINOLAR) ---
MOVIES_UZ = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA", "caption": "🎬 HP 1: Hikmatlar toshi\n@harry_potter_fans_uz"},
    {"name": "🎬 2. Maxfiy hujra", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA", "caption": "🎬 HP 2: Maxfiy hujra\n@harry_potter_fans_uz"},
    {"name": "🎬 3. Azkoban maxbusi", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "🎬 HP 3: Azkoban maxbusi\n@harry_potter_fans_uz"},
    {"name": "🎬 4. Alanga kubogi", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "🎬 HP 4: Alanga kubogi\n@harry_potter_fans_uz"},
    {"name": "🎬 5. Feniks jamiyati", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "🎬 HP 5: Feniks jamiyati\n@harry_potter_fans_uz"},
    {"name": "🎬 6. Tilsim Shahzoda", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA", "caption": "🎬 HP 6: Tilsim Shahzoda\n@harry_potter_fans_uz"},
    {"name": "🎬 7. Ajal tuhfasi 1", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA", "caption": "🎬 HP 7: Ajal tuhfasi 1-qism\n@harry_potter_fans_uz"},
    {"name": "🎬 8. Ajal tuhfasi 2", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "🎬 HP 8: Ajal tuhfasi 2-qism\n@harry_potter_fans_uz"},
]

MOVIES_RU = [
    {"name": "🎬 1. Философский камень", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE", "caption": "🎬 ГП 1: Философский камень\n@harry_potter_fans_uz"},
    {"name": "🎬 2. Тайная комната", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ", "caption": "🎬 ГП 2: Тайная комната\n@harry_potter_fans_uz"},
    {"name": "🎬 3. Узник Азкабана", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ", "caption": "🎬 ГП 3: Узник Азкабана\n@harry_potter_fans_uz"},
    {"name": "🎬 4. Кубок огня", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE", "caption": "🎬 ГП 4: Кубок огня\n@harry_potter_fans_uz"},
    {"name": "🎬 5. Орден Феникса", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ", "caption": "🎬 ГП 5: Орден Феникса\n@harry_potter_fans_uz"},
    {"name": "🎬 6. Принц-полукровка", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ", "caption": "🎬 ГП 6: Принц-полукровка\n@harry_potter_fans_uz"},
    {"name": "🎬 7. Дары Смерти 1", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ", "caption": "🎬 ГП 7: Дары Смерти 1\n@harry_potter_fans_uz"},
    {"name": "🎬 8. Дары Смерти 2", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE", "caption": "🎬 ГП 8: Дары Смерти 2\n@harry_potter_fans_uz"},
]

MOVIES_EN = [
    {"name": "🎬 1. Sorcerer's Stone", "file_id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ", "caption": "🎬 HP 1: Sorcerer's Stone\n@harry_potter_fans_uz"},
    {"name": "🎬 2. Chamber of Secrets", "file_id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ", "caption": "🎬 HP 2: Chamber of Secrets\n@harry_potter_fans_uz"},
    {"name": "🎬 3. Prisoner of Azkaban", "file_id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ", "caption": "🎬 HP 3: Prisoner of Azkaban\n@harry_potter_fans_uz"},
    {"name": "🎬 4. Goblet of Fire", "file_id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ", "caption": "🎬 HP 4: Goblet of Fire\n@harry_potter_fans_uz"},
    {"name": "🎬 5. Order of the Phoenix", "file_id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ", "caption": "🎬 HP 5: Order of the Phoenix\n@harry_potter_fans_uz"},
    {"name": "🎬 6. Half-Blood Prince", "file_id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ", "caption": "🎬 HP 6: Half-Blood Prince\n@harry_potter_fans_uz"},
    {"name": "🎬 7. Deathly Hallows 1", "file_id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ", "caption": "🎬 HP 7: Deathly Hallows 1\n@harry_potter_fans_uz"},
    {"name": "🎬 8. Deathly Hallows 2", "file_id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ", "caption": "🎬 HP 8: Deathly Hallows 2\n@harry_potter_fans_uz"},
]

# --- SHLYAPA ---
HOUSES_DETAILS = {
    "Hufflepuff": {"emoji": "🦡", "kalit": "aql", "txt": "💭 E-eh, men ko'ryapman... \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan."},
    "Gryffindor": {"emoji": "🦁", "kalit": "jasorat", "txt": "🦁 Yuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Jasurlik sening qoningda!"},
    "Slytherin": {"emoji": "🐍", "kalit": "ilon", "txt": "🐍 Buyuklikka intilish... Makr va aqlli munosabat. Sen maqsad sari hech narsadan to'xtamaysan!"},
    "Ravenclaw": {"emoji": "🦅", "kalit": "burgut", "txt": "🦅 O'tkir zehn va bilimga chanqoqlik. Sening aqling har qanday jumboqni yecha oladi!"}
}

# --- FUNKSIYALAR ---
def get_mention(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

async def delete_after_delay(message: types.Message, delay: int = 60):
    await asyncio.sleep(delay)
    try: await message.delete()
    except: pass

async def check_sub(user_id):
    try:
        m_ch = await bot.get_chat_member(CHANNEL, user_id)
        m_gr = await bot.get_chat_member(GROUP, user_id)
        valid = ['member', 'administrator', 'creator', 'restricted']
        return m_ch.status in valid, m_gr.status in valid
    except: return False, False

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

# --- JAZO HANDLER (MUTE, BAN, UNMUTE, KICK) ---
@dp.message_handler(commands=["mute", "ban", "unmute", "kick"])
async def admin_actions(message: types.Message):
    if message.chat.type == 'private': return
    
    admin_member = await message.chat.get_member(message.from_user.id)
    if not admin_member.is_chat_admin(): return

    if not message.reply_to_message:
        return await message.reply("⚠️ Bu buyruqni ishlatish uchun biror xabarga reply qiling!")

    target = message.reply_to_message.from_user
    bot_obj = await bot.get_me()

    # Adminlarni yoki Botni jazolashni oldini olish
    target_member = await message.chat.get_member(target.id)
    if target_member.is_chat_admin() or target.id == bot_obj.id:
        return await message.reply("🧙‍♂️ Kechirasiz, lekin o'zingizni yoki boshqa bir sehrgar adminni jazolash taqiqlangan! Bu Hogwarts qonunlariga zid.")

    cmd = message.get_command()
    mention = get_mention(target)

    try:
        if cmd == "/mute":
            args = message.get_args().split()
            m_time = int(args[0]) if args and args[0].isdigit() else 15
            await message.chat.restrict(target.id, permissions=types.ChatPermissions(can_send_messages=False), until_date=int(time.time())+(m_time*60))
            txt = f"🙊 {mention} <b>{m_time}</b> daqiqaga mute qilindi."
        elif cmd == "/ban":
            await message.chat.kick(target.id)
            txt = f"🚫 {mention} guruhdan haydaldi va banlandi."
        elif cmd == "/unmute":
            await message.chat.restrict(target.id, permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            txt = f"🔊 {mention} mutedan ozod qilindi."
        elif cmd == "/kick":
            await message.chat.unban(target.id)
            txt = f"👢 {mention} guruhdan chiqarib yuborildi."

        msg = await message.answer(txt, parse_mode="HTML")
        asyncio.create_task(delete_after_delay(msg))
    except Exception as e:
        await message.reply(f"❌ Xatolik yuz berdi: {str(e)}")

# --- START ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    in_ch, in_gr = await check_sub(message.from_user.id)
    mention = get_mention(message.from_user)
    
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
            InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="recheck_sub")
        )
        return await message.answer(f"Salom {mention}!\n\nBotdan foydalanish uchun kanalimiz va guruhimizga a'zo bo'ling.", reply_markup=btn, parse_mode="HTML")
    
    start_txt = f"Salom {mention}!\n\nHogwarts olamiga kirishga tayyormisiz? ✨\n\nMarhamat, menyulardan birini tanlang 👇"
    await message.answer(start_txt, reply_markup=main_menu(), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "recheck_sub")
async def recheck_callback(callback: types.CallbackQuery):
    in_ch, in_gr = await check_sub(callback.from_user.id)
    if in_ch and in_gr:
        await callback.message.delete()
        await start_cmd(callback.message)
    else:
        await callback.answer("Hali ham obuna bo'lmadingiz! ❌", show_alert=True)

# --- SHLYAPA ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    uid, data = str(message.from_user.id), load_data(HOUSES_FILE)
    if uid not in data:
        data[uid] = random.choice(list(HOUSES_DETAILS.keys()))
        save_data(HOUSES_FILE, data)
    
    h = HOUSES_DETAILS[data[uid]]
    msg = await message.answer("🧐 *O'ylayapman...*")
    await asyncio.sleep(2)
    
    final_text = f"{h['txt']}\n\n✨ *Hamma narsa ayon!* ✨\n\nFakultetingiz: {h['emoji']} <b>{data[uid]}</b>\n🔑 Kalit so'z: <code>{h['kalit']}</code>"
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapaga borish", url=f"https://t.me/{SHLYAPA_USER}"))
    await msg.edit_text(final_text, reply_markup=btn, parse_mode="HTML")

# --- MEDIA MENYU (KITOB/KINO) ---
@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_lang(message: types.Message):
    btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="b_uz"),
        InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="b_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="home")
    )
    await message.answer("Kitoblar tilini tanlang:", reply_markup=btn)

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movie_lang(message: types.Message):
    btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="m_uz"),
        InlineKeyboardButton("🇷🇺 Ruscha", callback_data="m_ru"),
        InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="m_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="home")
    )
    await message.answer("Kinolar tilini tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data in ["b_uz", "b_en", "m_uz", "m_ru", "m_en", "home"])
async def sub_menu(callback: types.CallbackQuery):
    d = callback.data
    if d == "home":
        await callback.message.delete()
        return await bot.send_message(callback.message.chat.id, "Asosiy menyu:", reply_markup=main_menu())
    
    btn = InlineKeyboardMarkup(row_width=1)
    if d == "b_uz":
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"get_buz_{i}"))
    elif d == "b_en":
        for i, b in enumerate(BOOKS_EN): btn.add(InlineKeyboardButton(b["name"], callback_data=f"get_ben_{i}"))
    elif d == "m_uz":
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"get_muz_{i}"))
    elif d == "m_ru":
        for i, m in enumerate(MOVIES_RU): btn.add(InlineKeyboardButton(m["name"], callback_data=f"get_mru_{i}"))
    elif d == "m_en":
        for i, m in enumerate(MOVIES_EN): btn.add(InlineKeyboardButton(m["name"], callback_data=f"get_men_{i}"))
    
    btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="home"))
    await callback.message.edit_text("Marhamat tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith("get_"))
async def send_file(callback: types.CallbackQuery):
    _, code, idx = callback.data.split("_")
    idx = int(idx)
    
    if code == "buz": item = BOOKS_UZ[idx]; f = bot.send_document
    elif code == "ben": item = BOOKS_EN[idx]; f = bot.send_document
    elif code == "muz": item = MOVIES_UZ[idx]; f = bot.send_video
    elif code == "mru": item = MOVIES_RU[idx]; f = bot.send_video
    elif code == "men": item = MOVIES_EN[idx]; f = bot.send_video
    
    await f(callback.message.chat.id, item["file_id"], caption=item["caption"])
    await callback.answer()

# --- WELCOME ---
@dp.message_handler(commands=["setwelcome"], user_id=ADMIN_ID)
async def welcome_init(message: types.Message):
    await message.reply("Kutib olish media yoki matnini yuboring ({name} - ism uchun):")
    dp.register_message_handler(welcome_save, user_id=ADMIN_ID, content_types=types.ContentTypes.ANY)

async def welcome_save(message: types.Message):
    if message.text and message.text.startswith("/"): return
    f_id, f_type = (message.photo[-1].file_id, "photo") if message.photo else ((message.video.file_id, "video") if message.video else ("None", "text"))
    data = load_data(WELCOME_FILE)
    data[str(message.chat.id)] = {"text": message.caption or message.text or "Xush kelibsiz {name}!", "f_id": f_id, "f_type": f_type}
    save_data(WELCOME_FILE, data)
    dp.message_handlers.unregister(welcome_save)
    await message.reply("✅ Kutib olish sozlamalari saqlandi!")

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    data = load_data(WELCOME_FILE)
    cid = str(message.chat.id)
    if cid in data:
        conf = data[cid]
        for user in message.new_chat_members:
            mention = get_mention(user)
            cap = conf['text'].replace("{name}", mention)
            try:
                if conf['f_type'] == "photo": msg = await bot.send_photo(cid, conf['f_id'], caption=cap, parse_mode="HTML")
                elif conf['f_type'] == "video": msg = await bot.send_video(cid, conf['f_id'], caption=cap, parse_mode="HTML")
                else: msg = await bot.send_message(cid, cap, parse_mode="HTML")
                asyncio.create_task(delete_after_delay(msg))
            except: pass

# --- GETID ADMIN ---
@dp.message_handler(commands=["getid"], user_id=ADMIN_ID)
async def get_id_start(message: types.Message):
    await message.reply("Fayl (rasm, video, hujjat) yuboring, ID sini beraman:")
    await AdminStates.waiting_for_file.set()

@dp.message_handler(state=AdminStates.waiting_for_file, content_types=types.ContentTypes.ANY)
async def get_id_process(message: types.Message, state: FSMContext):
    f_id = message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else (message.document.file_id if message.document else None))
    if f_id: await message.reply(f"<code>{f_id}</code>", parse_mode="HTML")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
