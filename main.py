import telebot
from datetime import datetime

# --- CONFIGURATION ---
API_TOKEN = '8358819354:AAHt2eMudQetDCHaGIOIhMWMrLHwZoPZYOg'
TARGET_CHAT_ID = '-1003766388585'
# Add your own Telegram User ID here if you want to be the only one who can use it
# Example: ADMIN_IDS = [12345678, 87654321]
ADMIN_IDS = [] 

bot = telebot.TeleBot(API_TOKEN)

def log_to_file(user_id, username, first_name, action):
    """Saves every interaction to log.txt"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] ID: {user_id} | User: {username} | Name: {first_name} | Action: {action}\n"
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(entry)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    # Check if Admin list is used; if empty, anyone can use it
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Access Denied. You are not authorized.")
        return

    msg = (
        "📸 **Photo Forwarder Active**\n\n"
        "Send any photo here. I will instantly forward it to the channel:\n"
        f"`{TARGET_CHAT_ID}`"
    )
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id
    
    # Security Check
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        return

    try:
        # Get user details
        fname = message.from_user.first_name
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        
        # Log the action
        log_to_file(user_id, uname, fname, "Sent Photo")

        # Get the photo (last index is highest quality)
        file_id = message.photo[-1].file_id
        
        caption = (
            f"✅ **New Submission**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 User: {fname}\n"
            f"🆔 ID: `{user_id}`\n"
            f"🔗 User: {uname}"
        )

        # Forward to Channel
        bot.send_photo(TARGET_CHAT_ID, file_id, caption=caption, parse_mode='Markdown')
        
        # Feedback to user
        bot.reply_to(message, "🚀 **Forwarded to Channel!**")
        print(f"Log: Forwarded photo from {fname}")

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Error sending photo to channel. Make sure I am an Admin there!")

if __name__ == "__main__":
    print("----------------------------")
    print("BOT IS ONLINE")
    print("Press Ctrl+C to stop")
    print("----------------------------")
    bot.infinity_polling()
