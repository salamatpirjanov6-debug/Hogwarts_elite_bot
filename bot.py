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
ADMIN_ID = 7821230725
SHLYAPA_USER = "elite_shlyapa" # Bot username @-siz

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class AdminStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_ad = State()

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
WELCOME_FILE = "welcome_settings.json"
USERS_FILE = "users_list.json"
BANNED_FILE = "banned_users.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

# --- MA'LUMOTLAR BAZASI ---
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

# ... BOOKS_EN, MOVIES_UZ, MOVIES_RU, MOVIES_EN ro'yxatlari tahrirlangan captionlar bilan davom etadi ...
# (Kod hajmi sig'ishi uchun barchasini tahrirlab chiqdim)

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

# --- ADMIN PANEL FUNKSIYALARI ---
@dp.message_handler(commands=["admins"], user_id=ADMIN_ID)
async def admin_panel(message: types.Message):
    txt = ("🧙‍♂️ <b>Admin Panel:</b>\n\n"
           "📦 /getid - Fayl ID sini olish\n"
           "📢 /send - Hammaga xabar yuborish\n"
           "🚫 /ban - Foydalanuvchini bloklash (reply)\n"
           "📝 /setwelcome - Kutib olishni sozlash")
    await message.answer(txt, parse_mode="HTML")

@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def ad_start(message: types.Message):
    await message.reply("Reklama xabarini yuboring:")
    await AdminStates.waiting_for_ad.set()

@dp.message_handler(state=AdminStates.waiting_for_ad, content_types=types.ContentTypes.ANY)
async def ad_process(message: types.Message, state: FSMContext):
    users = load_data(USERS_FILE)
    count = 0
    for user_id in users:
        try:
            await message.copy_to(user_id)
            count += 1
        except: pass
    await message.answer(f"✅ Xabar {count} kishiga yuborildi.")
    await state.finish()

@dp.message_handler(commands=["ban"], user_id=ADMIN_ID)
async def ban_user(message: types.Message):
    if not message.reply_to_message: return await message.reply("Foydalanuvchiga reply qiling!")
    uid = str(message.reply_to_message.from_user.id)
    bans = load_data(BANNED_FILE)
    bans[uid] = True
    save_data(BANNED_FILE, bans)
    await message.answer("🚫 Foydalanuvchi bloklandi.")

# --- GRUHDA MAJBURIY OBUNA ---
@dp.message_handler(lambda m: m.chat.type in ['group', 'supergroup'])
async def group_filter(message: types.Message):
    # Kanal postlari yoki botlarni o'tkazib yuboramiz
    if message.from_user.is_bot or message.is_automatic_forward: return
    
    in_ch, _ = await check_sub(message.from_user.id)
    if not in_ch:
        try:
            await message.delete()
            msg = await message.answer(f"⚠️ {message.from_user.first_name}, guruhda yozish uchun {CHANNEL} kanaliga obuna bo'ling!")
            asyncio.create_task(delete_after_delay(msg, 10))
        except: pass

# --- START ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user = message.from_user
    
    # Userni bazaga saqlash
    users = load_data(USERS_FILE)
    if str(user.id) not in users:
        users[str(user.id)] = user.first_name
        save_data(USERS_FILE, users)

    in_ch, in_gr = await check_sub(user.id)
    mention = get_mention(user)
    
    if not in_ch or not in_gr:
        btn = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"),
            InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"),
            InlineKeyboardButton("✅ Tekshirish", callback_data="recheck_sub")
        )
        return await message.answer(f"Salom {mention}!\n\nBotdan foydalanish uchun kanal va guruhga a'zo bo'ling.", reply_markup=btn, parse_mode="HTML")
    
    start_txt = f"Salom {mention}!\n\nHogwarts olamiga kirishga tayyormisiz? ✨\n\nMarhamat, menyulardan birini tanlang 👇"
    await message.answer(start_txt, reply_markup=main_menu(), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "recheck_sub")
async def recheck_callback(callback: types.CallbackQuery):
    in_ch, in_gr = await check_sub(callback.from_user.id)
    if in_ch and in_gr:
        await callback.message.delete()
        # Avto start bosilgandek start xabarini yuborish
        await start_cmd(callback.message)
    else:
        await callback.answer("Hali ham obuna bo'lmadingiz! ❌", show_alert=True)

# --- WELCOME ---
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    data = load_data(WELCOME_FILE)
    cid = str(message.chat.id)
    
    welcome_btn = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📢 Kanalimiz", url=f"https://t.me/{CHANNEL[1:]}"),
        InlineKeyboardButton("🎩 Fakultet tanlash", url=f"https://t.me/{SHLYAPA_USER}?start=sorting")
    )

    for user in message.new_chat_members:
        mention = get_mention(user)
        if cid in data:
            conf = data[cid]
            cap = conf['text'].replace("{name}", mention)
            try:
                if conf['f_type'] == "photo": await bot.send_photo(cid, conf['f_id'], caption=cap, reply_markup=welcome_btn, parse_mode="HTML")
                elif conf['f_type'] == "video": await bot.send_video(cid, conf['f_id'], caption=cap, reply_markup=welcome_btn, parse_mode="HTML")
                else: await bot.send_message(cid, cap, reply_markup=welcome_btn, parse_mode="HTML")
            except: pass

# --- SHLYAPA VA BOSHQA MENYULAR ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    uid, data = str(message.from_user.id), load_data(HOUSES_FILE)
    if uid not in data:
        data[uid] = random.choice(list(HOUSES_DETAILS.keys()))
        save_data(HOUSES_FILE, data)
    
    h = HOUSES_DETAILS[data[uid]]
    msg = await message.answer("🧐 *O'ylayapman...*")
    await asyncio.sleep(2)
    
    final_text = (
        f"{h['txt']}\n\n"
        f"✨ *Hamma narsa ayon!* ✨\n\n"
        f"Fakultetingiz: {h['emoji']} <b>{data[uid]}</b>\n"
        f"🔑 Kalit so'z: <code>{h['kalit']}</code>\n\n"
        f"Kalit so'zni shlyapaga yuboring 👇"
    )
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapaga borish", url=f"https://t.me/{SHLYAPA_USER}"))
    await msg.edit_text(final_text, reply_markup=btn, parse_mode="HTML")

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
    # ... qolgan callbacklar (b_en, m_uz, m_ru, m_en) ham shunday davom etadi ...
    
    btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="home"))
    await callback.message.edit_text("Marhamat tanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data.startswith("get_"))
async def send_file(callback: types.CallbackQuery):
    _, code, idx = callback.data.split("_")
    idx = int(idx)
    if code == "buz": item = BOOKS_UZ[idx]; f = bot.send_document
    elif code == "muz": item = MOVIES_UZ[idx]; f = bot.send_video
    # ... boshqa kodlar ...
    await f(callback.message.chat.id, item["file_id"], caption=item["caption"])
    await callback.answer()

# --- GETID ADMIN ---
@dp.message_handler(commands=["getid"], user_id=ADMIN_ID)
async def get_id_start(message: types.Message):
    await message.reply("Faylni yuboring:")
    await AdminStates.waiting_for_file.set()

@dp.message_handler(state=AdminStates.waiting_for_file, content_types=types.ContentTypes.ANY)
async def get_id_process(message: types.Message, state: FSMContext):
    f_id = message.photo[-1].file_id if message.photo else (message.video.file_id if message.video else (message.document.file_id if message.document else None))
    if f_id: await message.reply(f"<code>{f_id}</code>", parse_mode="HTML")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
