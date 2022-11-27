# bot.py
import os
import sqlite3
import discordBot
import asyncio
import json
from dotenv import load_dotenv
from users import User, Users
from messages import Messages


class DiscordClient(discordBot.Client):
    def __init__(self) -> None:
        intents = discordBot.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        intents.members = True
        self.messageBuffer = []
        super().__init__(intents=intents)
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')

    def run(self):
        super.run(self.TOKEN)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discordBot.message.Message):
        await message.author.send(message.content)
        with sqlite3.connect("Atlas.db") as connection:
            user = Users.getUserFromDiscord(connection, message.author.id)
            if user:
                Messages.addMessage(connection, user.id, message.content, message.created_at)
            elif "!register" in message.content:
                Users.addUser(connection, message.author.name, message.author.id)
                user = Users.getUserFromDiscord(connection, message.author.id)
                Messages.addMessage(connection, user.id, message.content, message.created_at)

    def getMessages(self):
        temp = self.messageBuffer
        self.messageBuffer = []
        return temp


if __name__ == "__main__":
    client = DiscordClient()
