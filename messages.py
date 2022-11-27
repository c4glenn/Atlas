import datetime
import sqlite3
from users import User, Users

class Message:
    def __init__(self, idNum, user: User, contents, date, source, attachments=[]):
        self.idNum = idNum
        self.user = user
        self.contents = contents
        self.date = date
        self.source = source
        self.attachments = attachments
    def __eq__(self, __o: object) -> bool:
        return __o.idNum == self.idNum
    def __hash__(self) -> int:
        return hash(self.idNum)
    def __str__(self) -> str:
        with sqlite3.connect("Atlas.db") as connection:
            return f"{Users.getUserFromID(connection, self.user.id).name}: '{self.contents}' via {self.source} {f'with {self.attachments} attached' if len(self.attachments) > 2 else ''}"

class Messages:
    def createDB(dbConnection: sqlite3.Connection):
        dbConnection.execute("DROP TABLE Messages")
        dbConnection.execute("""
        CREATE TABLE Messages(
            id INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            contents TEXT,
            date timestamp,
            source TEXT,
            attachments TEXT)""")

    def addMessage(dbConnection: sqlite3.Connection, userID: int, contents: str, date: datetime.datetime, source: str, attachments):
        dbConnection.execute("""
        INSERT INTO Messages(userID, contents, date, source, attachments) VALUES (?,?,?,?,?)
        """, (userID, contents, date, source, str(attachments)))
        return Messages.getMessages(dbConnection, f"SELECT * FROM Messages WHERE userID = {userID} AND date = '{date}'")[0]

    def getMessages(dbConnection, text, params=None):
        if params:
            rows = dbConnection.execute(text, params)
        else:
            rows = dbConnection.execute(text)
        messages = []
        for row in rows:
            messages.append(Message(row[0], Users.getUserFromID(dbConnection, row[1]), row[2], row[3], row[4], row[5]))
        return messages
    
    def getUsersMessages(dbConnection, userID):
        return Messages.getMessages(dbConnection, f"SELECT * from Messages where userID = {userID} ORDER BY date")
    def getAllMessages(dbConnection):
        return Messages.getMessages(dbConnection, "SELECT * FROM Messages")

if __name__ == "__main__":
    DBSTRING = "Atlas.db"
    print(DBSTRING)
    with sqlite3.connect(DBSTRING, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as connection:
        Messages.createDB(connection)
        print("Whats up")
        Messages.addMessage(connection, 0, "Hey guys", datetime.datetime.now(), "tests")
        Messages.addMessage(connection, 0, "NUMBER 2", datetime.datetime.now(), "tests")
        Messages.addMessage(connection, 0, "Wowsers :)", datetime.datetime.now(), "tests")
        for m in Messages.getUsersMessages(connection, 0):
            print(m)