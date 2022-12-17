import sqlite3
from flask import Flask, request
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as hasher
import secrets
import datetime
from Database import Database

app = Flask(__name__)

database = Database("database.db")

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = secrets.token_urlsafe()
        self.token_generation_date = datetime.datetime.now()
        self.write = False
        self.read = False
        self.change_permissions = False
        self.edit = False

connection = sqlite3.connect(database.db)
cursor = connection.cursor()

statement0 = '''DROP TABLE IF EXISTS USERS'''
cursor.execute(statement0)

cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
    USERNAME VARCHAR(20) PRIMARY KEY,
    PASSWORD VARCHAR(200) NOT NULL,
    TOKEN VARCHAR(200) NOT NULL,
    TOKEN_GENERATION_DATE TEXT NOT NULL,
    WRITE INTEGER NOT NULL CHECK (WRITE IN (0,1)),
    READ INTEGER NOT NULL CHECK (READ IN (0,1)),
    CHANGE_PERMISSIONS INTEGER NOT NULL CHECK (CHANGE_PERMISSIONS IN (0,1)),
    EDIT INTEGER NOT NULL CHECK (EDIT IN (0,1))
    );
    ''')

admin_user = User("admin","admin")
admin_user.write = True
admin_user.read = True
admin_user.change_permissions = True
admin_user.edit = True


with sqlite3.connect(database.db) as conn:
    add_user = "INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?)"
    cursor = conn.cursor()
    cursor.execute(add_user,(admin_user.username,hasher.hash(admin_user.password),admin_user.token,admin_user.token_generation_date,admin_user.write,admin_user.read,admin_user.change_permissions,admin_user.edit))
    conn.commit()

guest_user = User("guest","guest")
guest_user.write = False
guest_user.read = True
guest_user.change_permissions = False
guest_user.edit = False


with sqlite3.connect(database.db) as conn:
    add_user = "INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?)"
    cursor = conn.cursor()
    cursor.execute(add_user,(guest_user.username,hasher.hash(guest_user.password),guest_user.token,guest_user.token_generation_date,guest_user.write,guest_user.read,guest_user.change_permissions,guest_user.edit))
    conn.commit()

# cursor.execute("INSERT INTO USERS VALUES('admin','admin');")
connection.commit()
connection.close()

@app.route('/login')
def login():
    input_username = request.form.get('inputUsername', default = 'guest', type = str) 
    input_password = request.form.get('inputPassword', default = 'guest', type = str)
    
    with open('readme.txt', 'w') as f:
        f.write(input_username)

    with sqlite3.connect(database.db) as conn:
        query = "SELECT TOKEN, TOKEN_GENERATION_DATE, PASSWORD FROM USERS WHERE (USERNAME = ?)"
        cursor = conn.cursor()
        selected_user = cursor.execute(query,(input_username,)).fetchall()
        conn.commit()

        with open('readme2.txt', 'w') as f:
            f.write(str(selected_user))

    hashed_password = selected_user[0][2]
    if(not hasher.verify(input_password, hashed_password)):
        return {"msg" : "ERROR: User Not Found!"}, 401
    token = selected_user[0][0]
    # if(datetime.datetime.now() - datetime.strptime(selected_user[0][1])> datetime.timedelta(24)):
    #     token = secrets.token_urlsafe()  # token and token gd should be updated after this step  

     
    data = {
        'input_username': input_username,
        'input_password': input_password
    }
    response = Flask.make_response(Flask.jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

