from ctypes import c_char

from requests import session
from User import  User
import  json, time
session = session()
basic_url = "http://127.0.0.1:5000"
str = "" # מחרוזת הפסים או האותיות המגולות
set_firm = {}
count_err = 0 # ספירת הטעויות
word = "" # המילה המוגרלת
current_user = User # המשתמש הנוכחי
list_drow =[] # רשימת הציורים של ההמן תלוי
list_drow.append(r"""x-------x""")
list_drow.append(r"""x-------x
|
|
|
|
|""")
list_drow.append(r"""x-------x
|       |
|       0
|
|
|""")
list_drow.append(r"""x-------x
|       |
|       0
|       |
|
|""")
list_drow.append(r"""x-------x
|       |
|       0
|      \|/ 
|
|""")
list_drow.append(r""""x-------x
|       |
|       0
|      \|/ 
|      \
|""")
list_drow.append(r"""x-------x
|       |
|       0
|      \|/ 
|      \ / 
|""")

def decorator(func):
    def wrapper():
        if(session.get(f"{basic_url}/get_cookie").text.__eq__("Cookie not found")): # אם לא קיימת עוגיה
            while True: # כל עוד הוא לא נעצר
                print("you need login again")
                while True:
                    try:
                        tz = input("enter tz:")
                        if tz.__len__() != 9:
                            raise DivideError("tz invalid")
                        break
                    except DivideError as e:
                        print(e)
                if not current_user.tz.__eq__(tz): # אם לא הכניס את אותו תז עליה שיחק עד עכשיו
                    while True:
                        try:
                            yes_no = int(input("הכנסת תז אחרת אם הנך רוצה לשחק על תז זו הקש 1 ןתצטרך להרשם שוב אם הינך רוצה להכניס תז הקש 2"))  # שואל אם רוצה לתקן
                            if yes_no != 1 and yes_no != 2:
                                raise DivideError("you need choose 1 or 2")
                            break
                        except ValueError as e:
                            print(e)
                        except DivideError as e:
                            print(e)
                    if yes_no == 1: # אם לא רוצה לתקן שולח אותו שוב להתחברות אם כן ירצה לתקן יכנס שוב ללולאה
                        login()
                else: # אם הכניס את אותה תז איתה שחק עד עכשיו מכין עוגיה חדשה על שמו של המשתמש הנוכחי
                    obj = {'all_user': json.dumps(current_user.__dict__)}  # מכין את האוביקט שישלח לעוגיה
                    response = session.post(f"{basic_url}/set_cookie", json=obj)  # מכין עוגיה
                    if response.status_code != 200:
                        print(response.status_code)
                    print("login again sccsesful you continu the play")
                    break # עוצר את הלולאה
        func()
    return 
    
class DivideError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

# פונקציית התחברות
def login():
    while True:
        try:
            tz = input("enter tz:")
            if tz.__len__() != 9:
                raise DivideError("tz invalid")
            break
        except DivideError as e:
            print(e)
    obj = {"tz": tz} # שולח את הת:ז לפונקציה בשרת
    response = session.post(f"{basic_url}/login", json = obj)
    if response.status_code == 200:
        if not response.text.__eq__("login"): # אם נמשתמש כבר רשום במערכת
            obj_dict = json.loads(response.text) # ממיר את מה שחזר לאוביקט מסוג מלקת משתמש
            global  current_user
            current_user = User(**obj_dict)
            print(f"hellow {current_user.name}") # כותב את שמו
            obj = {'all_user': response.text} # מכין את האוביקט שישלח לעוגיה
            response = session.post(f"{basic_url}/set_cookie", json=obj) # מכין עוגיה
            if response.status_code != 200:
                print(response.status_code)
            random_word_cleint()  # שולח לפונקציית הגרלת המילה
        else: # אם הת"ז אינה רשומה במערכת
            register(tz) # שולח לפונקציית הרשמה
    else:
        print(response.status_code)

# פונקציית הרשמה
def register(tz): # מקבל את הת"ז שהכניס בפונקציית התחברות
    name = input("enter name:") # מקבל שם
    password = input("enter password:") # מקבל סיסמה
    obj = {"name": name, "tz": tz, "password": password, "count_play" : 0, "words" : "", "count_win": 0} # האוביקט שאותו נשלח לפונקציית הרשמה בשרת
    response = session.post(f"{basic_url}/register",json = obj) # מפעיל את הפונקציה בשרת
    if response.status_code == 200: # אם הצליח
        global  current_user
        obj_dict = json.loads(response.text)  # ממיר את מה שחזר לאוביקט מסוג מלקת משתמש
        current_user = User(**obj_dict)
        print(f"hellow {current_user.name}")  # כותב את שמו
        obj = {'all_user': response.text}
        response = session.post(f"{basic_url}/set_cookie",json = obj)
        random_word_cleint() # שולח לפונקציית הגרלת המילה
    else:
        print(response.status_code)

# פנוקציה המקבלת מהשרת מילה ומדפיסה מספר פסים מתאים ומפעילה את פונקציית המשחק
@decorator
def random_word_cleint():
    while True:
        try:
            num = int(input("enter number:"))
            break
        except ValueError as e:
            print(e)
    response = session.get(f"{basic_url}/random_word/{int(num)}") # ניתוב לפונקציה מהשרת
    if response.status_code == 200:
        global  word, str, count_err, current_user, set_firm
        count_err = 0
        set_firm = {''}
        word = response.text # הצבת הערך שהתקבל
        print(response.text)
        str = "_ " # הפסים או האותיות של המילה המוגרלת
        str = str * (response.text.__len__() - 1)
        print(str)
        user = User(current_user.name, current_user.tz, current_user.password,
                    current_user.count_play + 1, " ".join(set((f"{current_user.words} {word}").split())).strip(),
                    current_user.count_win) # מכין משתמש חדש מעודכן - מוסיף למשתמש הנוכחי משחק אחד את המילה שהוגרלה
        current_user = user # מעדכן את המשתמש הנוכחי בתוספות
        # מעדכן את המשתמש בקובץ
        response = session.post(f"{basic_url}/update_file",json = json.dumps(current_user.__dict__))  # ניתוב לפונקציה מהשרת
        if response.status_code != 200:
            print(response.status_code)
        # file_read = open("./Store.txt", "r")
        # lines_file = file_read.readlines()
        # for l_n in lines_file:
        #     obj_dict = json.loads(l_n)  # המרה לאוביקט משתמש
        #     user = User(**obj_dict)
        #     if user.tz == (current_user.tz):
        #         lines_file.remove(l_n)
        #         continue
        # lines_file.append(json.dumps(current_user.__dict__))
        # file_write = open("./Store.txt", 'w')
        # print("".join(lines_file), file=file_write)
        # file_read.close()
        # file_write.close()
    else:
        print(response.status_code)
    play() # שולח לפונקציית המשחק

# פונקציית ניהול המשחק
@decorator
def play():
    global  count_err, str, current_user
    while count_err < 7: # כל עוד לא הגיע ל7 טעויות
        if("_" not in str):
            print("your win !!!!!!!!!!!!!!!!!!!")
            user = User(current_user.name, current_user.tz, current_user.password,
            current_user.count_play,current_user.words,
            current_user.count_win + 1) # מעדכן את המשתמש עם ניצחון נוסף
            current_user = user
            # מעדכן אותו בקובץ
            response = session.post(f"{basic_url}/update_file",json.dumps(current_user.__dict__))  # ניתוב לפונקציה מהשרת
            if response.status_code != 200:
                print(response.status_code)
            # file_read = open("./Store.txt", "r")
            # lines_file = file_read.readlines()
            # for l_n in lines_file:
            #     obj_dict = json.loads(l_n)  # המרה לאוביקט משתמש
            #     user = User(**obj_dict)
            #     if user.tz == (current_user.tz):
            #         lines_file.remove(l_n)
            #         continue
            # lines_file.append(json.dumps(current_user.__dict__))
            # file_write = open("./Store.txt", 'w')
            # print("".join(lines_file), file=file_write)
            # file_read.close()
            # file_write.close()
            break
        while True:
            try:
                char = input("enter char:")
                if not ascii('a') <= ascii(char) <= ascii('z') and not ascii('A') <= ascii(char) <= ascii('Z') or char.__len__() != 1\
                        or char in set_firm:
                    raise DivideError("you need enter tav than no firm")
                break
            except DivideError as e:
                print(e)
        set_firm.add(char)
        if not char in word:
            print(list_drow[count_err])
            count_err = count_err + 1
            print(f"your have add {7 - count_err} mistake")
            print(str)
        else:
            split_str = str.split(" ")
            start = 0
            while word.find(char, start) != -1:
                split_str[word.find(char, start)] = char
                start = word.find(char, start) + 1
            new_str = " ".join(split_str)
            str = new_str
            print(new_str)
    if count_err == 7:
        print("dont give up")
    while True:
        try:
            more_history_exit = int(input("enter 1 to play again. enter 2 see history. enter 3 exit"))
            if ascii('1') <=  ascii(more_history_exit) <= ascii('3'):
                raise DivideError("you need choose 1 or 2 or 3")
            break
        except ValueError as e:
            print(e)
        except DivideError as e:
            print(e)
    if more_history_exit == 1:
        random_word_cleint()
    if more_history_exit == 2:
        history()
    else:
        print("good bay")

@decorator
def history():
    print(f"You have played {current_user.count_play} times. You won {current_user.count_win} times. "
          f"The words that were in your games {current_user.words}")
    while True:
        try:
            more_history_exit = int(input("enter 1 to play again. enter 2 see history. enter 3 exit"))
            if ascii('1') <=  ascii(more_history_exit) <= ascii('3'):
                raise DivideError("you need choose 1 or 2 or 3")
            break
        except ValueError as e:
            print(e)
        except DivideError as e:
            print(e)
    if more_history_exit == 1:
        random_word_cleint()
    if more_history_exit == 2:
        print(f"You have played {current_user.count_play} times. You won {current_user.count_win} times. "
            f"The words that were in your games {current_user.words}")
    else:
        print("good bay")

if __name__ == "__main__":
    logo = r"""	        _    _
           | |  | |
           | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
           |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
           | |  | | (_| | | | | (_| | | | | | | (_| | | | |
           |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                __/ |
                               |___/
    """
    print(logo)
    login()

