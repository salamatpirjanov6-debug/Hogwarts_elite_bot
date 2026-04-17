Import json
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
# Yangi token muvaffaqiyatli joylashtirildi
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8754136836:AAE10PBmNVqEYlJqb8gPxqzHey445m0lBKw")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7821230725
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML") # Standart HTML rejimi
dp = Dispatcher(bot, storage=storage)

class AdminStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_ad = State()

# --- MA'LUMOTLAR BAZASI ---

# Alohida tugma uchun "Hammasi birda" fayli
ALL_IN_ONE_BOOK = {"name": "📚 Hammasi birda (1-7)", "file_id": "BQACAgIAAxkBAAIDvWnOr_Z5zZ9Xj_vOL8p9R-Z8o8aLAAIqAAIx_1lLYm3f_zJ7z5M6BA", "caption": "📚 Garri Potter: Barcha qismlar (1-7) bitta faylda!\n\n📢 Kanal: @harry_potter_fans_uz"}

BOOKS_UZ = [
    {"name": "📖 1. Falsafiy tosh", "file_id": "BQACAgIAAxkBAANBacuvW5b3Swv7_h1BWKHAr9BSFDEAAnAAA0vfYUn_DvBFWXk9WToE", "caption": "📖 Nomi: Garri Potter va Falsafiy tosh\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 2. Maxfiy xujra", "file_id": "BQACAgIAAxkBAANGacuv4uq6XXW9EVN4c1mrczrhf4AAAi4AAwSsEEpZs7eKKsu6szoE", "caption": "📖 Nomi: Garri Potter va Maxfiy hujra\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 3. Azkaban maxbusi", "file_id": "BQACAgIAAxkBAANlacuwQSg_C6sntUxgp1s-EwTRw10AAgkHAAJfZdhIu3sjwnyKCrQ6BA", "caption": "📖 Nomi: Garri Potter va Azkaban mahbusi\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 4. Otashli jom", "file_id": "BQACAgIAAxkBAANnacuwaXcFuxDS8ll0QQ8YYgjxNxcAAjMAAwSsEEoCrCr_9txjwDoE", "caption": "📖 Nomi: Garri Potter va Otashli jom\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 5. Kaknus ordeni", "file_id": "BQACAgIAAxkBAANpacuwkFa_xAhxOPRwz6_O5mhZzkMAAmsAA-A7GEoe0fZOrviJXjoE", "caption": "📖 Nomi: Garri Potter va Kaknus ordeni\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 6. Chalazot shaxzoda", "file_id": "BQACAgIAAxkBAANracuwqVy7l3UaOeEsHvDN8DYyYK4AApIAAzXcUEotF3tao-vWxToE", "caption": "📖 Nomi: Garri Potter va Chalazot shahzoda\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 7. Ajal tuhfalari 1", "file_id": "BQACAgIAAxkBAANtacuwwS1FlLl5SubbQJDSn6ghyyoAAg8CAAKpCIBJRzBcQ4IMdzA6BA", "caption": "📖 Nomi: Garri Potter va Ajal tuhfalari 1\n\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "📖 8. Ajal tuhfalari 2", "file_id": "BQACAgIAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Nomi: Garri Potter va Ajal tuhfalari 2\n\n📢 Kanal: @harry_potter_fans_uz"},
]

BOOKS_EN = [
    {"name": "📖 1. Philosopher's Stone", "file_id": "BQACAgUAAxkBAAIDOWnOk3dbX8E-yaAVFy_xfeP6IqKGAAL_AwACn_N4VR4lpjl-n1tZOgQ", "caption": "📖 Name: Harry Potter 1\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 2. Chamber of Secrets", "file_id": "BQACAgUAAxkBAAIDO2nOk9iTjQ_vULXaRoo7BPiFoyESAAMEAAKf83hV774CCp3aF146BA", "caption": "📖 Name: Harry Potter 2\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 3. Prisoner of Azkaban", "file_id": "BQACAgUAAxkBAAIDPWnOk_jB-bYD-xsrsq6Y1xveD1mBAAL-AwACn_N4Vd-iiVWRVt-DOgQ", "caption": "📖 Name: Harry Potter 3\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 4. Goblet of Fire", "file_id": "BQACAgUAAxkBAAIDP2nOlAzIskBV4m7d6OgD3G1o2FOEAAL7AwACn_N4VdM2NXmcWgR-OgQ", "caption": "📖 Name: Harry Potter 4\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 5. Order of the Phoenix", "file_id": "BQACAgUAAxkBAAIDQWnOlB5zRwpHT1wOS9diXcxjCcogAAL5AwACn_N4VQGCfrTny6GKOgQ", "caption": "📖 Name: Harry Potter 5\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 6. Half-Blood Prince", "file_id": "BQACAgUAAxkBAAIDQ2nOlDGDPZqe9r1QZbUUJDj4-L0UAAL6AwACn_N4VWeuyWoTm2SnOgQ", "caption": "📖 Name: Harry Potter 6\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 7. Deathly Hallows 1", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Name: Harry Potter 7\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "📖 8. Deathly Hallows 2", "file_id": "BQACAgUAAxkBAAIDRWnOlEOi6oyRRafs-Y9Yl1Lo19fjAAL8AwACn_N4VdOVKXxjV5MlOgQ", "caption": "📖 Name: Harry Potter 8\n📢 Channel: @harry_potter_fans_uz"},
]

MOVIES_UZ = [
    {"name": "🎬 1. Hikmatlar toshi", "file_id": "BAACAgIAAxkBAAN0acuyGAMCrWD9TTuMq55gFHUM8scAAr2OAAKIIOhKA6wazQylWz46BA", "caption": "🎬 Nomi: HP 1: Hikmatlar toshi\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 2. Maxfiy hujra", "file_id": "BAACAgIAAxkBAAOFacu0BPXsr3WF3yYGmJHdjVeDjSMAAmSFAALhnOhKpL77RQyPlaE6BA", "caption": "🎬 Nomi: HP 2: Maxfiy hujra\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 3. Azkoban maxbusi", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "🎬 Nomi: HP 3: Azkoban maxbusi\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 4. Alanga kubogi", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "🎬 Nomi: HP 4: Alanga kubogi\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 5. Feniks jamiyati", "file_id": "BAACAgIAAxkBAAOHacu0W-SHgaTmaKyMu7N7S4D-9NQAAn6FAALhnOhKpYQqLyzBd-k6BA", "caption": "🎬 Nomi: HP 5: Feniks jamiyati\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 6. Tilsim Shahzoda", "file_id": "BAACAgIAAxkBAAONacu1kktAejSVYq9GM3xmHXGzrfAAAoyFAALhnOhKrgZBW8bL1Ws6BA", "caption": "🎬 Nomi: HP 6: Tilsim Shahzoda\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 7. Ajal tuhfasi 1", "file_id": "BAACAgIAAxkBAAOPacu1qaZL-FLQaWMNmAbS1P6B-DUAApeFAALhnOhKF_fANiYvpAk6BA", "caption": "🎬 Nomi: HP 7: Ajal tuhfasi 1\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
    {"name": "🎬 8. Ajal tuhfasi 2", "file_id": "BAACAgIAAxkBAAOJacu1AoUKWQUInEPM0DGXvSZhueUAAqmFAALhnOhKZfF9wiu0Drs6BA", "caption": "🎬 Nomi: HP 8: Ajal tuhfasi 2\n⏱ Vaqti: 2.5 soat\n🌐 Tili: O'zbekcha\n🎞 Sifati: HD\n📢 Kanal: @harry_potter_fans_uz"},
]

MOVIES_RU = [
    {"name": "🎬 1. Философский камень", "file_id": "BAACAgIAAxkBAAIDSWnOlb1_AAGAYgWnEGm3bGJfXjFeggACKAoAAjH_WUs4J1skcGE7GToE", "caption": "🎬 Название: ГП 1: Философский камень\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 2. Тайная комната", "file_id": "BAACAgIAAxkBAAIDS2nOld1zIwQEOIo_XNaB20dS4yBKAAImCgACMf9ZS8YV5UtV-2QLOgQ", "caption": "🎬 Название: ГП 2: Тайная комната\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 3. Узник Азкабана", "file_id": "BAACAgIAAxkBAAIDTWnOlfGGh3F6yuTdkzg6YDll0LciAAInCgACMf9ZSxH4i6-D8wN7OgQ", "caption": "🎬 Название: ГП 3: Узник Азкабана\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 4. Кубок огня", "file_id": "BAACAgIAAxkBAAIDT2nOlgJFMBSJSqBULhYTkSS0dmsdAAIjCgACMf9ZS1Zt8gABJXZpWDoE", "caption": "🎬 Название: ГП 4: Кубок огня\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 5. Орден Феникса", "file_id": "BAACAgQAAxkBAAIDUWnOlhMJxYJ_yWbXZLJ25ZPTS0JJAAKgDAAC2L_JULzvFz_NQdPnOgQ", "caption": "🎬 Название: ГП 5: Орден Феникса\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 6. Принц-полукровка", "file_id": "BAACAgIAAxkBAAIDU2nOliUy9hL1ssJ5e-kORyqEL5DgAAIlCgACMf9ZS2Yi3TnE3abiOgQ", "caption": "🎬 Название: ГП 6: Принц-полукровка\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 7. Дары Смерти 1", "file_id": "BAACAgIAAxkBAAIDVWnOljREOEjf4v0o0Sz2DHs1Zm3xAALpBAACKP2pSAiPJCewUqfUOgQ", "caption": "🎬 Название: ГП 7: Дары Смерти 1\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
    {"name": "🎬 8. Дары Смерти 2", "file_id": "BAACAgIAAxkBAAIDV2nOlkSVUkDW2WL6f4WrUmapIQABcQACZQQAAsSsoUjP9fxCTDgDNzoE", "caption": "🎬 Название: ГП 8: Дары Смерти 2\n⏱ Время: 2.5 часа\n🌐 Язык: Русский\n🎞 Качество: HD\n📢 Канал: @harry_potter_fans_uz"},
]

MOVIES_EN = [
    {"name": "🎬 1. Sorcerer's Stone", "file_id": "BAACAgQAAxkBAAIDWWnOltDBBkgHlm6EC5zZ1__vemdSAAJ_BwACrMaBUKRYUpDTm11oOgQ", "caption": "🎬 Name: HP 1: Sorcerer's Stone\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 2. Chamber of Secrets", "file_id": "BAACAgQAAxkBAAIDW2nOlynvMgKOoF9hn7r8CcccUZo-AAKBBwACrMaBUM7959H4o01HOgQ", "caption": "🎬 Name: HP 2: Chamber of Secrets\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 3. Prisoner of Azkaban", "file_id": "BAACAgQAAxkBAAIDXWnOlz4dtzVGjgW6u9JUz1frSKKNAAKHBwACrMaBUKP9MbVImI-uOgQ", "caption": "🎬 Name: HP 3: Prisoner of Azkaban\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 4. Goblet of Fire", "file_id": "BAACAgQAAxkBAAIDX2nOl0-8b1wOF8VhdnLiVTmx2lQ0AAKOBwACrMaBUNmv6Ega62iuOgQ", "caption": "🎬 Name: HP 4: Goblet of Fire\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 5. Order of the Phoenix", "file_id": "BAACAgQAAxkBAAIDYWnOl1-UJIPeUi9iwkH5xveOb1cBAAKVBwACrMaBUC7iNQH-PQokOgQ", "caption": "🎬 Name: HP 5: Order of the Phoenix\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 6. Half-Blood Prince", "file_id": "BAACAgQAAxkBAAIDY2nOl28ipXgwucm7uiCsJ00NrHObAAKNCAACqwKBUHgSmGHyOYgROgQ", "caption": "🎬 Name: HP 6: Half-Blood Prince\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 7. Deathly Hallows 1", "file_id": "BAACAgQAAxkBAAIDZWnOl36nQLjV7TlugAMlJE6y1xFKAAKXCAACqwKBUMiAIxlbsJmOOgQ", "caption": "🎬 Name: HP 7: Deathly Hallows 1\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
    {"name": "🎬 8. Deathly Hallows 2", "file_id": "BAACAgQAAxkBAAIDZ2nOl41aUWcgKRzzP_r-suInRRSKAAKkCAACqwKBUC733-s2FjB3OgQ", "caption": "🎬 Name: HP 8: Deathly Hallows 2\n⏱ Time: 2.5 hours\n🌐 Lang: English\n🎞 Quality: HD\n📢 Channel: @harry_potter_fans_uz"},
]

HOUSES_DETAILS = {
    "Hufflepuff": {"emoji": "🦡", "kalit": "aql", "txt": "💭 E-eh, men ko'ryapman... \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan."},
    "Gryffindor": {"emoji": "🦁", "kalit": "jasorat", "txt": "🦁 Yuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Jasurlik sening qoningda!"},
    "Slytherin": {"emoji": "🐍", "kalit": "ilon", "txt": "🐍 Buyuklikka intilish... Makr va aqlli munosabat. Sen maqsad sari hech narsadan to'xtamaysan!"},
    "Ravenclaw": {"emoji": "🦅", "kalit": "burgut", "txt": "🦅 O'tkir zehn va bilimga chanqoqlik. Sening aqling har qanday jumboqni yecha oladi!"}
}

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
USERS_FILE = "users_list.json"
WELCOME_FILE = "welcome_settings.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

# --- FUNKSIYALAR ---
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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

# --- AVTO-OCHIRISH FUNKSIYASI ---
async def delete_after_delay(message: types.Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

# --- JAZO TIZIMI ---
@dp.message_handler(commands=["mute", "ban", "unmute"])
async def handle_punishment(message: types.Message):
    if message.chat.type == 'private': return
    
    sender_id = message.from_user.id
    sender_member = await message.chat.get_member(sender_id)
    
    if not sender_member.is_chat_admin():
        return await message.reply(f"🧙‍♂️ Kechirasiz {get_mention(message.from_user)}, sizda sehrli tayoqcha 🪄 yo'q! Avval sehrli tayoqchaga ega bo'ling.")

    if not message.reply_to_message:
        return await message.reply("⚠️ Sehr ishlatish uchun biror kishiga reply qiling!")

    target = message.reply_to_message.from_user
    target_member = await message.chat.get_member(target.id)
    bot_obj = await bot.get_me()

    if target_member.is_chat_admin() or target.id == bot_obj.id:
        return await message.reply("🧙‍♂️ Kechirasiz, lekin o'zingizni yoki boshqa bir sehrgar adminni jazolash taqiqlangan!")

    cmd = message.get_command()
    try:
        if cmd == "/ban":
            await message.chat.kick(target.id)
            await message.answer(f"🚫 {get_mention(target)} ⛓ Hogwarts o'quvchisi yovuz yo'lga kirgani uchun Azkabanga ravona bo'ldi!")
        elif cmd == "/mute":
            await message.chat.restrict(target.id, permissions=types.ChatPermissions(can_send_messages=False), until_date=int(time.time())+300)
            await message.answer(f"🙊 {get_mention(target)} Silencio afsuni ostida! 5 daqiqaga ovozi o'chirildi.")
        elif cmd == "/unmute":
            await message.chat.restrict(target.id, permissions=types.ChatPermissions(can_send_messages=True))
            await message.answer(f"🔊 {get_mention(target)}dan Silencio afsuni yechildi.")
    except Exception as e:
        await message.reply(f"❌ Sehr amalga oshmadi: {str(e)}")

# --- START VA TEKSHIRISH ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user = message.from_user
    users = load_data(USERS_FILE)
    if str(user.id) not in users:
        users[str(user.id)] = user.first_name
        save_data(USERS_FILE, users)

    is_subscribed = await check_sub(user.id)
    if not is_subscribed:
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
            InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="recheck_sub")
        )
        return await message.answer(f"Salom {get_mention(user)}!\n\nBotdan foydalanish uchun kanal va guruhga a'zo bo'ling.", reply_markup=btn)
    
    await message.answer(f"Salom {get_mention(user)}!\nHogwarts olamiga xush kelibsiz! ✨", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "recheck_sub")
async def recheck_callback(callback: types.CallbackQuery):
    is_subscribed = await check_sub(callback.from_user.id)
    if is_subscribed:
        await callback.message.delete()
        await bot.send_message(callback.message.chat.id, f"Salom {get_mention(callback.from_user)}!\nHogwarts olamiga xush kelibsiz! ✨", reply_markup=main_menu())
    else:
        await callback.answer("Siz hali ham barcha shartlarni bajarmadingiz! ❌", show_alert=True)

# --- KITOBLAR VA KINOLAR ---
@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_lang(message: types.Message):
    btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📚 Hammasi birda (1-7)", callback_data="get_all_books"),
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="b_uz"),
        InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="b_en"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="home")
    )
    await message.answer("Kitoblar bo'limini tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == "get_all_books")
async def all_books_sender(callback: types.CallbackQuery):
    await bot.send_document(callback.message.chat.id, ALL_IN_ONE_BOOK["file_id"], caption=ALL_IN_ONE_BOOK["caption"])
    await callback.answer()

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
async def handle_sub_menus(callback: types.CallbackQuery):
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
    await callback.message.edit_text("Marhamat, tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith("get_"))
async def send_media_file(callback: types.CallbackQuery):
    _, code, idx = callback.data.split("_")
    idx = int(idx)
    
    if code == "buz": item = BOOKS_UZ[idx]; f = bot.send_document
    elif code == "ben": item = BOOKS_EN[idx]; f = bot.send_document
    elif code == "muz": item = MOVIES_UZ[idx]; f = bot.send_video
    elif code == "mru": item = MOVIES_RU[idx]; f = bot.send_video
    elif code == "men": item = MOVIES_EN[idx]; f = bot.send_video
    
    await f(callback.message.chat.id, item["file_id"], caption=item["caption"])
    await callback.answer()

# --- SHLYAPA ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    uid, data = str(message.from_user.id), load_data(HOUSES_FILE)
    if uid not in data:
        data[uid] = random.choice(list(HOUSES_DETAILS.keys()))
        save_data(HOUSES_FILE, data)
    
    h = HOUSES_DETAILS[data[uid]]
    msg = await message.answer("🧐 <b>O'ylayapman...</b>")
    await asyncio.sleep(2)
    
    final_text = (f"{h['txt']}\n\n✨ <b>Hamma narsa ayon!</b> ✨\n\nFakultetingiz: {h['emoji']} <b>{data[uid]}</b>\n🔑 Kalit so'z: <code>{h['kalit']}</code>\n\nKalit so'zni shlyapaga yuboring 👇")
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapaga borish", url=f"https://t.me/{SHLYAPA_USER}"))
    await msg.edit_text(final_text, reply_markup=btn)

# --- ADMIN PANEL ---
@dp.message_handler(commands=["admins"], user_id=ADMIN_ID)
async def admin_panel(message: types.Message):
    txt = ("🧙‍♂️ <b>Admin Panel:</b>\n\n/send - Reklama\n/getid - Fayl ID\n/ban - Azkaban\n/mute - Silencio")
    await message.answer(txt)

@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def ad_start(message: types.Message):
    await message.reply("Reklama xabarini yuboring:")
    await AdminStates.waiting_for_ad.set()

@dp.message_handler(state=AdminStates.waiting_for_ad, content_types=types.ContentTypes.ANY)
async def ad_process(message: types.Message, state: FSMContext):
    users = load_data(USERS_FILE)
    count = 0
    for uid in users:
        try:
            await message.copy_to(uid)
            count += 1
        except: pass
    await message.answer(f"✅ Xabar {count} kishiga yuborildi.")
    await state.finish()

# --- WELCOME VA AVTO OCHIRISH ---
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    data = load_data(WELCOME_FILE)
    cid = str(message.chat.id)
    btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
        InlineKeyboardButton("🎩 Fakultet", url=f"https://t.me/{SHLYAPA_USER}?start=sorting")
    )
    for user in message.new_chat_members:
        mention = get_mention(user)
        if cid in data:
            conf = data[cid]
            cap = conf['text'].replace("{name}", mention)
            if conf['f_type'] == "photo": 
                m = await bot.send_photo(cid, conf['f_id'], caption=cap, reply_markup=btn)
            elif conf['f_type'] == "video": 
                m = await bot.send_video(cid, conf['f_id'], caption=cap, reply_markup=btn)
            else: 
                m = await bot.send_message(cid, cap, reply_markup=btn)
            
            asyncio.create_task(delete_after_delay(m, 600))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
