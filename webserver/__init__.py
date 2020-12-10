from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory, safe_join, abort
import mysql.connector
import re
from . import labimp
#import labimp
import datetime
import json
import functools

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'CZ5iMX2KkTXkm9D1RyRqFYkedt-9C4mF'
datab = labimp.labdb()

@app.route('/')
def start():
    if(session.get("UserID")):
        return render_template('home.html', user = True)
    return render_template('home.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("images", "favicon.ico")

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
        if(request.method == "POST"):
            return render_template('account.html', user = username, error="password incorrect")
        else:
            return render_template('account.html', user = username)
    return redirect("/login")

"""
Route to shopping basket
"""
@app.route('/basket', methods = ["POST","GET"])
def basket():
    if session.get("UserID"):
        return render_template('basket.html', user = true)
    else:
        return render_template('basket.html')

@app.route('/updateBasket', methods = ["POST"])
def updateBasket():
    if request.method == "POST":
        if session.get("UserID"):
            username = getUserName()
            if username:
                pid = request.form["pid"]
                mod = request.form["mod"]
                if not datab.addToCart(userid, pid, mod):
                    return getBasketItemAsJsonString(session["UserID"], pid, mod)
                return ""
        else:
            return ""
    else:
        return ""

"""
adds a new item to user basket
"""
@app.route('/addProduct', methods = ["POST"])
def addProduct():
    if session.get("UserID"):
        return ""
    return ""

@app.route('/incrementProduct', methods = ["POST"])
def incrementProduct():
    if session.get("UserID"):
        return ""
    return ""
"""
Route to products page
"""
@app.route('/products', methods = ["POST", "GET"])
def products():
    return render_template('products.html')
"""
Route to product page
"""
@app.route('/products/<int:pid>')
def productPage(pid):
    if session.get("UserID"):
        return render_template('products.html', user=True)
    return render_template('product.html', pname = pid)

"""
Return javascript file
"""
@app.route('/js/<path:file>')
def sendjs(file):
    return send_from_directory('js', file)

@app.route('/images/<path:image>')
def sendImage(image):
    return send_from_directory('images',image)



"""
Should load basket from database into cookies
"""
@app.route("/loadBasket")
def loadBasket():
    if session.get("UserID"):
        username = getUserName()
        if(username):
            return getBasketAsJsonString(session["UserID"])
    return ""

@app.route("/loadProducts")
def loadProducts():
    if session.get("UserID"):
        return ""
    return None

#@app.route("/addProduct")
#def addProduct():
#kör makeProduct.js
#lägg till produkt i databas


"""
validates username and password, if validated set userid to return userid of session
"""
def validateUser(username, password):
    userId = datab.validateUser(username, password)
    if(userId):
        session["UserID"] = userId
        session["DTS"] = datetime.datetime.now().strftime("%y:%m:%d,%H:%M:%S")
        return True
    else:
        return False

"""
Will return username linked to UserID of session, no username is found it will pop the userid from the session
"""
def getUserName():
    if not session.get('DTS'):
        session.pop("UserID", None)
        return ""
    dts = datetime.datetime.strptime(session['DTS'],"%y:%m:%d,%H:%M:%S")
    username = ""
    if datetime.datetime.now() - dts > TTL or not (username := datab.getUserName(session["UserID"])):
        session.pop("UserID", None)
        session.pop("DTS", None)
        return ""
    return username

def getBasketItemAsJsonString(userid, pid, count):
    data = datab.getBasketCount(userid, pid)
    obj = {"pid":data[0],"path":data[1], "name":data[2],"make":data[3],"count":data[4] ,"price":data[5]}
    return json.dumps(obj)

def getBasketAsJsonString(userid):
    basket = datab.getBasket(userid)
    products = []
    for item in basket:
        obj = convertBasketResponseToJson(item)
        products.append(obj)
    jsonbasket = {"products":products}
    return json.dumps(jsonbasket)

def convertBasketResponseToJson(data):
    obj = {"pid":data[0],"path":data[1], "name":data[2],"make":data[3],"count":data[4] ,"price":data[5]}
    return obj
    

TTL = datetime.timedelta(days = 7)

if __name__ == "__main__":
    app.run()
