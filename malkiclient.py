import requests
from requests import session
import time
from malkiuser import user

s = r"""  | |  | |
          | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
          |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
          | |  | | (_| | | | | (_| | | | | | | (_| | | | |
          |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                               __/ |
                              |___/

"""
print(s)
session = session()
basic_url = "http://127.0.0.1:5000"  # שמירת כתובת הבסיס- הכתובת עליה השרת רץ

myuser = user("", "", "")


def login():
    name = input("הכנס שם")
    id = input("הכנס ת.זהות")
    password = input("הכנס קוד")
    myuser.name = name
    myuser.id = id
    myuser.password = password
    message = {'name': myuser.name, 'id': myuser.id, 'password': myuser.password}

    # json=message כדי לשלוח את האובייקט בבקשה נשתמש ב:
    response = session.post(f"{basic_url}/login", json=message)  # בקשת post
    if response.status_code == 200:  # אם הבקשה הצליחה
        str = ""
        response1 = session.get(f'{basic_url}/get_cookie')  # , cookies=cookie
        if response1.status_code == 200:
            response2 = response1.text.split(":")

            for u in response2:
                # print(u)
                str += f"{u}:"
        myuser.countgames = int(response2[3])
        myuser.conntwins = int(response2[4])
        s = {""}
        for x in response2[5].replace("{", "").replace("}", "").replace("\n", "").replace('"', "").replace('"',
                                                                                                           "").replace(
            "\\\\n", "").replace('\\\\\\\\n', "").split(","):
            s.add(x)
        # use.words = s
        myuser.words = s
        #print(myuser.words)
        print(f" שלום ל {message['name']}")  # הדפסת התוכן
    else:
        response = session.post(f"{basic_url}/register", json=message)  # בקשת post
        if response.status_code == 200:  # אם הבקשה הצליחה
            print(f"ברוכים הבאים ל{name}")  # הדפסת התוכן


arrman = [r""""x-------x
                        """,
          r"""
x-------x
|
|
|
|
|
""", r"""
x-------x
|       |
|       0
|
|
|

""", r"""
x-------x
|       |
|       0
|       |
|
|
""", r"""
x-------x
|       |
|       0
|      \|/ 
|
|
""", r"""x-------x
|       |
|       0
|      \|/ 
|      \
|
""", r"""x-------x
|       |
|       0
|      \|/ 
|      \ / 
|
"""]


def play():
    try:
        num = int(input("הכנס מספר"))
        message = {'num': num}
        response = session.post(f"{basic_url}/play", json=message)  # יצירת בקשת get
        str = ""
        str1 = ""
        faild = 0
        chararr = []
        myletters = ""
        goodword = []
        good = 0
        revach = 0
        if response.status_code == 200:  # אם הבקשה הצליחה
         word = response.json()  # הדפסת התוכן- הפעולה ההפוכה מהכנסה ל-json
         if word == "cokee failed":
            print("no")
         else:
            for a in word:
                if a != " ":
                    str += '_'
                else:
                    str += " "
                    revach += 1

            print(str)
            # a = input("הכנס אות")
            x = 0
            print(f"אורך המילה{len(word)}")
            while faild < 7 and good != (len(word) - revach):

             a = input("הכנס אות")
             while myletters.__contains__(a):
                a = input("הכנס אות")
             myletters += f"{a},"

             print(myletters)

             if a in word:
                for b in word:
                    if b == a:
                        good += 1
                        print(f"הצלחה מספר{good}")
                    else:
                        good += 0

             else:
                faild += 1
                print(arrman[x])
                x += 1
    # print("המשחק נגמ ")
             if good == len(word) - revach:
              myuser.words.add(word)
              myuser.conntwins += 1
              print(f"מספר הנצחונות {myuser.conntwins}")
              myuser.countgames += 1
              print(f" מספר המשחקים{myuser.countgames}")

            else:
             myuser.countgames += 1
             print(myuser.countgames)


             print("המשחק נגמר!!!אתה שחקן אלוף")
             end = int(input(
        "אם ברצונך להמשיך למשחק נוסף הקש 1 ,אם ברצונך לראות את ההסטוריה שלך הקש 2 ,אם ברצונך להתנתק הקש 3 "))
             if end == 1:
              update()
              play()
             elif end == 2:
              update()
              file = open('f.txt', 'r')  # פתיחת הקובץ לקריאה- ברירת המחדל של פונקציית open
              s = file.readlines()
              for s1 in s:
               s2 = s1.split(":")
               if s2.__len__() > 1:
                if s2[1] == myuser.id and s2[2] == myuser.password:
                    print(f"ההסטוריה שלך-  {s2}")
                    print(f"שם:{myuser.name},תז:{myuser.id},קוד:{myuser.password},מספר הנצחונות {myuser.conntwins}, מספר המשחקים{myuser.countgames},המילם:{myuser.words}")

             else:
              exit()
        else:
         print(f"Error: {response.status_code}")

    except ValueError as e:
      print(e)
    except:
     print("Error")


def update():
    print("clientupdate")
    w = ""
    cg = myuser.countgames
    cw = myuser.conntwins
    for x in myuser.words:
        w += x + ','
    print(w)
    message = {'name': myuser.name, 'id': myuser.id, 'password': myuser.password, 'countgames': cg,
               'countwins': cw, 'words': w}
    # json=message כדי לשלוח את האובייקט בבקשה נשתמש ב:
    response = session.post(f"{basic_url}/update", json=message)  # בקשת post
    if response.status_code == 200:
        print('העדכון הצליח')
    else:
        print("qwerty")


def exit():
    message = {'name': myuser.name, 'id': myuser.id, 'password': myuser.password}
    response = session.post(f"{basic_url}/exit", json=message)  # בקשת post
    if response.status_code == 200:
        print('היציאה הצליחה')
    else:
        print("טעות")


def main():
    login()
    play()


if __name__ == '__main__':
    main()
# def set_c
