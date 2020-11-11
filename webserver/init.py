from flask import Flask
from flask import render_template
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(user="python", passwd ="password", host ="localhost", database="labdb");
cur = db.cursor();
cur.execute("select * from test");
for row in cur:
    print (row)

@app.route('/')
def start():
    return render_template('webpage.html')

@app.route('/login', methods = ["POST","GET"])
def login():
    if(request.method == "POST"):
        return False	
@app.route('/register', methods = ["POST","GET"])
def reqister():
    if(request.method == "POST"):
        request.form["username"]
        
        
        
def reg_user(username, password):
    return True


def validate_user(username, password):
    return False
