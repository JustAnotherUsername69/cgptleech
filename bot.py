import os
import logging
from pyrogram import Client
from telegram.ext import Updater, CommandHandler, CallbackContext
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
def set_thumb(update, context):
    global thumbnail_path
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file = update.message.reply_to_message.photo[-1].get_file()
        thumbnail_path = file.download()
        update.message.reply_text("Thumbnail set successfully.")
    else:
        update.message.reply_text("Please reply to a photo with /setthumb to set the thumbnail.")

# Command to download file from a link and upload to Telegram
def leech(update, context):
    if len(context.args) < 1:
        update.message.reply_text("Please provide a download link.")
        return

    link = context.args[0]
    filename = f"Tg @StreamersHub {os.path.basename(link)}"
    
    update.message.reply_text(f"Downloading {filename}...")

    try:
        # Download the file using the downloader utility
        temp_file_path = download_file(link)

        # Upload the file with custom filename
        update.message.reply_text(f"Uploading {filename}...")
        handle_file_upload(update, context, temp_file_path, filename, thumbnail_path)

        os.remove(temp_file_path)  # Clean up temporary file
        update.message.reply_text(f"{filename} uploaded successfully!")

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Start the bot with /setthumb and /leech commands
def main():
    # Use your Bot API for command handling (for receiving commands only)
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("setthumb", set_thumb))
    dispatcher.add_handler(CommandHandler("leech", leech))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

    try:
        # Download the file using the downloader utility
        temp_file_path = download_file(link)

        # Upload the file with custom filename
        update.message.reply_text(f"Uploading {filename}...")
        handle_file_upload(update, context, temp_file_path, filename, thumbnail_path)

        os.remove(temp_file_path)  # Clean up temporary file
        update.message.reply_text(f"{filename} uploaded successfully!")

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Error downloading file: {str(e)}")

# Start the bot with /setthumb and /leech commands
def main():
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("setthumb", set_thumb))
    dispatcher.add_handler(CommandHandler("leech", leech))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
