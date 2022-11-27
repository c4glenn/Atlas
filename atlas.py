from discordBot import DiscordThingy
import threading
import queue
from users import User, Users
from messages import Message, Messages
import sqlite3
import discord

DBSTRING = "Atlas.db"

class Atlas:
    def __init__(self) -> None:
        self.send = queue.Queue()
        self.recieve = queue.Queue()
        self.dc = DiscordThingy(inQueue = self.send, outQueue=self.recieve)
        self.connection = sqlite3.connect(DBSTRING, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    def start(self) -> None:
        a = threading.Thread(target=self.dc.run)
        a.start()
        self.runLoop()

    def getMessages(self) -> discord.Message:
        try:
            return self.recieve.get_nowait()
        except queue.Empty:
            pass

    def sendDiscord(self, discordID, content):
        try:
            self.send.put_nowait((discordID, content))
        except queue.Full:
            print(f"Failed to send {content} to {discordID}")

    def process(self, message:Message):
        print(message)
        return f"Message Recieved"

    def command(self, message: Message):
        if(message.source == "discord"):
            response = self.process(message)
            self.sendDiscord(message.user.discord, response)

    def discordHandler(self) -> None:
        m = self.getMessages()
        if(m):
            user = Users.getUserFromDiscord(self.connection, m.author.id)
            message = Messages.addMessage(self.connection, user.id, m.content, m.created_at, "discord", m.attachments)
            self.command(message)
    
    def runLoop(self) -> None:
        while True:
            self.discordHandler()
            

if __name__ == "__main__":
    a = Atlas()
    a.start()