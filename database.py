import mysql.connector as db
    
def getConnection(myhost, myusername, mypassword, mydatabase):
    mydb = db.connect(
      host = myhost,
      user = myusername,
      passwd = mypassword,
      database = mydatabase
    )
    return mydb

def getCursor(connection):
    cursor = connection.cursor()
    return cursor
    
def isDatabase(db_name, cursor):
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        if x[0] == db_name:
            return True
    return False

def createDatabase(db_name, cursor):
    cursor.execute("CREATE DATABASE " + db_name)
    print("database " + db_name + " created ...")

def buildDB(db_name, host, username, password):
    connection = getConnection(host, username, password, "")
    cursor = getCursor(connection)
    if isDatabase(db_name, cursor) == False :
        createDatabase(db_name, cursor)
    connection.close()
    connection = getConnection(host, username, password, db_name)
    cursor = getCursor(connection)
    return connection