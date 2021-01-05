from cryptography.fernet import Fernet
import mysql.connector, os.path, datetime
try:
    from . import tables
except:
    import tables

class databas:
    def __init__(self, usr, password, hst, dbname, tables):
        self.user = usr
        self.password = password
        self.host = hst
        self.name = dbname
        self.connect()
        self.dbCursor.execute("CREATE DATABASE IF NOT EXISTS " +dbname)
        self.dbConnection.database = dbname
        for table in tables:
            self.createTable(tables[table])
        
        #self.db = mysql.dbCursorector.dbCursorect(user=usr, passwd=password, host=hst, database=dbname)
        #self.dbCursor = self.db.cursor(buffered=True)
            
    """
    Insert values into table, both table and values should both be pre-generated strings to be so it matches
    wished insert, this method autocommits, should not be done togheter with a transaction
    """
    def insertIntoTable(self, table, values, inserts):
        self.testConnection()
        #print('INSERT INTO ' + table + ' VALUES('+values + ')')
        self.dbCursor.execute('INSERT INTO ' + table + ' VALUES('+values + ')',inserts)
            
    """
    returns query from given table with the option
    to select specific collumns from table and match specific values in tables.
    When matching strings use taged string formating to set string to compare to.
    Where string as element in kwargs and key to that element is the tag for where
    that string should be placed
    """
    def select(self, table,  col = '*',joinTables = [], conditions = [], where = "", **kwargs):
        self.testConnection()
        commit = not self.dbConnection.in_transaction 
        tbl = []
        statement ="SELECT "+col+" FROM "+table
        if(len(joinTables) == len(conditions)):
            for i in range(0, len(joinTables)):
                statement += " INNER JOIN " +joinTables[i] + " ON " + conditions[i]
        if where:
            statement+= " WHERE "+ where
        #print(statement%kwargs)
        self.dbCursor.execute(statement, kwargs)
        for row in self.dbCursor:
            tbl.append(row)
        #print("sql response",tbl)
        if commit:
            self.dbConnection.commit()  # so it does not lock it self into a specific state of dbs
        return tbl

    def update(self, table, setCol, setValue, where = "", **kwargs):
        """
        Update Table with new info, need to be manually commited.
        """
        self.testConnection()
        commit = not self.dbConnection.in_transaction
        if type(setCol) == list and type(setValue) == list and len(setCol) == len(setValue):
            statement = "UPDATE "+ table + " SET "
            for i in range(0,len(setCol)):
                if not isinstance(setValue[i], str):
                    statement +=setCol[i]+" = "+str(setValue[i])
                else:
                    statement +=setCol[i]+" = '"+setValue[i]+"'"
                if i<len(setCol)-1:
                    statement+=", "
        else:
            if not isinstance(setValue, str):
                statement ="UPDATE "+table+" SET "+setCol+" = "+str(setValue)
            else:
                statement ="UPDATE "+table+" SET "+setCol+" = '"+setValue+"'"
        if where:
            statement += " WHERE "+where
        #print(statement % kwargs)
        self.dbCursor.execute(statement, kwargs)
        rowsupdated = self.dbCursor.rowcount
        if commit:
            self.dbConnection.commit()
        return rowsupdated

    def delete(self, table, where):
        """
        Delete row from table, need to manually commit.
        """
        self.testConnection()
        statement = "DELETE FROM "+table+" WHERE "+where
        #print(statement)
        self.dbCursor.execute(statement)
    """
    returns all colmns from table
    """
    def returnTable(self, table):
        self.testConnection()
        tbl = []
        self.dbCursor.execute('select * from '+table)
        for row in dbCursor:
            tbl.append(row)
        return tbl

    """
    Creates a table according to given string table.
    table string of table you want to insert,
    kwargs dict of for string formating to get dynamic table naming.
    Creates only the table if table does not exist
    """
    def createTable(self, table, **kwargs):
        #print(table)
        self.testConnection()
        #print("CREATE TABLE IF NOT EXISTS " + table %kwargs)
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS " + table, kwargs)
        self.dbConnection.commit()
        
    """
    Closes the connection to db and closes curser. return if either failed
    """
    def close(self):
        if not (self.dbCursor.close() or self.dbConnection.close()):
            print("failed to close")
            return False
        return True
            
    """
    Tests if have lost connection to db
    """
    def testConnection(self):
        if not self.dbConnection.is_connected():
            self.reconnect()

    """
    Connect to mysql and create cursor
    """
    def connect(self):
        self.dbConnection = mysql.connector.connect(user=self.user, passwd=self.password, host=self.host)
        self.dbCursor = self.dbConnection.cursor(buffered=True)
        
    """
    Reconnect to db stored named
    """
    def reconnect(self):
        self.connect()
        self.dbConnection.database = self.name

    def commit(self):
        self.dbConnection.commit()

    """
    Start a transaction
    """
    def startTransaction(self):
        self.dbConnection.start_transaction()
    
    def lockTables(self, tables):
        lock = ""
        for i in range(0, len(tables)):
            lock += " " + tables[i] + " WRITE"
            if i < (len(tables)-1):
                lock +=","
        #print(lock)
        self.dbCursor.execute("LOCK TABLES" + lock)

    def unlockTables(self):
        self.dbCursor.execute("UNLOCK TABLES")
        self.commit()

    def rollback(self):
        self.dbConnection.rollback()

        
class labdb:
    def __init__(self):
        try:
            file = open("secret.key","x")
            key = Fernet.generate_key()
            file.write(key.decode("utf-8"))
            file.close()
            self.crypto = Fernet(key)
        except:
            file = open("secret.key","r")
            key = file.read()
            if not key:
                file.close()
                file = open("secret.key","w")
                key = Fernet.generate_key()
                file.write(key.decode("utf-8"))
                file.close()
                self.crypto = Fernet(key)
            else:
                file.close()
                self.crypto = Fernet(key.encode("utf-8"))
            
        self.db = databas('python', 'password', 'localhost', 'labdb', tables.tables)
        self.matchUserID = 'UserID = %(UserID)s'
        self.matchUserName = 'UserName = %(UserName)s'
        self.matchPassword = 'Password = %(Password)s'
        self.matchEmail = "Email = %(Email)s"
        self.matchStatus = "Status = %(Status)s"
        self.matchPid = "ProductID = %(PID)s"
        self.matchItem = "Item = %(Item)s"
        self.matchName = "Name = %(Name)s"
        self.matchMake = "Make = %(Make)s"
        self.matchAccess = "AccessLevel = %(Access)s"
        self.matchDoubleAccess = "(AccessLevel = %(Access1)s or AccessLevel = %(Access2)s)"
        self.matchTransaction = "TransactionNumber = %(TransactionNumber)s"
        self.encrypt = lambda s: self.crypto.encrypt(str(s).encode("utf-8"))
        self.decrypt = lambda s: self.crypto.decrypt(s).decode("utf-8") 
        if not self.hasUserWith(username = "Admin"):
            self.regAdmin("Admin","admin@localhost", "password")
    """
    Checks if it can find a username for given userid
    """
    def isUserID(self, userid):
        return bool(self.getUserName(userid))

    """
    checks if there exist someone with given username or given email,
    returns false if neither is given.
    """
    def hasUserWith(self,username = "", email = ""): 
        answer = []
        if  username and email:
            answer = self.db.select("Accounts", where = self.matchUserName + " or " + self.matchEmail, UserName = username, Email = email)
        elif username:
            answer = self.db.select("Accounts", where = self.matchUserName, UserName = username)
        elif email:
            answer = self.db.select("Accounts", where = self.matchEmail, Email = email)
        else:
            return False
        return len(answer) > 0

    """
    Registers a account as user with given email and given password with a given accvlvl
    """
    def regAccount(self, user, email, pw, acclvl):
        values = "%s, %s, %s,%s"
        self.db.insertIntoTable(tables.accountsInsert, values, (user, email, pw, acclvl.value))
        self.db.commit()

    """
    Registers a Website-user as user with given email and given password
    """
    def regUser(self, user, email, pw):
        self.regAccount(user, email, pw, tables.AccountAccess.USER)
        
    """
    Registers a Website-manager as user with given email and given password
    """
    def regManager(self, user, email, pw):
        self.regAccount(user, email, pw, tables.AccountAccess.MANAGER)

    """
    Registers a Website-admin as user with given email and given password
    """
    def regAdmin(self, user, email, pw):
        self.regAccount(user, email, pw, tables.AccountAccess.ADMIN)

    """
    returns username with given userid if not any result return empty string
    """
    def getUserName(self, userid):
        userid = self.decrypt(userid)
        answer = self.db.select("Accounts", col = "UserName", where= self.matchUserID, UserID = userid)
        if answer:
            return answer[0][0]
        else:
            return ""
    
    def validateAccount(self, username, password, access = tables.AccountAccess.USER):
        where = self.matchUserName+ " and "+ self.matchPassword  + " and "
        if(type(access) == list):
            where += self.matchDoubleAccess
            answer = self.db.select("Accounts", where = where , UserName = username, Password = password, Access1= str(access[0]), Access2 = str(access[1]))
        else:
            where += self.matchAccess
            answer = self.db.select("Accounts", where = where , UserName = username, Password = password, Access= str(access))
        return answer

    def validateUser(self, username, password):
        """
        validates a user log in attempt
        """
        answer = self.validateAccount(username, password)
        if answer:
            return self.encrypt(answer[0][0])
        return ""
        

    def validateEmployee(self, username, password):
        """
        validates a employee log in attempt
        """
        answer = self.validateAccount(username, password, access=[tables.AccountAccess.MANAGER, tables.AccountAccess.ADMIN])
        if not answer:
            return ""
        return self.encrypt(answer[0][0])

    def getUserID(self, var):
        answer = self.db.select("Accounts","UserID",where= self.matchEmail+ " or " + self.matchUserName, UserName = var, Email = var)
        if answer:
            return self.encrypt(answer[0][0])
        return ""

    def updatePassword(self, userId, oldpassword, newpassword):
        """
        update with new password for user, return true on success, false otherwise
        """
        userId = self.decrypt(userId)
        rowcount = self.db.update("Accounts", "Password", newpassword, where=self.matchUserID + " and " + self.matchPassword, UserID = userId, Password = oldpassword )
        self.db.commit()
        return bool(rowcount)

    def getAccessLevel(self, userId):
        """
        return access level of user, return type string
        """
        table = "Accounts"
        col = "AccessLevel, Username"
        where = self.matchUserID
        userId = self.decrypt(userId)
        answer = self.db.select(table, col= col, where = where, UserID = userId)
        if answer:
            return answer[0]
        return ""

    def addToCart(self, userid, productid, nr):
        """
        Adds a product to a new basket transaction or to existing basket
        """
        userid = self.crypto.decrypt(userid).decode("utf-8")
        transaction = self.db.select("Transactions", col="TransactionNumber", where=self.matchStatus+" AND "+self.matchUserID, Status = tables.TransactionState.BASKET.value, UserID = userid)
        if not transaction: # check if new basket needed
            values = "%s, %s"
            self.db.insertIntoTable(tables.transactionsInsert, values,(userid, tables.TransactionState.BASKET.value))
            self.db.commit()
            transaction = self.db.select("Transactions", col="TransactionNumber", where=self.matchStatus+" AND "+self.matchUserID, Status = tables.TransactionState.BASKET.value, UserID = userid)
            transnr = transaction[0][0]
        else:
            transnr = transaction[0][0]
            answer = self.db.select("TransactionData",col="Count", where = self.matchTransaction + " AND "+ self.matchItem, TransactionNumber =  transnr, Item = productid)
            if answer:
                count = answer[0][0]+nr
                if count > 0:
                    rowsupdated = self.db.update("TransactionData", "Count", str(count), "TransactionNumber='%s' AND Item='%s'"%(transnr, productid))
                    self.db.commit()
                    return 0
                elif count == 0:
                    rowsupdated = self.db.delete("TransactionData", "TransactionNumber='%s' AND Item='%s'"%(transnr, productid))
                    self.db.commit()
                    return 0
                else:
                    return 1
        if nr >= 1:
            self.db.insertIntoTable(tables.transactionDataInsert, "%s, %s, %s",(transnr, productid, nr))
            self.db.commit()
            return 0
        return 1
    
    def getBasketCount(self, userid, pid = 0):
        """
        Returns all products in basket or a given one
        return list if all otherwise return tuple
        col in order:
        production Id, image path, product name, name of product maker, amount in basket, price of product
        """
        userid = self.decrypt(userid)
        joinTables = ["Products t2", "Transactions t3"]
        col = "Item, Image, Name, Make, Count, t2.Price"
        conditions = ["t1.Item = t2.ProductID", "t1.TransactionNumber=t3.TransactionNumber"]
        if pid:
            where = "t3."+self.matchUserID+" and "+ "t3."+self.matchStatus + " and " +"t1."+self.matchItem
            answer = self.db.select("TransactionData" +" t1", col = col, joinTables = joinTables, conditions = conditions, where = where, UserID = userid, Status = tables.TransactionState.BASKET.value, Item = pid)
            if answer:
                return answer[0]
            return ""
        else:
            where = "t3."+self.matchUserID+" and "+ "t3."+self.matchStatus
            answer = self.db.select("TransactionData" +" t1", col = col, joinTables = joinTables, conditions = conditions, where = where, UserID = userid, Status = tables.TransactionState.BASKET.value)
            return answer

    def getBasket(self, userid):
        return self.getBasketCount(userid)

    def checkout(self, userid):
        userid = self.decrypt(userid)
        self.db.startTransaction()
        self.db.lockTables(["Transactions AS t2", "Products AS t3", "TransactionData AS t1"])
        joinTables = ["Transactions t2", "Products t3"]
        conditions = ["t1.TransactionNumber = t2.TransactionNumber", "t1.Item = t3.ProductID"]
        where = "t2."+self.matchUserID +" and t2."+ self.matchStatus 
        answer = self.db.select("TransactionData t1", "t1.TransactionNumber, Item, InStock, Count, Name, t3.Price", joinTables, conditions, where, UserID = userid, Status = tables.TransactionState.BASKET.value)
        if not answer:
            self.db.rollback()
            self.db.unlockTables()
            self.db.commit()
            return "Basket empty", 0
        for prod in answer:
            stockleft = prod[2]-prod[3]
            update = self.db.update("TransactionData t1", "Price", prod[5], where = self.matchTransaction+ " and "+ self.matchItem, TransactionNumber = prod[0], Item = prod[1])
            if not update:
                self.db.rollback()
                self.db.unlockTables()
                self.db.commit()
                return "ERROR could not confirm PRICE", 0
            if stockleft < 0 or not self.setStock(prod[1],stockleft, " t3") :
                #("rollback not in stock")
                self.db.rollback()
                self.db.unlockTables()
                self.db.commit()
                return "product not in stock", 0
        if not self.db.update("Transactions t2", ["DateTime","Status"], [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),tables.TransactionState.DONE.value],where=self.matchTransaction,TransactionNumber = answer[0][0]):
            #print("rollback failed update")
            self.db.rollback()
            self.db.unlockTables()
            self.db.commit()
            return "Error trying to complete purchase", 0
        self.db.unlockTables()
        self.db.commit()
        return "Purchase completed", 1

    def loadTransactions(self,userid):
        userid = self.decrypt(userid)
        col = "t1.TransactionNumber, DateTime, Status, Name, Make, Count, t1.Price"
        joinTables = ["Transactions t2", "Products t3"]
        conditions = ["t1.TransactionNumber = t2.TransactionNumber", "t1.Item = t3.ProductID"]
        where = "t2."+self.matchUserID + " and (t2." +self.matchStatus%{"Status":"%(Status1)s"}+ " or t2." + self.matchStatus%{"Status":"%(Status2)s"}+")"
        return self.db.select("TransactionData t1", col, joinTables, conditions, where, UserID= userid, Status1=tables.TransactionState.DONE.value, Status2=tables.TransactionState.WAIT.value)

    def addNewProduct(self, name, make, price, stock = 0, imagepath = "") :
        """
        Adds a product to database
        """
        if imagepath:
            values = "%s, %s, %s, %s, %s" 
            self.db.insertIntoTable(tables.productsInsertImage, values, (name, make, price, stock, imagepath))
        else:
            values = "%s, %s, %s, %s"
            self.db.insertIntoTable(tables.productsInsert, values, (name, make, price, stock))
        self.db.commit()

    def getProducts(self):
        answer = self.db.select("Products")
        return answer

    def postReview(self, pid, uid, rating, comment):
        uid = self.decrypt(uid)
        if self.db.select("Review", where = self.matchPid + " and " + self.matchUserID, PID = pid, UserID = uid):
            self.db.update("Review", "Rating", rating, where = self.matchPid + " and " + self.matchUserID, PID = pid, UserID = uid)
            if comment:
                self.db.update("Review", "Comment", comment, where = self.matchPid + " and " + self.matchUserID, PID = pid, UserID = uid)
            self.db.commit()
            return
        if comment:
            values = "%s, %s, %s,%s"
            self.db.insertIntoTable("Review", values, (pid, uid, rating, comment))
        else:
            values = "%s, %s, %s, NULL" %(pid, uid, rating)
            self.db.insertIntoTable("Review", values, (pid, uid, rating))
        self.db.commit()

    def getReviews(self, pid):
        answer = self.db.select("Review t1", "ProductID, Username, Rating, Comment", ["Accounts t2"], ["t1.UserID = t2.UserID"], where = self.matchPid, PID = pid)
        return answer

    def getProduct(self, pid):
        answer = self.db.select("Products", where=self.matchPid, PID = pid)
        if answer:
            return answer[0]
        return ()

    def hasProduct(self, pid = 0, pname = "", pmake = ""):
        if not pid and not (pname and pmake):
            return True
        if pid:
            return bool(self.db.select("Products", where=self.matchPid, PID = pid))
        else:
            return bool(self.db.select("Products", where=self.matchName + " and " + self.matchMake, Name = pname, Make = pmake))

    def increaseStock(self, pid, amount):
        """
        increase stock by a given amount
        """
        answer = self.db.select("Products", col='InStock', where=self.matchPid, PID = pid)
        stock = amount+answer[0][0]
        if(stock >= 0):
            return self.db.update("Products", "InStock", stock, where = self.matchPid, PID = pid)
        return False

    def setStock(self, pid, stock, tag = ""):
        """
        Set stock of product
        """
        if(stock  >= 0):
            return self.db.update("Products"+tag, "InStock", stock, where = self.matchPid, PID = pid)
        return False

    def setPrice(self, pid, price):
        if(price >= 0):
            return self.db.update("Products", "Price", price, where = self.matchPid, PID = pid)
        return False

    def addImagePath(self, pid, imagepath):
        """
        Adds image to product
        """
        return self.db.update("Products", "Image", imagepath, where=self.matchPid, PID = pid)

    
    def close(self):
        """
        Closes connection to db
        """
        self.db.close()

"""
testing = True
if __name__ == "__main__" and testing:
    db = labdb()
    if True:

        user = "testuser"
        email = "testmail@mail.com"
        pw = "pw"
        print(db.hasProduct(1))
        db.regUser(user, email, pw)
        db.addNewProduct("cykel","disney",999, imagepath="/images/image1.png")
        print(db.hasUserWith(user, email))
        print(db.hasUserWith(user))
        print(db.hasUserWith(email = email))
        
        userid = db.validateUser(user, pw)
        print(db.getUserName(userid))
        #print(db.addToCart(userid, 1, 1))
        #print(db.addToCart(userid, 1, 1))
        print(db.setStock(1, 20))
        print(db.getBasket(userid))
        print(db.checkout(userid))
        print(db.getBasket(userid))
        db.close()
    else:
        print("except")
        db.close()
"""