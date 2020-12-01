from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re
from . import labimp
#import labimp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CZ5iMX2KkTXkm9D1RyRqFYkedt-9C4mF'
datab = labimp.labdb()


@app.route('/')
def start():
    if(session.get("UserID")):
        username = getUserName()
        if username:
            return render_template('home.html', user = username)
    return render_template('home.html')


@app.route('/login', methods = ["POST","GET"])
def login():
    if session.get("UserID"):
        if getUserName():
            return redirect("/account")
    if(request.method == "POST"):
        username = str(request.form["username"])
        password = str(request.form["password"])
        if validateUser(username, password):
            return redirect('/account')
        else:
            return render_template('login.html', error = "invalid user/password combination")
    if request.args.get("fromRegister"):
        return render_template('login.html',message = "Success, a new account has been created you can now log in!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get("UserID"):
        session.pop("UserID", None)
    return redirect('/login')

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
    if session.get("UserID"):
        return redirect("/account")
    if(request.method == "POST"):
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if datab.hasUserWith(username = username, email = email):
           return render_template('register.html', error = "User name or email is already used by other account")
        if re.findall("[\W]",username) or not username:
            return render_template('register.html', error = "No whitespace or special are aloud in user name")
        if not re.match("^[\w]+([\w]|\-|\_|\.)*[\w]+@[\w]+\.[\w]+$", email):
            return render_template('register.html', error = "Please submit a valid email address")
        if re.findall("[\s]", password) or not password:
            return render_template('register.hmtl', error = "No whitespace are aloud in password")
        datab.regUser(username, email, password)
        return redirect(url_for('login',fromRegister=True))
    return render_template('register.html')

@app.route('/account', methods = ["POST","GET"])
def account():
    if session.get("UserID"):
        username = getUserName()
        if not username: 
            return redirect("/login")
        return render_template('account.html', user = username)
    return redirect("/login")
  
"""
validates username and password, if validated set userid to return userid of session
"""
def validateUser(username, password):
    userId = datab.validateUser(username, password)
    if(userId):
        session["UserID"] = userId
        return True
    else:
        return False
"""
Will return username linked to UserID of session, no username is found it will pop the userid from the session
"""
def getUserName():
    username = datab.getUserName(session["UserID"])
    if not username:
        session.pop("UserID", None)
        return ""
    return username



if __name__ == "__main__":
    app.run()
