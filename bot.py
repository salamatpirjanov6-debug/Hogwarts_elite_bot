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
# Railway-da Environments bo'limiga TELEGRAM_BOT_TOKEN qo'shishni unutmang
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7718919427:AAH0p85Lh_XFsc-2n0L8O956T8Xw68Y9NqE")
CHANNEL = "@harry_potter_fans_uz"
GROUP = "@hogwarts_elite"
ADMIN_ID = 7670992727 # Sizning IDgiz
SHLYAPA_USER = "elite_shlyapa"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- BAZA FAYLLARI ---
HOUSES_FILE = "user_houses.json"
USERS_FILE = "bot_users.json"

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

# --- FAYL IDlar (O'zgarishsiz qoldi) ---
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

# --- SHLYAPA GAPLARI (YANGI ✨) ---
SORTING_MESSAGES = [
    "🤔 *Hmmm... qiyin, juda qiyin.* \nKo'ryapman, bu yerda aql ham yetarli, iste'dod ham... va-a-ay, qanday ulkan xohish!",
    "🧐 *Iye, bu qanday sirli qalb?* \nAql bovar qilmaydigan jasorat, biroz makr... Ha, sen Hogvarts tarixini o'zgartira olasan!",
    "💭 *E-eh, men ko'ryapman...* \nSadoqat senda birinchi o'rinda. Mehnat qilishdan qo'rqmaysan, do'stlaring uchun joningni berishga tayyorsan.",
    "🐍 *Qiziq, juda qiziq...* \nShon-shuhratga bo'lgan chanqoqlik, aqlli munosabat. Ha, sen buyuklikka loyiqsan!",
    "🦁 *Bu yerda nima bor?* \nYuraging to'la qo'rqmaslik. Sen xavf-xatarga tik boqishni bilasan. Ha, jasurlik sening qoningda!"
]

# --- MENYULAR (O'zgarishsiz) ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📚 Kitoblar"), KeyboardButton("🎬 Kinolar"))
    markup.add(KeyboardButton("🎩 Saralovchi shlyapa"))
    return markup

def book_lang_menu():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_book_uz"),
        InlineKeyboardButton("➡️ Orqaga", callback_data="back_to_main")
    )
    return btn

def movie_lang_menu():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_movie_uz"),
        InlineKeyboardButton("➡️ Orqaga", callback_data="back_to_main")
    )
    return btn

# --- LOGIKA ---
houses_dict = {
    "Slytherin": "ilon",
    "Hufflepuff": "aql",
    "Ravenclaw": "burgut",
    "Gryffindor": "jasorat"
}
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
        if not in_ch: btn.add(InlineKeyboardButton("📢 Kanal", url=f"https://t.me/{CHANNEL[1:]}"))
        if not in_gr: btn.add(InlineKeyboardButton("👥 Guruh", url=f"https://t.me/{GROUP[1:]}"))
        btn.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub_status"))
        await message.answer("❗ Botdan foydalanish uchun obuna bo'ling:", reply_markup=btn)
        return
    
    await message.answer(f"Xush kelibsiz, sehrgar {message.from_user.first_name}! Bo'limni tanlang:", reply_markup=main_menu())

# --- ADMIN REKLAMA ---
@dp.message_handler(commands=["send"], user_id=ADMIN_ID)
async def send_ads(message: types.Message):
    text = message.get_args()
    if not text:
        await message.reply("Foydalanish: `/send xabar_matni`")
        return
    
    users = load_data(USERS_FILE)
    count = 0
    for uid in users:
        try:
            await bot.send_message(uid, text)
            count += 1
        except: continue
    await message.answer(f"📢 Xabar {count} ta sehrgarga yuborildi!")

# --- MENYU HANDLERLARI (FIXED) ---
@dp.message_handler(lambda m: m.text == "📚 Kitoblar")
async def book_menu_btn(message: types.Message):
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    await message.answer("Kitoblar uchun tilni tanlang:", reply_markup=book_lang_menu())

@dp.message_handler(lambda m: m.text == "🎬 Kinolar")
async def movie_menu_btn(message: types.Message):
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    await message.answer("Kinolar uchun tilni tanlang:", reply_markup=movie_lang_menu())

# --- SHLYAPA (YANGILANGAN ✨) ---
@dp.message_handler(lambda m: m.text == "🎩 Saralovchi shlyapa")
async def sorting_hat(message: types.Message):
    if not (await check_sub(message.from_user.id))[0]: return await start_cmd(message)
    
    uid = str(message.from_user.id)
    data = load_data(HOUSES_FILE)
    
    # Kinodagi shlyapa gaplaridan tasodifiy tanlash
    intro_text = random.choice(SORTING_MESSAGES)
    
    if uid not in data:
        # Yangi foydalanuvchi bo'lsa, fakultet tanlash
        fname = random.choice(list(houses_dict.keys()))
        data[uid] = fname
        save_data(HOUSES_FILE, data)
    
    # Saqlangan fakultetni olish
    fname = data[uid]
    key_word = houses_dict[fname]
    
    # Fakultetga mos emoji va tasvirlar
    house_details = {
        "Slytherin": {"emoji": "🐍", "color": "Yashil"},
        "Hufflepuff": {"emoji": "🦡", "color": "Sariq"},
        "Ravenclaw": {"emoji": "🦅", "color": "Ko'k"},
        "Gryffindor": {"emoji": "🦁", "color": "Qizil"}
    }
    
    h_emoji = house_details[fname]["emoji"]
    
    # Yakuniy chiroyli matn
    text = (f"{intro_text}\n\n"
            f"✨ Hamma narsa ayon! ✨\n\n"
            f"Sizning fakultetingiz: {h_emoji} **{fname}** {h_emoji}\n\n"
            f"🔑 Kalit so'zi: `{key_word}`\n\n"
            f"*(Nusxa olish uchun kalit so'z ustiga bosing)*\n"
            f"Kalit so'zni shlyapaga yuboring 👇")
    
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("🎩 Shlyapa bilan bog'lanish", url=f"https://t.me/{SHLYAPA_USER}"))
    await message.answer(text, reply_markup=btn, parse_mode="Markdown")

# --- CALLBACKLAR (O'zgarishsiz) ---
@dp.callback_query_handler(lambda c: True)
async def callback_handler(callback: types.CallbackQuery):
    uid = callback.message.chat.id
    
    if callback.data == "check_sub_status":
        in_ch, in_gr = await check_sub(callback.from_user.id)
        if in_ch and in_gr:
            await callback.message.delete()
            await bot.send_message(uid, "Tabriklaymiz! Endi botdan foydalanishingiz mumkin. 🎉", reply_markup=main_menu())
        else:
            await callback.answer("❗ Siz hali obuna bo'lmagansiz, iltimos qayta urinib ko'ring!", show_alert=True)

    elif callback.data == "back_to_main":
        await callback.message.delete()
        await bot.send_message(uid, "Asosiy menyu:", reply_markup=main_menu())

    elif callback.data == "lang_book_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, b in enumerate(BOOKS_UZ): btn.add(InlineKeyboardButton(b["name"], callback_data=f"uzb_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kitoblar:", reply_markup=btn)

    elif callback.data == "lang_movie_uz":
        btn = InlineKeyboardMarkup(row_width=1)
        for i, m in enumerate(MOVIES_UZ): btn.add(InlineKeyboardButton(m["name"], callback_data=f"uzm_{i}"))
        btn.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        await callback.message.edit_text("🇺🇿 O'zbekcha kinolar:", reply_markup=btn)

    elif callback.data.startswith("uzb_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_document(uid, BOOKS_UZ[idx]["file_id"], caption=BOOKS_UZ[idx]["name"])
    elif callback.data.startswith("uzm_"):
        idx = int(callback.data.split("_")[1])
        await bot.send_video(uid, MOVIES_UZ[idx]["file_id"], caption=MOVIES_UZ[idx]["name"])

    await callback.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
