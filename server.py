import random

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from hugmam import user

app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/login', methods=["POST"])
def login():
    obj = request.json
    if obj.get('id') and obj.get('password'):
        with open("users.txt", 'r') as f:
            s = f.read().strip()
        for x in s.split("\n"):
            s1 = x.split(':')
            if s1[1] == obj.get('id') and s1[2] == obj.get('password'):
                response = make_response(x)
                response.set_cookie('user', x, max_age=1000, httponly=True, secure=False)
                return response
        # rs = make_response("status")
        # rs.status = 404
        # return rs
    # else:
    return jsonify("Error!!! Enter all details")


@app.route('/sign_in', methods=["POST"])
def sign_func():
    obj = request.json
    with open("users.txt", 'r') as users:
        s = users.read()
    with open("./users.txt", 'w') as users:  # פתיחת קובץ לכתיבה. אם הקובץ קיים הוא ייפתח וידרס. אם לא- יווצר קובץ חדש
        if obj.get('name') and obj.get('id') and obj.get('password'):
            a = user(obj.get('name'), obj.get('id'), obj.get('password'));
            a1 = a.__str__()
            print(f"{a1}\n{s}", file=users)  # הדפסה לתוך הקובץ עם הפרמט
            res = make_response(a1)
            res.set_cookie('user', a1, max_age=1000, httponly=True, secure=False)
            return res


        else:
            print(f"{s}", file=users)  # הדפסה לתוך הקובץ עם הפרמט
            return jsonify("הכנס את כל השדות");


@app.route('/sign_out', methods=["POST"])
def sign_out():
    obj = request.json

    with open("users.txt", 'r') as f:
        s = f.readlines()
    str = ""
    for x in s:
        s1 = x.split(":")
        if x.__len__() > 1 and obj.get('id') == s1[1] and obj.get('password') == s1[2]:
            str += ""
        else:
            str += f"{x}"
    with open("users.txt", 'w') as f:
        print(str, file=f)
    return jsonify("יצאת מהאתר")



@app.route('/get_cookie', methods=["GET"])
def get_cookie():
    use = request.cookies.get('user')
    if use:
        return jsonify(use)
    return jsonify("Not found")


def my_decorator1(func):
    def wrapper(*args, **kwargs):
        use = request.cookies.get('user')
        if use:
            return func(*args, **kwargs)
        else:
            return jsonify("you need to login")

    return wrapper


arr = ['hellow everyone', 'miri ', 'happy chanuka', 'gradle']


@app.route('/play', methods=["POST"])
@my_decorator1
def play():
    random.shuffle(arr)
    print(arr)
    obj = request.json
    if obj['num'] < arr.__len__():
        return jsonify(arr[obj['num']])
    return jsonify(arr[obj['num'] % arr.__len__()])


@app.route('/update', methods=['POST'])
def update():
    obj = request.json
    use = user(obj.get("name"), obj.get("id"), obj.get("password"))
    use.words = obj.get("words")
    use.count = obj.get("count")
    use.wins = obj.get("wins")
    with open("users.txt", 'r') as f:
        s = f.readlines()
    str = ""
    for x in s:
        s1 = x.split(":")
        if x.__len__() > 1 and obj.get('id') == s1[1] and obj.get('password') == s1[2]:
            str += f"{obj.get('name')}:{obj.get('id')}:{obj.get('password')}:{obj.get('count')}:{obj.get('wins')}:{obj.get('words')}\n"
        else:
            str += f"{x}"
    with open("users.txt", 'w') as f:
        print(str, file=f)
    return jsonify("כל הכבוד")







if __name__ == "__main__":
    app.run(debug=True)
