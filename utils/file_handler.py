import os
from pyrogram import Client
from tqdm import tqdm

# Function to upload files (large files handled by Pyrogram)
async def handle_file_upload(app: Client, update, context, file_path, filename, user_id):
    """
    Uploads the downloaded file to Telegram with the given filename and optional thumbnail.
    """
    file_size = os.path.getsize(file_path)
    max_file_size = 4 * 1024 * 1024 * 1024  # 4GB for Telegram Premium accounts

    # If file exceeds size, use the user account to upload directly
    if file_size > max_file_size:
        await update.message.reply_text(f"The file is too large to upload through the bot. Uploading it via your account instead.")
        
        with open(file_path, "rb") as f:
            upload = await app.send_document(
                user_id,
                f,
                caption=filename
            )
        return upload.document.file_id

    # For normal size files, upload them directly
    progress_bar = tqdm(total=file_size, unit="B", unit_scale=True, desc=filename)
    
    with open(file_path, "rb") as f:
        upload = await app.send_document(
            user_id,
            f,
            caption=filename
        )
        progress_bar.update(file_size)
        progress_bar.close()

    return upload.document.file_id
    return upload.document.file_id
