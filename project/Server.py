from flask import Flask, request, jsonify, abort, make_response # צריך ליבא ולא הצלחתי להתקין
from flask_cors import CORS # צריך ליבא ולא הצלחתי להתקין
from User import  User
import json, random

app = Flask(__name__)  # יצירת מופע מהשרת
# כדי לפתור את בעיית ה-CORS
CORS(app, supports_credentials=True)  # supports_credentials=True- מאפשר עוגיות

#פונקציית התחברות
@app.route('/login', methods=['POST'])
def login():
    obj = request.json # מקבל ת"ז
    file = open('./Store.txt', 'r')
    list_file = file.readlines()
    for f in list_file:# עובר על מערך שורות קובץ השמירה
        obj_dict = json.loads(f)# המרה לאוביקט משתמש
        user = User(**obj_dict)
        if user.tz ==  (obj['tz']):# שאלה האם הוא מחובר
            return  make_response(f) # מחזיר את המשתמש בצורה של ג'יסון
    return make_response("login")

# פונקציית הרשמה
@app.route('/register', methods = ['POST'])
def register():
    obj = request.json # מקבלת אוביקט המכיל ת"ז שם וסיסמה
    user = User(obj['name'], obj['tz'], obj['password'],obj['count_play'], obj['words'], obj['count_win']) # יוצר מהמידע שקיבל אוביקט מסוג מחלקת משתמש
    with open("./Store.txt", 'a') as f:
        print(json.dumps(user.__dict__), file = f) # מוסיף אותו לקובץ השמירה כשהוא מומר לג'יסון
    return make_response(json.dumps(user.__dict__)) # מחזיר את המשתמש שנרשם בצורת ג'יסון

#פונקציית הגרלת המילה
@app.route('/random_word/<num>', methods=['GET'])
def random_word(num):
    file = open("./Words", 'r')
    list_word = file.readlines()
    random.shuffle(list_word)
    return list_word[int(num) % list_word.__len__()]

# פונקציית עריכת העוגיה
@app.route('/set_cookie', methods = ['POST'])
def set_cookie_func():
    obj = request.json
    response = make_response("cookie set!")
    response.set_cookie('user', obj['all_user'], max_age=10, httponly=True, secure=False, samesite='None')
    return response

# פונקציית בדיקה האם יש עוגיה
@app.route('/get_cookie', methods=['GET'])
def get_cookie_func():
    all_user = request.cookies.get('user')
    if all_user:
        return make_response("Cookie found!")
    return make_response("Cookie not found")

@app.route('/update_file', methods = ['POST'])
def update_file():
    obj = request.json
    file_read = open("./Store.txt", "r")
    lines_file = file_read.readlines()
    for l_n in lines_file:
        obj_dict = json.loads(l_n)  # המרה לאוביקט משתמש
        user = User(**obj_dict)
        if user.tz == (obj['tz']):
            lines_file.remove(l_n)
            continue
    lines_file.append(obj)
    file_write = open("./Store.txt", 'w')
    print("".join(lines_file), file=file_write)
    file_read.close()
    file_write.close()

if __name__ == "__main__":
    app.run(debug=True)