import os
import logging
from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from utils.downloader import download_file
from utils.file_handler import handle_file_upload
from config.settings import TELEGRAM_API_KEY, API_ID, API_HASH, SESSION_STRING

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client
app = Client("my_bot_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

thumbnail_path = None

# Command to set thumbnail for videos
async def set_thumb(update: Update, context: CallbackContext):
    global thumbnail_path
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file = update.message.reply_to_message.photo[-1].get_file()
        thumbnail_path = file.download()
        await update.message.reply_text("Thumbnail set successfully.")
    else:
        await update.message.reply_text("Please reply to a photo with /setthumb to set the thumbnail.")

# Command to download file from a link and upload to Telegram
async def leech(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a download link.")
        return

    link = context.args[0]
    filename = f"Tg @StreamersHub {os.path.basename(link)}"
    
    await update.message.reply_text(f"Downloading {filename}...")

    try:
        # Download the file using the downloader utility
        temp_file_path = download_file(link)

        # Upload the file with custom filename
        await update.message.reply_text(f"Uploading {filename}...")
        await handle_file_upload(update, context, temp_file_path, filename, thumbnail_path)

        os.remove(temp_file_path)  # Clean up temporary file
        await update.message.reply_text(f"{filename} uploaded successfully!")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Start the bot with /setthumb and /leech commands
def main():
    # Use Application for handling bot interactions
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Add command handlers
    application.add_handler(CommandHandler("setthumb", set_thumb))
    application.add_handler(CommandHandler("leech", leech))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
