import os
import logging
import zipfile
from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from utils.downloader import download_file
from utils.file_handler import handle_file_upload
from config.settings import TELEGRAM_API_KEY, API_ID, API_HASH, SESSION_STRING, DUMP_CHANNEL_ID

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client (User API)
app = Client("my_bot_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

thumbnail_path = None
users_progress = {}

# Command to set thumbnail for videos
async def set_thumb(update: Update, context: CallbackContext):
    """Command to set a custom thumbnail for videos."""
    user_id = update.message.from_user.id
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file = await update.message.reply_to_message.photo[-1].get_file()  # Await file retrieval
        thumbnail_path = await file.download()  # Download file synchronously
        context.user_data['thumbnail'] = thumbnail_path
        await update.message.reply_text(f"Thumbnail set successfully for user {user_id}.")
    else:
        await update.message.reply_text("Please reply to a photo with /setthumb to set the thumbnail.")

# Command to download file from a link, upload to dump channel, and forward it to the user
async def leech(update: Update, context: CallbackContext):
    """Command to leech a file from a provided URL and upload it to a dump channel."""
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a download link.")
        return

    link = context.args[0]
    user_id = update.message.from_user.id
    filename = f"Tg @StreamersHub {os.path.basename(link)}"
    
    await update.message.reply_text(f"Downloading {filename}...")

    try:
        # Download the file using the downloader utility
        temp_file_path = await download_file(link, user_id)
        
        # Upload the file to the dump channel
        file_id = await handle_file_upload(app, update, context, temp_file_path, filename, DUMP_CHANNEL_ID)
        
        # Forward the uploaded file back to the user
        forwarded_msg = await app.send_document(user_id, file_id, caption=filename)
        
        # Remove the file from VPS after sending
        os.remove(temp_file_path)

        await update.message.reply_text(f"{filename} uploaded and sent to you successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Command to download, unzip, and upload individual files
async def unzipleech(update: Update, context: CallbackContext):
    """Command to leech and unzip a file before uploading its contents."""
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a link to a zip file.")
        return

    link = context.args[0]
    user_id = update.message.from_user.id
    filename = f"Tg @StreamersHub {os.path.basename(link)}"
    
    await update.message.reply_text(f"Downloading and unzipping {filename}...")

    try:
        # Download the zip file
        zip_file_path = await download_file(link, user_id)
        
        # Extract files from the zip
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(f'/tmp/{user_id}_unzipped')
        
        # Upload each file in the zip to the user
        for extracted_file in os.listdir(f'/tmp/{user_id}_unzipped'):
            file_path = os.path.join(f'/tmp/{user_id}_unzipped', extracted_file)
            file_id = await handle_file_upload(app, update, context, file_path, extracted_file, DUMP_CHANNEL_ID)
            await app.send_document(user_id, file_id, caption=extracted_file)
            os.remove(file_path)  # Remove each file after uploading

        os.remove(zip_file_path)  # Remove the original zip file
        await update.message.reply_text(f"All files from {filename} have been uploaded successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Command to greet the user with /start
async def start(update: Update, context: CallbackContext):
    """Command to greet the user and explain bot functionality."""
    await update.message.reply_text("Hello! I'm your file leeching bot. Use /leech <link> to download files.")

def main():
    """Main entry point for the bot."""
    # Run the Pyrogram Client to ensure it's initialized and ready for use
    app.start()  # Start the client (necessary to initialize it properly)

    # Use Application for handling bot interactions
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setthumb", set_thumb))
    application.add_handler(CommandHandler("leech", leech))
    application.add_handler(CommandHandler("unzipleech", unzipleech))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
