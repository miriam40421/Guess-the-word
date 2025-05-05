class OneTwoThree(Exception):  # המחלקה צריכה לרשת ממחלקת Exception
    """ exception for less than 3"""

    def __init__(self, message=" small than 3"):
        self.message = message
        super().__init__(self.message)  # שליחת ההודעה למחלקת האב


import requests
from requests import session
import time
from hugmam import user

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

# login
use = user("", 0, 0)


def login():
    a, b, c = input("enter name:"), input("enter id:"), input("enter password:")
    use.name = a
    use.id = b
    use.password = c
    message = {'name': use.name, 'id': use.id, 'password': use.password};
    response = session.post(f"{basic_url}/login", json=message)  # בקשת post
    if response.status_code == 200:  # אם הבקשה הצליחה
        print("hellow!!!!!!!!!!!")
        res = session.get(f'{basic_url}/get_cookie')  # , cookies=cookie
        if res.status_code == 200:
            user = res.text.split(':')
            use.name = user[0].replace('"', "")
            use.id = user[1]
            use.password = user[2]
            use.count = int(user[3])
            use.wins = int(user[4])
            s = {""}
            for x in user[5].replace("{", "").replace("}", "").replace("\n", "").replace('"', "").split(","):
                s.add(x)
            use.words = s
            print(use.__str__())
        else:
            print("👍😍")



    # else:
    # sign
    # if response.status_code == 404:  # אם הבקשה הצליחה
    else:
        response = session.post(f"{basic_url}/sign_in", json=message)  # בקשת post
        if response.status_code == 200:
            print("welcome to our Atar!!!!!!!!!!!")
            res = session.get(f'{basic_url}/get_cookie')
            print(res.text)  # הדפסת התוכן
        else:
            print(f"Error: {response.status_code}")



def play():
    try:
        num = int((input("enter number:")))
        message = {'num': num}
        response = session.post(f'{basic_url}/play', json=message)
        word = response.json()
        if word == "you need to login":
            print("you cant")
        else:

            print(word)
            s = ""
            fail1 = 0
            fail2 = 6
            succes = 0
            a = ""
            for i in range(0, len(word)):
                if word[i] == " ":
                    s += " "
                s += "_"
            print(s)

            # message = {'name': user.name, 'id': user.id, 'password': user.password};
            strarr = [
                "x-------x",
                """
                x-------x
                |
                |
                |
                |
                |""",
                """
                x-------x
                |       |
                |       0
                |
                |
                |""",

                """
                x-------x
                |       |
                |       0
                |       |
                |
                |""",

                r"""
                x-------x
                |       |
                |       0
                |      \|/ 
                |
                |""",

                r"""
                x-------x
                |       |
                |       0
                |      \|/ 
                |      \
                |
                """,

                r"""
                x-------x
                |       |
                |       0
                |      \|/ 
                |      \ / 
                |
                """]

            while fail1 <= 6 and succes < len(word) - word.count(" "):
                l = input("enter letter")
                flag = False
                if a.__contains__(l) == False:
                    a += l + ","
                    print(f"you already enter:{a}")
                    for i in range(0, len(word)):

                        if word[i] == l:
                            succes += 1
                            flag = True
                    if flag == False:
                        print(strarr[fail1])
                        print(f"you have more{fail2} fails")
                        fail2 -= 1
                        fail1 += 1
            if succes == len(word) - word.count(" "):
                use.words.add(word)
                use.wins += 1
                use.count += 1
                print(succes)
                print(len(word) - word.count(" "))
                print("GAME!!!!!!")


            if fail1 == 7:
                use.count += 1
                print("GAME OVER!!!!!!")
            a = 0
            while a != 3 and a != 2 and a != 1:
                a = int(
                    input("press 1 if you want to play again, 2 if you want to see history,3 if you want to sign out"))
                if a == 1:
                    update()
                    play()

                if a == 2:
                    update()
                    print(
                        f"name:{use.name},id:{use.id},password:{use.password},words:{use.words},countGame:{use.count},wins:{use.wins}")
                if a == 3:
                    m = {'name': use.name, 'id': use.id, 'password': use.password}
                    # print(m)
                    response = session.post(f"{basic_url}/sign_out", json=m)
                    if response.status_code == 200:
                        print(response.json())
                    else:
                        print(f"Error: {response.status_code}")


    except ValueError as er:
        print(f"Error! {er}")
    except:
        print(f"Error!")


def update():
    s = ""
    c = use.count
    w = use.wins
    for x in use.words:
        s += x + ','
    message = {'name': use.name, 'id': use.id, 'password': use.password, 'count': c, 'wins': w,
               'words': s}

    response = session.post(f'{basic_url}/update', json=message)
    if response.status_code == 200:  # אם הבקשה הצליחה
        print(response.json())  # הדפסת התוכן
    else:
        print(f"Error: {response.status_code}")
def main():
    login()
    play()


if __name__ == '__main__':
    main()
# def set_cookie():
#     message = {'name': 'Sara'}
# response = session.post(f'{basic_url}/set_cookie', json=message)
# if response.status_code==200:
# print(response.text)
# time.sleep(1)
# cookie = response.cookies.get_dict()
#     response = session.get(f'{basic_url}/get_cookie')  # , cookies=cookie
#     if response.status_code == 200:
#      print(response.json())
#     else:
#      print(f"ssss{response.status_code}")
# else:
#     print(response.status_code)
