from flask import Flask
from flask import render_template
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(user="python", passwd ="password", host ="localhost", database="labdb")


@app.route('/')
def start():
    return render_template('webpage.html')

@app.route('/login', methods = ["POST","GET"])
def login():
    if(request.method == "POST"):
        username = request.form["username"]
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
    cur.execute("select name from test where %s", username)
    result = cur.fetchone() is not None    
    cur.close()
    return result
