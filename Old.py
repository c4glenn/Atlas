import discord
import os
from dotenv import load_dotenv
import asyncio

class DiscordThingy(discord.Client):
    def __init__(self, **options) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        intents.members = True
        super().__init__(intents=intents, **options)
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
    async def start(self, reconnect: bool = True) -> None:
        return await super().start(self.TOKEN, reconnect=reconnect)
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message: discord.message.Message):
        print(f"{message.author.id} said {message.content}")


class Atlas:
    def __init__(self) -> None:
        self.dc = DiscordThingy()
        asyncio.create_task(self.dc.start)
        


if __name__ == "__main__":
    a = Atlas()