from pyrogram import Client

# Function to upload files (large files handled by Pyrogram)
async def handle_file_upload(update, context, file_path, filename, thumbnail_path):
    """
    Uploads the downloaded file to Telegram with the given filename and optional thumbnail.
    """
    if file_path.endswith(('.mp4', '.mkv', '.avi')):
        # Upload video with thumbnail
        with open(file_path, 'rb') as f:
            if thumbnail_path:
                with open(thumbnail_path, 'rb') as thumb:
                    await context.bot.send_video(update.message.chat_id, f, caption=filename, thumb=thumb)
            else:
                await context.bot.send_video(update.message.chat_id, f, caption=filename)
    else:
        # Upload non-video file
        with open(file_path, 'rb') as f:
            await context.bot.send_document(update.message.chat_id, f, filename=filename)
