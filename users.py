import json

class User:
    def __init__(self, id, name, discord) -> None:
        self.id = id
        self.name = name
        self.discord = discord

class Users:
    def __init__(self):
        with open("users.json", "r") as f:
            self.users = [User(a["id"], a["name"], a["discord"]) for a in json.loads(f.read())]
    def getUserFromID(self, id: int) -> User:
        temp = None
        for user in self.users:
            if user.id == id:
                temp = user
        return temp