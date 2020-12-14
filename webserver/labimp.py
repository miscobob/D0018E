from cryptography.fernet import Fernet
import mysql.connector, os.path
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
    def insertIntoTable(self, table, values):
        self.testConnection()
        #print('INSERT INTO ' + table + ' VALUES('+values + ')')
        self.dbCursor.execute('INSERT INTO ' + table + ' VALUES('+values + ')')
        self.dbConnection.commit()
            
    """
    returns query from given table with the option
    to select specific collumns from table and match specific values in tables.
    When matching strings use taged string formating to set string to compare to.
    Where string as element in kwargs and key to that element is the tag for where
    that string should be placed
    """
    def select(self, table,  col = '*',joinTables = [], conditions = [], where = "" , **kwargs):
        self.testConnection()
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
        return tbl

    def update(self, table, setCol, setValue, where = "", **kwargs):
        self.testConnection()
        statement ="UPDATE "+table+" SET "+setCol+"="+setValue
        if where:
            statement += " WHERE "+where
        #print(statement % kwargs)
        self.dbCursor.execute(statement, kwargs)

    def delete(self, table, where):
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
    def transaction(self):
        return
        
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
        self.matchStatus = "Status = %(status)s"
        self.matchPid = "ProductID = %(PID)s"
        self.matchItem = "Item = %(Item)s"
        self.matchTransaction = "TransactionNumber = %(TransactionNumber)s"
        self.useridCrypt = lambda userid: self.crypto.encrypt(str(userid).encode("utf-8"))
        self.useridDecrypt = lambda userid: self.crypto.decrypt(userid).decode("utf-8") 
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
        values = "'%s', '%s', '%s', '%s'" % (user, email, pw, acclvl)
        self.db.insertIntoTable(tables.accountsInsert, values)

    """
    Registers a Website-user as user with given email and given password
    """
    def regUser(self, user, email, pw):
        self.regAccount(user, email, pw, 'user')
        
    """
    Registers a Website-manager as user with given email and given password
    """
    def regManager(self, user, email, pw):
        self.regAccount(user, email, pw, 'manager')

    """
    Registers a Website-admin as user with given email and given password
    """
    def regAdmin(self, user, email, pw):
        self.regAccount(user, email, pw, 'admin')

    """
    returns username with given userid if not any result return empty string
    """
    def getUserName(self, userid):
        userid = self.useridDecrypt(userid)
        answer = self.db.select("Accounts", col = "UserName", where= self.matchUserID, UserID = userid)
        if answer:
            return answer[0][0]
        else:
            return ""
    
    
    def validateUser(self, username, password):
        """
        validates a user log in attempt
        """
        answer = self.db.select("Accounts", col = "UserID", where = self.matchUserName+ " and "+ self.matchPassword , UserName = username, Password = password)
        if answer:
            return self.useridCrypt(answer[0][0])
        else:
            return ""

    def addToCart(self, userid, productid, nr):
        """
        Adds a product to a new basket transaction or to existing basket
        """
        userid = self.crypto.decrypt(userid).decode("utf-8")
        transaction = self.db.select("Transactions", col="TransactionNumber", where=self.matchStatus+" AND "+self.matchUserID, status = tables.TransactionState.BASKET.value, UserID = userid)
        if not transaction: # check if new basket needed
            values = "'%s', '%s'" % (userid, tables.TransactionState.BASKET.value)
            self.db.insertIntoTable(tables.transactionsInsert, values)
            transaction = self.db.select("Transactions", col="TransactionNumber", where=self.matchStatus+" AND "+self.matchUserID, status = tables.TransactionState.BASKET.value, UserID = userid)
            transnr = transaction[0][0]
        else:
            transnr = transaction[0][0]
            answer = self.db.select("TransactionData",col="Count", where = self.matchTransaction + " AND "+ self.matchItem, TransactionNumber =  transnr, Item = productid)
            if answer:
                count = answer[0][0]+nr
                if count > 0:
                    self.db.update("TransactionData", "Count", str(count), "TransactionNumber='%s' AND Item='%s'"%(transnr, productid))
                    self.db.commit()
                    return 0
                elif count == 0:
                    self.db.delete("TransactionData", "TransactionNumber='%s' AND Item='%s'"%(transnr, productid))
                    self.db.commit()
                    return 0
                else:
                    return 1
        if nr >= 1:
            self.db.insertIntoTable(tables.transactionDataInsert, "'%s', '%s', '%s'"%(transnr, productid, nr))
            return 0
        return 1
    
    def getBasketCount(self, userid, pid = 0):
        """
        Returns all products in basket or a given one
        return list if all otherwise return tuple
        col in order:
        production Id, image path, product name, name of product maker, amount in basket, price of product
        """
        userid = self.useridDecrypt(userid)
        joinTables = ["Products t2", "Transactions t3"]
        col = "Item, Image, Name, Make, Count, Price"
        conditions = ["t1.Item = t2.ProductID", "t1.TransactionNumber=t3.TransactionNumber"]
        if pid:
            where = "t3."+self.matchUserID+" and "+ "t3."+self.matchStatus + " and " +"t1."+self.matchItem
            answer = self.db.select("TransactionData" +" t1", col = col, joinTables = joinTables, conditions = conditions, where = where, UserID = userid, status = tables.TransactionState.BASKET.value, Item = pid)
            if answer:
                return answer[0]
            return ""
        else:
            where = "t3."+self.matchUserID+" and "+ "t3."+self.matchStatus
            answer = self.db.select("TransactionData" +" t1", col = col, joinTables = joinTables, conditions = conditions, where = where, UserID = userid, status = tables.TransactionState.BASKET.value)
            return answer

    def getBasket(self, userid):
        return self.getBasketCount(userid)

    def addNewProduct(self, name, make, price, stock = 0, imagepath = "") :
        if imagepath:
            values = "'%s', '%s', '%s', '%s', '%s'" % (name, make, price, stock, imagepath)
            self.db.insertIntoTable(tables.productsInsertImage, values)
        else:
            values = "'%s', '%s', '%s', '%s'" % (name, make, price, stock)
            self.db.insertIntoTable(tables.productsInsert, values)

    def getProducts(self):
        answer = self.db.select("Products")
        return answer

    def getProduct(self, pid):
        answer = self.db.select("Products", where=self.matchPid, PID = pid)
        if answer:
            return answer[0]
        return ()

    def setStock(self, pid, stock):
        if(stock  > 0 ):
            self.db.update("Products", "InStock", stock, where = self.matchPid, PID = pid)
            update(self, table, setCol, setValue, where = self.matchPid, PID = pid)

    def addImagePath(self, pid, imagepath):
        if(os.path.isfile(imagepath)):
            self.db.update("Products", "InStock", stock)
            update(self, table, setCol, setValue)
            return True
        return False

    """
    Closes connection to db
    """
    def close(self):
        self.db.close()

"""
testing = True
if __name__ == "__main__" and testing:
    db = labdb()
    if True:
        user = "testuser"
        email = "testmail@mail.com"
        pw = "pw"
        #db.regUser(user, email, pw)
        #db.addNewProduct("cykel","disney",999, imagepath="/images/image1.png")
        print(db.hasUserWith(user, email))
        print(db.hasUserWith(user))
        print(db.hasUserWith(email = email))
        userid = db.validateUser(user, pw)
        print(db.getUserName(userid))
        print(db.addToCart(userid, 1, 1))
        #print(db.addToCart(userid, 2, 1))
        print(db.getBasket(userid))
        print(db.getProduct(1))
        print(db.getProducts())
        db.close()
    else:
        print("except")
        db.close()  
"""