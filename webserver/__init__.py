from flask import Flask
from flask import render_template
from flask import request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(user="python", passwd ="password", host ="localhost", database="labdb")


@app.route('/')
def start():
    return render_template('index.html')

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
        else:
            return render_template('webpage.html')

@app.route('/register', methods = ["POST","GET"])
def reqister():
    if(request.method == "POST"):
        request.form["username"]


def reg_user(username, password):
    return True


def validate_user(username, password):
    cur = db.cursor()
    print(str(username))
    cur.execute("select name from test where name = '"+ username+"'")
    result = cur.fetchall()
    cur.close()
    return result

if __name__ == "__main__":
    app.run()
