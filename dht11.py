from serial import Serial
import database
import time
import sys
import re

# init
db_name = "meteo"
host = "localhost"
username = "root"
password = ""
serialport = 'COM3'
frequence = 9600
query = "CREATE TABLE dht (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, temperature INT NOT NULL, humidity INT NOT NULL, seconds VARCHAR(255) NOT NULL)"
sql = "INSERT INTO dht(temperature, humidity, seconds) VALUES (%s, %s, %s)"


try:
    ########  DATABASE   #########
    connection = database.buildDB(db_name, host, username, password)
    cursor = database.getCursor(connection)
    cursor.execute("SHOW TABLES")
    tables = []
    for table in cursor:
        tables.append(table[0])
    if len(tables) == 0:
        cursor.execute(query)
        print("Table created...")

    ######## Serial COM  #########
    port = Serial(serialport, frequence)
    print("\n")
    print(port.readline().decode('utf-8'))
    while(1):            
        # Measure
        humidity = port.readline().decode('utf-8').split('\r\n')[0]
        temperature = port.readline().decode('utf-8').split('\r\n')[0]    
        
        # Time
        seconds = time.time()
        result = time.localtime(seconds)
        hh = result.tm_hour
        mm = result.tm_min
        
        #Database insertion
        val = (temperature, humidity, str(seconds))
        cursor.execute(sql, val)
        connection.commit()
        # print
        print(hh, ":", mm)
        print("Humidité: ", humidity, "%")
        print("Température: ", temperature, "C"); print()
except KeyboardInterrupt:
    print("Arret du programme ...")
    port.close()
except:
    erreur = re.sub(r"<class '", r"", str(sys.exc_info()[0]))
    erreur = re.sub(r"'>", r"", erreur)
    print("Erreur  : ", erreur)
    print("Message : ",sys.exc_info()[1])
    