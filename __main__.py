
from telethon import TelegramClient, events
from decouple import config
import subprocess
import os

API_ID = int(config("API_ID"))
API_HASH = config("API_HASH")
BOT_TOKEN = config("BOT_TOKEN")

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("Send a video file to compress it to 360p.")

@bot.on(events.NewMessage())
async def handle_video(event):
    if not event.video:
        return
    msg = await event.respond("📥 Downloading...")
    file_path = await event.download_media()

    output_file = "compressed.mp4"
    cmd = f'ffmpeg -i "{file_path}" -preset ultrafast -c:v libx264 -s 640x360 -pix_fmt yuv420p -crf 28 -c:a aac -b:a 64k -ac 2 -threads 2 "{output_file}" -y'
    await msg.edit("🗜 Compressing...")
    subprocess.run(cmd, shell=True)

    await msg.edit("📤 Uploading...")
    await event.reply(file=output_file, caption="✅ Compressed to 360p")

    os.remove(file_path)
    os.remove(output_file)

bot.run_until_disconnected()
