import os
from tqdm import tqdm
from pyrogram import Client

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

# Function to send a progress bar during file upload
async def send_progress_bar(update, context, total_size, filename, user_id):
    """
    Sends progress bar during the upload process.
    """
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=filename)

    # Send file in chunks while updating the progress bar
    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):  # Read in 1 MB chunks
            await context.bot.send_document(user_id, chunk)
            progress_bar.update(len(chunk))

    progress_bar.close()
