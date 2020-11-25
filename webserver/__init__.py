from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import mysql.connector
import re
from . import labimp

app = Flask(__name__)

datab = labimp.labdb()


@app.route('/')
def start():
    return render_template('home.html')


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
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if datab.hasUserWith(username = username, email = email):
           return render_template('register.html', error = "User name is already taken")
        if re.findall("[\W]",username) or not username:
            return render_template('register.html', error = "No whitespace or special are aloud in user name")
        if not re.match("^[\w]+([\w]|\-|\_|\.)*[\w]+@[\w]+\.[\w]+$", email):
            return render_template('register.html', error = "Please submit a valid email address")
        if re.findall("[\s]", password) or not password:
            return render_template('register.html', error = "No whitespace are aloud in password")
        datab.req_user(username, email, password)
        return render_template('login.html', error = "Success, you can now log in")
    return render_template('register.html')


def validate_user(username, password):
    return True

if __name__ == "__main__":
    app.run()
