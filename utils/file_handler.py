from telegram import Update
from telegram.ext import CallbackContext

def handle_file_upload(update: Update, context: CallbackContext, file_path: str, filename: str, thumbnail_path: str):
    """
    Uploads the downloaded file to Telegram with the given filename and optional thumbnail.
    """
    if file_path.endswith(('.mp4', '.mkv', '.avi')):
        # Upload video with thumbnail
        if thumbnail_path:
            with open(thumbnail_path, 'rb') as thumb:
                context.bot.send_video(update.message.chat_id, video=open(file_path, 'rb'), caption=filename, thumb=thumb)
        else:
            context.bot.send_video(update.message.chat_id, video=open(file_path, 'rb'), caption=filename)
    else:
        # Upload non-video file
        context.bot.send_document(update.message.chat_id, document=open(file_path, 'rb'), filename=filename)
