class user:

    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password
        self.count = 0
        self.wins = 0
        self.words = {"", ""}


    def __str__(self):
        return f"{self.name}:{self.id}:{self.password}:{self.count}:{self.wins}:{self.words}"
