#מחלקת משתשמש
class User:
    def __init__(self, name, tz, password, count_play, words, count_win):
        self.name = name
        self.tz = tz
        self.password = password
        self.count_play = count_play
        self.words = words
        self.count_win = count_win

    def __str__(self):
        return (f"name:{self.name}; tz:{self.tz}; password:{self.password}; count_play:{self.count_play}; words:{self.words};"
                f" count_win:{self.count_win}")
