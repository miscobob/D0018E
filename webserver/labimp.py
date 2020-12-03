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
            
    """
    Insert values into table, both table and values should both be pre-generated strings to be so it matches
    wished insert, this method autocommits, should not be done togheter with a transaction
    """
    def insertIntoTable(self, table, values):
        self.testConnection()
        self.dbCursor.execute('INSERT INTO ' + table + ' VALUES('+values + ')')
        self.dbConnection.commit()
            
    """
    returns query from given table with the option
    to select specific collumns from table and match specific values in tables.
    When matching strings use taged string formating to set string to compare to.
    Where string as element in kwargs and key to that element is the tag for where
    that string should be placed
    """
    def select(self, tables, col = '*', where = "", **kwargs):
        self.testConnection()
        tbl = []
        statement ="SELECT "+col+" FROM "+tables
        if where:
            statement+=" WHERE "+ where
        self.dbCursor.execute(statement, kwargs)
        for row in self.dbCursor:
            tbl.append(row)
        return tbl

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
        self.accountsTable = 'Accounts (UserName, Email, Password, AccessLevel)'
        self.accountsValues = '(%(UserName)s, %(Email)s, %(Password)s, %(AccessLevel)s)'
        self.matchUserID = 'UserID = %(UserID)s'
        self.matchUserName = 'UserName = %(UserName)s'
        self.matchPassword = 'Password = %(Password)s'
        self.matchEmail = "Email = %(Email)s"
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
    """
    Registers a account as user with given email and given password with a given accvlvl
    """
    def regAccount(self, user, email, pw, acclvl):
        values = "'%s', '%s', '%s', '%s'" % (user, email, pw, acclvl)
        self.db.insertIntoTable(self.accountsTable, values)
    """
    Registers a Website-user as user with given email and given password
    """
    def regUser(self, user, email, pw):
        self.regAccount(user, email, pw, 'user')
        self.db.createTable(tables.transaction, UserID = self.db.select("Accounts", col = "UserID", where = self.matchUserName, UserName = user)[0][0])

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
        answer = self.db.select("Accounts", col = "UserName", where= self.matchUserID, UserID = self.crypto.decrypt(userid).decode("utf-8"))
        if answer:
            return answer[0][0]
        else:
            return ""
    
    def sql_insert(self, id, name):
        self.db.dbCursor.execute("INSERT INTO test VALUES(" +id+ ',"' +name+ '")')
        self.db.dbConnection.commit()

    """
    validates a user log in attempt
    """
    def validateUser(self, username, password):
        answer = self.db.select("Accounts", where = self.matchUserName+ " and "+ self.matchPassword , UserName = username, Password = password)
        if answer:
            return self.crypto.encrypt(str(answer[0][0]).encode("utf-8"))
        else:
            return ""
    """
    Closes connection to db
    """
    def close(self):
        self.db.close()


testing = True
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
    
