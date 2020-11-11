from flask import Flask
from flask import render_template
import MySQLdb

app = Flask(__name__)
db = MySQLdb.connect(host ="localhost", user="python", passwd ="password", db="labdb");
cur = db.cursor();
cur.execute("select * from test");
for(row in cur.fetchall()):
    print row[0]

@app.route('/')
def start():
    return render_template('webpage.html')

@app.route('/login', methods = ["POST","GET"])
def login():
    if(request.method == "POST"):

@app.route('/register', methods = ["POST","GET"])
def reqister():
    if(request.method == "POST"):
        request.form["username"];
        
        
        
def reg_user(username, password):
    return True;


def validate_user(username, password):
    return False;
