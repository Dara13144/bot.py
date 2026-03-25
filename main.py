import telebot
from datetime import datetime, timedelta
import time

# --- CONFIGURATION ---
API_TOKEN = '8588375535:AAEp9ksw9nH0FHHIgoQZI2MYXLary3YTH70'
TARGET_CHAT_ID = '-1003766388585'

bot = telebot.TeleBot(API_TOKEN)

# User Tracking for Spam Protection (Cooldown)
user_cooldowns = {}

def log_activity(user_id, username, first_name, status):
    """Saves every interaction to log.txt with a timestamp."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{now}] ID: {user_id} | User: {username} | Name: {first_name} | Status: {status}\n"
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"File Error: {e}")

@bot.message_handler(commands=['start'])
def welcome_user(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🙏 **សួស្ដី {user_name}!**\n\n"
        "សូមផ្ញើរូបភាពមកកាន់ទីនេះ ដើម្បីបញ្ជូនទៅកាន់ Channel។\n"
        "Please send a photo here to forward it to the channel."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_incoming_photo(message):
    uid = message.from_user.id
    fname = message.from_user.first_name
    uname = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    # Spam Protection: 3-second cooldown between photos
    if uid in user_cooldowns:
        last_time = user_cooldowns[uid]
        if datetime.now() - last_time < timedelta(seconds=3):
            bot.reply_to(message, "⚠️ **Slow down!** Please wait a few seconds before sending another photo.")
            return

    user_cooldowns[uid] = datetime.now()

    try:
        # Get highest resolution photo
        file_id = message.photo[-1].file_id
        
        # Professional Dara Dev Caption
        caption_text = (
            f"📥 **NEW PHOTO SUBMISSION**\n"
            f"⚡──────────────────⚡\n"
            f"👤 **Name:** {fname}\n"
            f"🆔 **User ID:** `{uid}`\n"
            f"🔗 **Profile:** {uname}\n"
            f"📅 **Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"⚡──────────────────⚡\n"
            f"📍 *System by Dara Dev*"
        )

        # Forward to Channel
        bot.send_photo(
            chat_id=TARGET_CHAT_ID,
            photo=file_id,
            caption=caption_text,
            parse_mode='Markdown'
        )

        log_activity(uid, uname, fname, "SUCCESS: Photo Forwarded")
        bot.reply_to(message, "✅ **រួចរាល់!** រូបភាពត្រូវបានបញ្ជូនទៅ Channel។\nForwarded successfully!")

    except Exception as e:
        log_activity(uid, uname, fname, f"ERROR: {str(e)}")
        bot.reply_to(message, "❌ **Error:** មិនអាចបញ្ជូនបានទេ។ Admin ត្រូវតែបន្ថែម Bot ចូលក្នុង Channel។")
        print(f"System Error: {e}")

if __name__ == "__main__":
    print("---------------------------------------")
    print("🚀 DARA DEV: PHOTO SYSTEM ONLINE")
    print(f"Target Channel: {TARGET_CHAT_ID}")
    print("Press Ctrl+C to shutdown")
    print("---------------------------------------")
    
    # infinity_polling ensures it stays online during network drops
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
