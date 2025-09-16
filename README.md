# Telegram Bot for File Leeching

## Features

- Download files from any given URL using the `/leech <url>` command.
- Upload files with custom names to Telegram.
- Set a thumbnail for videos using the `/setthumb` command.

## Installation

1. Clone this repository.

   ```bash
   git clone https://github.com/yourusername/telegram-bot.git
   cd telegram-bot
   ```

2. Install the required dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Edit the `config/settings.py` file to set your Telegram Bot API key.

4. Run the bot.

   ```bash
   python bot.py
   ```

## Commands

- `/setthumb` – Reply to a photo to set it as a thumbnail.
- `/leech <link>` – Download a file from the provided URL and upload it to Telegram with a custom filename.
