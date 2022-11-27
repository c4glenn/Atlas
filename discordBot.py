import discord
import os
from dotenv import load_dotenv
import asyncio
from queue import Queue
import queue
from discord.ext import tasks, commands

class DiscordThingy(commands.Bot):
    def __init__(self, inQueue: Queue, outQueue: Queue, **options) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        intents.members = True
        super().__init__(intents=intents, command_prefix="!", **options)
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.MessageQueue = outQueue
        self.sendQueue = inQueue
    def run(self, reconnect: bool = True) -> None:
        return super().run(self.TOKEN, reconnect=reconnect)
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message: discord.message.Message):
        if message.author == self.user:
            return
        try:
            self.MessageQueue.put(message, block=False)
        except:
            print(f"Failed to enqueue {message.author.name}'s message {message.content}")
    async def setup_hook(self):
        self.loop.create_task(self.get_messages())
    async def get_messages(self):
        while True:
            try:
                a = self.sendQueue.get_nowait()
                user = await self.fetch_user(a[0])
                msg = await user.send(a[1])
            except queue.Empty:
                pass
            await asyncio.sleep(1)
