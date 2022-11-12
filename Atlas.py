import json
from users import User, Users

class Atlas:
    def __init__(self):
        self.users = Users()

    def command(self, message: str, userId: int):
        print(f"message: {str} from user: {self.users.getUserFromID(userId).name}")