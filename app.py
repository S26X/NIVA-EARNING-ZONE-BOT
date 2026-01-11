import telebot
from telebot import types
import os
import threading
from flask import Flask

# ১. আপনার তথ্য এবং ২ জন অ্যাডমিনের আইডি
TOKEN = '7919867918:AAEjGAwUApVfowkMdjofLXBJZ8tjQYQ2LUQ'
ADMIN_IDS = [7665757155, 8505710811] 

bot = telebot.TeleBot(TOKEN)
USER_FILE = "users.txt"

# ২. হোস্টিং সার্ভারকে চালু রাখার জন্য Flask Web Server
app = Flask('')
@app.route('/')
def home():
    return "Niva Bot is Active 24/7!"

def run():
    # Katabump বা অনলাইন সার্ভারের জন্য পোর্ট ৮০৮০ ব্যবহার করা হয়
    app.run(host='0.0.0.0', port=8080)

# ৩. ইউজার ডাটা সেভ ফাংশন
def save_user(chat_id):
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    if str(chat_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(str(chat_id) + "\n")

# ৪. স্টার্ট কমান্ড (সাজানো ওয়েলকাম মেসেজ)
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    user_name = message.from_user.first_name
    
    welcome_text = (
        f"👋 **Welcome Back, {user_name}!**\n"
        f"🌟 **Niva Buyer Zone**-এ আপনাকে স্বাগতম!\n\n"
        "🚀 **ফাস্টেস্ট সেলিং | সেরা নিরাপত্তা!**\n"
        "🛡️ প্রতারণাময় মার্কেটে আপনার আস্থার একমাত্র প্রতীক আমাদের এই BOT!\n\n"
        "যখন পুরো মার্কেট প্রতারণায় পূর্ণ, তখন আমরা দিচ্ছি—\n"
        "✅ **ফাস্টেস্ট কয়েন সেলের গ্যারান্টি**\n"
        "✅ **১০০% নিরাপদ লেনদেনের নিশ্চয়তা**\n\n"
        "💰 Niva, NS সহ সব ধরনের Coin সহজেই সেল করতে নিচের **SELL COIN -** বাটনে ক্লিক করুন! 👇"
    )
    
    markup = types.InlineKeyboardMarkup()
    # আপনার নতুন বটের ইউজারনেম অনুযায়ী অ্যাপ লিঙ্ক
    app_url = "https://t.me/niva_buyer_zone2_bot/app" 
    btn = types.InlineKeyboardButton("🛒 SELL YOUR COIN -", url=app_url)
    markup.add(btn)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ৫. ব্রডকাস্ট সিস্টেম (মেসেজ ১ বার যাওয়ার জন্য ফিক্সড)
@bot.message_handler(func=lambda message: message.from_user.id in ADMIN_IDS)
def broadcast(message):
    if message.text.startswith("SEND:"):
        msg_to_send = message.text.replace("SEND:", "").strip()
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                users = f.read().splitlines()
            success = 0
            for uid in users:
                try:
                    bot.send_message(uid, msg_to_send)
                    success += 1
                except:
                    continue
            bot.reply_to(message, f"✅ সফল! {success} জন ইউজার মেসেজ পেয়েছে।")
    else:
        bot.reply_to(message, "⚠️ মেসেজ পাঠাতে লিখুন- \n`SEND: আপনার মেসেজ`", parse_mode="Markdown")

# ৬. ডুপ্লিকেট মেসেজ বন্ধ করার মেইন রানার
if __name__ == "__main__":
    # থ্রেডিং ব্যবহার করে ওয়েব সার্ভার চালু
    t = threading.Thread(target=run)
    t.daemon = True # যাতে মেইন প্রোগ্রাম বন্ধ হলে এটাও বন্ধ হয়
    t.start()
    
    print("Bot is starting on Katabump/PC...")
    
    # skip_pending=True দিলে পুরনো মেসেজ ২ বার যাবে না
    try:
        bot.polling(none_stop=True, skip_pending=True, timeout=60)
    except Exception as e:
        print(f"Error: {e}")