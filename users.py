import sqlite3

class User:
    def __init__(self, id, name, discord) -> None:
        self.id = id
        self.name = name
        self.discord = discord
    def __str__(self) -> str:
        return f"USER {self.id}: {self.name} discord is {self.discord}"

class Users:
    def makeDB(dbConnection:sqlite3.Connection) -> None:
        dbConnection.execute("DROP TABLE IF EXISTS Users")
        dbConnection.execute("""
                CREATE TABLE Users(
                id INTEGER PRIMARY KEY,
                name TEXT,
                discord TEXT)""")
            
    def getUserFromID(dbConnection: sqlite3.Connection, ID: int) -> User:
        for row in dbConnection.execute(f"Select * from Users where id = {ID}"):
            return User(row[0], row[1], row[2])
        else:
            return User(-1, "No User", "None")

    def getUserFromDiscord(dbConnection: sqlite3.Connection, discord: int) -> User:
        for row in dbConnection.execute(f"Select * from Users where discord = {discord}"):
            return User(row[0], row[1], row[2])
    def getAllUsers(dbConnection: sqlite3.Connection):
        for row in dbConnection.execute(f"Select * from Users"):
            print(row)
    def addUser(dbConnection: sqlite3.Connection, user:User) -> None:
        Users.addUser(dbConnection, user.name, user.discord)
    def addUser(dbConnection:sqlite3.Connection, userName:str, userDiscord:int):
        dbConnection.execute(f"INSERT INTO Users (name, discord) VALUES (?, ?)", (userName,userDiscord))

if __name__ == "__main__":
    DBPATH = "Atlas.db"
    with sqlite3.connect(DBPATH) as connection:
        Users.makeDB(connection)
        Users.addUser(connection, "Philip", "253609533295951874")
        Users.addUser(connection, "Kate", "522627935166005250")
        Users.getAllUsers(connection)
        
