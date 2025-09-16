from pyrogram import Client
from telegram import Update
from telegram.ext import CallbackContext
from tqdm import tqdm

# Function to upload files (large files handled by Pyrogram)
async def handle_file_upload(update, context, file_path, filename, user_id):
    """
    Uploads the downloaded file to Telegram with the given filename and optional thumbnail.
    """
    progress_bar = tqdm(total=os.path.getsize(file_path), unit="B", unit_scale=True, desc=filename)
    with open(file_path, "rb") as f:
        upload = await context.bot.send_document(
            user_id,
            f,
            caption=filename
        )
        # Update progress during upload
        progress_bar.update(os.path.getsize(file_path))
        progress_bar.close()
    return upload.document.file_id
