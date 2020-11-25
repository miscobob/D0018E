from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import mysql.connector
from . import labimp

app = Flask(__name__)

db = mysql.connector.connect(user="python", passwd ="password", host ="localhost", database="labdb")
conn = db.cursor()

#db = mysql.connector.connect(user="python", passwd ="password", host ="localhost", database="labdb")

datab = labimp.labdb()

@app.route('/')
def start():
    return render_template('home.html')

@app.route('/<name>')
def route_html(name):
    return render_template(name)

@app.route('/login', methods = ["POST","GET"])
def login():
    if(request.method == "POST"):
        username = str(request.form["username"])
        password = request.form["password"]
        if validate_user(username, password):
            return render_template('success.html')
    return render_template('login.html')

@app.route('/sql', methods = ["POST","GET"])
def sql():
    if(request.method == "POST"):
        id = str(request.form["id"])
        name = str(request.form["name"])
        datab.sql_insert(id, name)
    elif(request.method == "GET"):
        return redirect('/cgi-bin/data.py')

@app.route('/register', methods = ["POST","GET"])
def register():
    if(request.method == "POST"):
        request.form["username"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
    return render_template('register.html', error = "NOT_YET_IMPLIMENTED");


def reg_user(username, password):
    return True


def validate_user(username, password):
    return True
    cur = db.cursor()
    print(str(username))
    cur.execute("select name from test where name = '"+ username+"'")
    result = cur.fetchall()
    cur.close()
    return result

if __name__ == "__main__":
    app.run()
