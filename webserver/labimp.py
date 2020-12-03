from cryptography.fernet import Fernet
import mysql.connector
from . import tables
#import tables

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
        
    def insertIntoTable(self, table, values):
        self.testConnection()
        #print('INSERT INTO ',table,' VALUES(',values,')')
        self.dbCursor.execute('INSERT INTO ' + table + ' VALUES('+values + ')')
        self.dbConnection.commit()
            
        
    def select(self, fromarg, col = '*', where = "", **kwargs):
        self.testConnection()
        tbl = []
        self.dbCursor.execute("SELECT "+col+" FROM "+fromarg+" WHERE " +where, kwargs)
        for row in self.dbCursor:
            tbl.append(row)
        return tbl
        
    def returnTable(self, table):
        self.testConnection()
        tbl = []
        self.dbCursor.execute('select * from '+table)
        for row in dbCursor:
            tbl.append(row)
        return tbl

    def createTable(self, table, **kwargs):
        print(table)
        self.testConnection()
        #print("CREATE TABLE IF NOT EXISTS " + table %kwargs)
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS " + table, kwargs)
        self.dbConnection.commit()

    def close(self):
        if not (self.dbCursor.close() or self.dbConnection.close()):
            print("failed to close")

    def testConnection(self):
        if not self.dbConnection.is_connected():
            self.reconnect()
    """
    Connect to mysql db
    """
    def connect(self):
        self.dbConnection = mysql.connector.connect(user=self.user, passwd=self.password, host=self.host)
        self.dbCursor = self.dbConnection.cursor(buffered=True)

    def reconnect(self):
        self.connect()
        self.dbConnection.database = self.name
        
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
        self.accountsTable = 'Accounts (UserName, Email, Password, AccessLevel)'
        self.accountsValues = '(%(UserName)s, %(Email)s, %(Password)s, %(AccessLevel)s)'
        self.matchUserID = 'UserID = %(UserID)s'
        self.matchUserName = 'UserName = %(UserName)s'
        self.matchPassword = 'Password = %(Password)s'
        self.matchEmail = "Email = %(Email)s"

    def isUserID(self, userid):
        return bool(self.getUserName(userid))
    
    def hasUserWith(self,username = "", email = ""):
        """
        Return if database either has a match for a given email or username,
        if neither username or email is set beyond default value return false
        """ 
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

    def regAccount(self, user, email, pw, acclvl):
        values = "'%s', '%s', '%s', '%s'" % (user, email, pw, acclvl)
        self.db.insertIntoTable(self.accountsTable, values)
        
    def regUser(self, user, email, pw):
        self.regAccount(user, email, pw, 'user')
        self.db.createTable(tables.transaction, UserID = self.db.select("Accounts", col = "UserID", where = self.matchUserName, UserName = user)[0][0])

    def regAdmin(self, user, email, pw):
        self.regAccount(user, email, pw, 'admin')

    def getUserName(self, userid):
        answer = self.db.select("Accounts", col = "UserName", where= self.matchUserID, UserID = self.crypto.decrypt(userid).decode("utf-8"))
        if answer:
            return answer[0][0]
        else:
            return ""
    
    def sql_insert(self, id, name):
        self.db.dbCursor.execute("INSERT INTO test VALUES(" +id+ ',"' +name+ '")')
        self.db.dbConnection.commit()

    def validateUser(self, username, password):
        answer = self.db.select("Accounts", where = self.matchUserName+ " and "+ self.matchPassword , UserName = username, Password = password)
        if answer:
            return self.crypto.encrypt(str(answer[0][0]).encode("utf-8"))
        else:
            return ""

    def close(self):
        self.db.close()


testing = False
if __name__ == "__main__" and testing:
    db = labdb()
    if True:
        user = "testuser"
        email = "testmail@mail.com"
        pw = "pw"
        db.regUser(user, email, pw)
        print(db.hasUserWith(user, email))
        print(db.hasUserWith(user))
        print(db.hasUserWith(email = email))
        userid = db.validateUser(user, pw)
        print(db.getUserName(userid))
        db.close()
    else:
        print("except")
        db.close()
    
