import mysql.connector

class databas:
    def __init__(self, usr, password, hst, dbname):
        self.db = mysql.connector.connect(user=usr, passwd=password, host=hst, database=dbname)
        self.conn = self.db.cursor()

    def insertIntoTable(self, table, values):
        conn.execute('INSERT INTO '+table+' VALUES('+values+')')
        self.db.commit()

    def returnTable(self, table):
        tbl = []
        self.conn.execute('select * from '+table)
        for row in conn:
            tbl.append(row)
        return tbl


class labdb:
    
    def __init__(self):
        self.db = databas('python', 'password', 'localhost', 'labdb')
        self.accountsTable = 'Accounts (UserName, E-mail, Password, Access-Level)'

    def req_user(self, user, email, pw):
        v = '\'' + user + '\','+ '\'' + email + '\','+ '\'' + pw + '\','
        self.db.insertIntoTable(self.accountsTable, v)


    def sql_insert(self, id, name):
        self.db.conn.execute("INSERT INTO test VALUES(" +id+ ',"' +name+ '")')
        self.db.db.commit()
