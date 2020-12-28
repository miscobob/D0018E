from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory, safe_join, abort
import mysql.connector
import re, datetime, json
try:
    from . import labimp
    from . import tables
except :
    import labimp
    import tables

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'CZ5iMX2KkTXkm9D1RyRqFYkedt-9C4mF'
datab = labimp.labdb()

@app.route('/')
def start():
    if(isUser(session.get("UserID"))):
        return render_template('home.html', user = True)
    return render_template('home.html')

@app.route('/admin')
@app.route('/admin/')
def admin():
    return redirect('/admin/login')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("images", "favicon.ico")

@app.route('/login', methods = ["POST","GET"])
def login():
    if isUser(session.get("UserID")):
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

@app.route('/admin/login', methods = ["POST","GET"])
def adminLogin():
    if isEmployee(session.get("UserID")):
        return redirect('/admin/account')
    if(request.method == "POST"):
        username = str(request.form["username"])
        password = str(request.form["password"])
        if validateEmployee(username, password):
            return redirect("/admin/account")
        return render_template('adminLogin.html',error = "invalid username/password combination")
    else:
        return render_template('adminLogin.html')        

@app.route('/logout')
def logout():
    if session.get("UserID"):
        session.pop("UserID", None)
    return redirect('/login')

@app.route('/register', methods = ["POST","GET"])
def register():
    if isUser(session.get("UserID"), TTLUser):
        return redirect("/account")
    if(request.method == "POST"):
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if len(username) < 5 or len(username) > 13 or re.findall("[\W]",username):
            return render_template('register.html', error = "Username must have between 5 and 12 characters and contain no whitespaces or special characters")
        if len(password) < 5 or len(password) > 13 or re.findall("[\s]", password):
            return render_template('register.hmtl', error = "Password must have between 5 and 12 characters and contain no whitespaces")
        if not re.match("^[\w]+([\w](\-|\_|\.))*[\w]+@[\w]+((\-|\_|\.)*[\w]+)*\.[\w]+$", email):
            return render_template('register.html', error = "Please submit a valid email address")
        if datab.hasUserWith(username = username, email = email):
           return render_template('register.html', error = "User name or email is already used by other account")
        datab.regUser(username, email, password)
        return redirect(url_for('login',fromRegister=True))
    return render_template('register.html')

@app.route('/account', methods = ["POST","GET"])
def account():
    if isUser(session.get("UserID"), TTLUser):
        username = getUserName()
        if not username: 
            return redirect("/login")
        if(request.method == "POST"):
            return setNewPassword('account.html', username)
        else:
            return render_template('account.html', user = username)
    return redirect("/login")

@app.route('/admin/account', methods = ["POST","GET"])
def adminAccount():
    if session.get("UserID") and (answer:= hasAccess(session.get("UserID"), [tables.AccountAccess.MANAGER,tables.AccountAccess.ADMIN],TTLAdmin)):
        username = answer[1]
        access = answer[0]
        if(request.method == "POST"):
            return setNewPassword('adminAccount.html', username, admin= (access == tables.AccountAccess.ADMIN))
        else:
            if access == tables.AccountAccess.ADMIN:
                return render_template('adminAccount.html', user = username, admin = True)
            return render_template('adminAccount.html', user = username)
    return redirect("/admin/login")

def setNewPassword(htmlFile, username, admin = False):
    """
    tries to set new password for user in session
    """
    oldpassword = request.form["oldpassword"]
    newpassword = request.form["newpassword"]
    if len(newpassword) < 5 or len(newpassword) > 13 or re.findall("[\s]", newpassword):
        return render_template(htmlFile, user = username, error="Password must have between 5 and 12 chars and contain no whitespaces", admin = admin)
    if datab.updatePassword(session.get("UserID"),oldpassword,newpassword):
        return render_template(htmlFile, user = username, message="password updated", admin = admin)
    return render_template(htmlFile, user = username, error="password incorrect", admin = admin)

@app.route('/admin/registerEmployee', methods = ["POST"])
def registerEmployee():
    if request.method == "POST" and isEmployee(session.get("UserID"), TTLAdmin):
        obj = request.get_json()
        if obj:
            username = obj["username"]
            email = obj["email"]
            password = obj["password"]
            accessLevel = tables.AccountAccess(obj["accesslevel"])
        else:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            accessLevel = tables.AccountAccess(request.form["accesslevel"])
            
        if len(username) < 5 or len(username) > 13 or re.findall("[\W]",username):
            return "<h3>No whitespace or special are aloud in user name and must be longer then 4 characters</h3>"
        if len(password) < 5 or len(password) > 13 or re.findall("[\s]", password):
            return "<h3>Password must have between 5 and 12 chars and contain no whitespaces</h3>"
        if not re.match("^[\w]+([\w](\-|\_|\.))*[\w]+@[\w]+((\-|\_|\.)*[\w]+)*\.[\w]+$", email):
            return "<h3>Please submit a valid email address</h3>"
        if datab.hasUserWith(username = username, email = email):
            return "<h3>User name or email is already used by other account</h3>"
        if accessLevel is tables.AccountAccess.ADMIN:
            datab.regAdmin(username, email, password)
        elif accessLevel is tables.AccountAccess.MANAGER:
            datab.regManager(username, email, password)
        else:
            return "<h3>please select a Accesslevel for new account</h3>"
        return "<p>New user employee has been registered</p>"
        
    return redirect("/")

"""
Route to shopping basket
"""
@app.route('/basket', methods = ["POST","GET"])
def basket():
    if isUser(session.get("UserID"), TTLUser):
        return render_template('basket.html', user = True)
    else:
        return render_template('basket.html')

@app.route('/updateBasket', methods = ["POST"])
def updateBasket():
    if request.method == "POST":
        obj = request.get_json()
        if obj:
            pid = obj["pid"]
            mod = obj["mod"]
        else:
            pid = request.form["pid"]
            mod = int(request.form["mod"])
        if(datab.hasProduct(pid)):
            if isUser(session.get("UserID")):
                username = getUserName()
                if username:
                    if not datab.addToCart(session["UserID"], pid, mod):
                        return ""
                    return "no product with id " + str(pid)
                return("failed to verfiy user authenticity")
            return ""
        return "no product with id " + str(pid)
    else:
        return redirect("/")


@app.route('/addProductToBasket', methods = ["POST"])
def addProductToBasket():
    """
    adds a new item to user basket
    """
    if request.method == "POST":
        obj = request.get_json()
        if obj:
                pid = obj["pid"]
                mod = obj["mod"]
                hasBasket = obj["hasBasket"]
        else:
            pid = request.form["pid"]
            mod = int(request.form["mod"])
            hasBasket = request.form["hasBasket"]
        if datab.hasProduct(pid):
            if isUser(session.get("UserID")):
                username = getUserName()
                if username:
                    if  not datab.addToCart(session["UserID"], pid, mod):
                        if hasBasket:
                            response = getBasketItemAsJsonString(session["UserID"], pid, mod)
                        else:
                            response = getBasketAsJsonString(session["UserID"])
                        return response
                    return "{}"
            obj = getProductAsJsonString(pid)
            if hasBasket:
                return obj
            else:
                data = '{"products":['+obj+']}'
                return data
        else:
            return "{}"
    return "{}"


@app.route('/products', methods = ["GET"])
def products():
    """
    Route to products page
    """
    if isUser(session.get("UserID"), TTLUser):
        return render_template('products.html', user = True)
    return render_template('products.html')

@app.route('/admin/products', methods = ["GET"])
def adminProducts():
    """
    Route to admin products page
    """
    if isEmployee(session.get("UserID"), TTLAdmin):
        return render_template('adminProducts.html', user = True)
    return redirect('/admin/login')


@app.route('/products/<int:pid>')
def productPage(pid):
    """
    Route to product page
    """
    if isUser(session.get("UserID"), TTLUser):
        return render_template('product.html', pname = pid, user=True)
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



@app.route("/loadBasket")
def loadBasket():
    """
    Should load basket from database into cookies
    """
    if isUser(session.get("UserID")):
        return getBasketAsJsonString(session["UserID"])
    return {}

@app.route("/loadProducts")
def loadProducts():
    s = ('{  "products":['
         '{"pid":"64852", "path":"/images/image1.png", "name":"product1", "make":"maker"},'
		 '{"pid":"1", "path":"/images/paul_senior.png", "name":"Trampcykel", "make":"Faze Clan"},'
         '{"pid":"64352", "path":"/images/image2.png", "name":"product2", "make":"maker"}]}')
    return s
    if session.get("UserID"):
        return ""
    return None

@app.route("/admin/addProduct" , methods = ["POST"])
def addProduct():
    if request.method == "POST" and isEmployee(session.get("UserID"), TTLAdmin):
        obj = request.get_json()
        if obj:
            pname = obj["name"]
            pmake = obj["make"]
            price = obj["price"]
            stock = obj["stock"]
            image = obj.get("path")
        else:
            pname = request.form["name"]
            pmake = request.form["make"]
            price = request.form["price"]
            stock = request.form["stock"]
            image = request.form.get("path")
        if datab.hasProduct(pname = pname, pmake=pmake):
            return "<h3>Product with that name already exist for that brand</h3>"
        else:
            datab.addNewProduct(pname, pmake, price, stock, image)
            return "<h4>A new product has been added</h4>"
    return redirect("/")


def validateUser(username, password):
    """
    validates username and password, if validated set userid to return userid of session
    """
    userId = datab.validateUser(username, password)
    if(userId):
        session["UserID"] = userId
        session["DTS"] = datetime.datetime.now().strftime("%y:%m:%d,%H:%M:%S")
        return True
    else:
        return False

def validateEmployee(username, password):
    userId = datab.validateEmployee(username, password)
    if(userId):
        session["UserID"] = userId
        session["DTS"] = datetime.datetime.now().strftime("%y:%m:%d,%H:%M:%S")
        return True
    else:
        return False

def hasAccess(userid, access, TTL):
    """
    check if given userid exist in list of access level
    """
    if not session.get('DTS'):
        session.pop("UserID", None)
        return None
    dts = datetime.datetime.strptime(session['DTS'],"%y:%m:%d,%H:%M:%S")
    if TTL and datetime.datetime.now()-dts>TTL:
        session.pop("UserID", None)
        session.pop("DTS", None)
        return None
    accessLevel, username = datab.getAccessLevel(userid)
    accessLevel = tables.AccountAccess(accessLevel)
    if accessLevel in access:
        return accessLevel, username
    return None
         
def getUserName(TTL = 0):
    """
    Will return username linked to UserID of session, 
    no username is found it will pop the userid from the session
    """
    if not session.get('DTS'):
        session.pop("UserID", None)
        return ""
    dts = datetime.datetime.strptime(session['DTS'],"%y:%m:%d,%H:%M:%S")
    username = ""
    if (TTL and datetime.datetime.now()-dts>TTL) or not (username := datab.getUserName(session["UserID"])):
        session.pop("UserID", None)
        session.pop("DTS", None)
    return username

def isUser(id, TTL = 0):
    return id and hasAccess(id, [tables.AccountAccess.USER], TTL)

def isEmployee(id, TTL = 0):
    return id and hasAccess(id, [tables.AccountAccess.ADMIN, tables.AccountAccess.MANAGER], TTL)

def getBasketItemAsJsonString(userid, pid):
    data = datab.getBasketCount(userid, pid)
    #print(data)
    obj = {"pid":data[0],"path":data[1], "name":data[2],"make":data[3],"count":data[4] ,"price":data[5]}
    return json.dumps(obj)

def getProductAsJsonString(pid):
    data = datab.getProduct(pid)
    obj = {"pid":data[0],"path":data[5], "name":data[1],"make":data[2],"count":1 ,"price":data[3]}
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
    

TTLUser = datetime.timedelta(days = 7)
TTLAdmin = datetime.timedelta(days = 1)
if __name__ == "__main__":
    app.run()
