# bot.py
import os
import discord
import json
from dotenv import load_dotenv
from Atlas import Atlas
from users import User, Users


with open("users.json", "r") as f:
    users = json.loads(f.read())

class MyClient(discord.Client):
    def __init__(self, atlas:Atlas, *, intents: discord.Intents, **options) -> None:
        self.atlas = atlas
        super().__init__(intents=intents, **options)
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.message):
        for user in users:
            if str(message.author) == user["discord"]:
                self.atlas.command(message.content, user["id"])
            else:
                print(f'Message from Unknown User -- {message.author}: {message.content} in server:{message.guild}')


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    a = Atlas()

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(a, intents=intents)
    client.run(TOKEN)