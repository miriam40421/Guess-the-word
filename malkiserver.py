import random

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from malkiuser import user

app = Flask(__name__)
CORS(app, supports_credentials=True)

myuser = user("", "", "")

@cross_origin(app, supports_credentials=True)
@app.route('/login', methods=["POST"])
def login():
    obj = request.json
    # print(obj)
    if obj.get('id') and obj.get('password'):
        file = open('f.txt', 'r')  # פתיחת הקובץ לקריאה- ברירת המחדל של פונקציית open
        s = file.readlines()
        # print(s)
        for s1 in s:
            # print(s1)
            s2 = s1.split(":")
            # print(s2[1])
            # print(s2[2])
            if int(s2[1]) == int(obj['id']) and int(s2[2]) == int(obj['password']):
                response = make_response(s1)
                response.set_cookie('user', s1, max_age=7000, httponly=True, secure=False)
                print(response)
                # myuser.name = response ["name"]
                # myuser.id=response
                return response
    return jsonify("אינך רשום אצלנו יש להרשם")
    # else:
    #     return jsonify(" יש למלא את כל הפרטים")


@cross_origin(app, supports_credentials=True)
@app.route('/register', methods=["POST"])
def register():
    obj = request.json
    if (obj.get('name') and obj.get('id') and obj.get('password')):
        with open("f.txt", 'r') as f1:
            alluser = f1.read()
        with open("f.txt", 'w') as f:  # פתיחת קובץ לכתיבה. אם הקובץ קיים הוא ייפתח וידרס. אם לא- יווצר קובץ חדש

            myuser = user(obj.get('name'), obj.get('id'), obj.get('password'))
            myuser1 = myuser.__str__()
            print(f"{myuser1}\n{alluser}", file=f)  # הדפסה לתוך הקובץ עם הפרמטר file שמקבל את האובייקט של הקובץ
            response = make_response(myuser1)
            response.set_cookie('user', myuser1, max_age=7000, httponly=True, secure=False)
            return response
    # else:
    return jsonify("הכנס את כל השדות")

def my_decorator1(func):
    def wrapper(*args, **kwargs):
       user = request.cookies.get('user')
       if user:
        return func(*args, **kwargs)
       else:
        return jsonify("cokee failed")
    return wrapper







@cross_origin(app, supports_credentials=True)
@app.route('/play', methods=["POST"])
@my_decorator1
def play():
    random.shuffle(arr)
    obj = request.json
    num = obj.get('num')
    if (num > arr.__len__()):
        return jsonify(arr[num % arr.__len__()])
    else:
        # print(arr[num])
        return jsonify(arr[num])

@cross_origin(app, supports_credentials=True)
@app.route('/get_cookie', methods=["GET"])
def get_cookie():
    user1 = request.cookies.get('user')
    if user1:
        return jsonify(user1)
    else:
     return jsonify("Not found")

@cross_origin(app, supports_credentials=True)
@app.route('/update', methods=["POST"])
def update():
    print("fghjk")
    obj = request.json
    myuser = user(obj.get('name'), obj.get('id'), obj.get('password'))
    myuser.countgames = obj.get('countgames')
    myuser.conntwins = obj.get('countwins')
    myuser.words = obj.get('words')
    print(myuser.__str__())
    with open("f.txt", 'r') as f1:
        alluser = f1.readlines()
        str = ""
        for x in alluser:
            s1 = x.split(':')
            if s1.__len__() > 1:
                if s1[1] == obj.get('id') and s1[2] == obj.get('password'):
                    # myuser1 = myuser.__str__()
                    # print(f"{myuser1}kjhg")
                    str += f"{obj.get('name')}:{obj.get('id')}:{obj.get('password')}:{obj.get('countgames')}:{obj.get('countwins')}:{obj.get('words')}\n"
                else:
                    str += x
            with open("f.txt", 'w') as f:

                print(f"{str}", file=f)  # הדפסה לתוך הקובץ עם הפרמטר file שמקבל את האובייקט של הקובץ

    return jsonify("הכנס את כל השדות")

@cross_origin(app, supports_credentials=True)
@app.route('/exit', methods=["POST"])
def exit():
    # print("fghjk")
    obj = request.json

    with open("f.txt", 'r') as f1:
        alluser = f1.readlines()
        str = ""
        for x in alluser:
            s1 = x.split(':')
            if s1.__len__() > 1:
                if s1[1] == obj.get('id') and s1[2] == obj.get('password'):

                    str += f"" "\n"
                else:
                    str += x
            with open("f.txt", 'w') as f:

                print(f"{str}", file=f)  # הדפסה לתוך הקובץ עם הפרמטר file שמקבל את האובייקט של הקובץ

    return jsonify("הכנס את כל השדות")






arr = ["חנוכה", "מסיבה","סביבון"]



if __name__ == "__main__":
    app.run(debug=True)
