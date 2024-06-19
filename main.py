from __future__ import unicode_literals

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import yt_dlp


def delete_file(filepath):
    os.remove(filepath)


def find_mp3_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_in_dir = os.listdir(current_dir)

    for file in files_in_dir:
        if file.endswith(".mp3"):
            return os.path.join(current_dir, file)

    return None


def download_audio(download_link):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([download_link])


class Bot(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("DISCORD_BOT_TOKEN")

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix='!', intents=intents)

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!download"):
            link = message.content[len("!download "):].strip()
            print(f'Extracted link: {link}')
            download_audio(download_link=link)
            file_path = find_mp3_file()
            try:
                if file_path:
                    await message.channel.send(file=discord.File(file_path))
                    delete_file(file_path)
                else:
                    await message.channel.send("No MP3 file found after download.")

            except Exception as e:
                await message.channel.send(f"Error:{e}")

        await self.process_commands(message)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
