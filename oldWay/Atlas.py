import json
import sqlite3
from users import User, Users
from discordBot import DiscordClient
from messages import Message, Messages
import datetime
import threading
from queue import Queue

UseDiscord = True

class DiscordThread(threading.Thread):
    def __init__(self, queue: Queue, args=(), kwargs=None):
        super().__init__(group=None, args=args, daemon=True, kwargs=kwargs)
        self.queue = queue

    def run(self):
        print(threading.current_thread().name)
        self.dc = DiscordClient()
        while True:
            if(self.queue.qsize() >= 1):
                val = self.queue.get_nowait()
                print(threading.current_thread().name, val)

class Atlas:
    def __init__(self):
        self.users = Users()
        self.lastCheck = datetime.datetime.now()
        self.connection = None
        self.messageQueue = Queue()
        self.connect()
        self.startDiscord()
        self.lastMessages = []

        
    def startDiscord(self):
        if UseDiscord:
            t = DiscordThread(self.messageQueue)
            t.start()

    def connect(self):
        if(self.connection):
            self.connection.close()
        self.connection:sqlite3.Connection = sqlite3.connect("Atlas.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.lastConnected = datetime.datetime.now()

    def tooLongThenConnect(self):
        if datetime.datetime.now() > self.lastConnected + datetime.timedelta(0, 0, 0, 0, 1, 0): #change to 0 0 0 0 0 1 
            self.connect()


    def command(self, message: Message):
        if message.date > datetime.datetime.now() - datetime.timedelta(0, 0, 0, 0, 30):
            print(f"message: {message.contents} from user: {message.user.name}")
    

    def getMessages(self):
        lastM = self.lastMessages
        messages = Messages.getAllMessages(self.connection)
        self.lastMessages = messages
        messages = list(set(messages) - set(lastM))
        for m in messages:
            self.command(m)     

    def process(self):
        while True:
            self.tooLongThenConnect()
            self.getMessages()

if __name__ == "__main__":
    a = Atlas()
    a.process()
