from datetime import datetime
from serial import Serial
import database
import time
import sys
import re

#####  INIT  #####
db_name    = "meteoo"
table_name = "dht"
host       = "localhost"
username   = "root"
password   = ""
serialport = 'COM3'
frequence  = 9600
query      = "CREATE TABLE " + table_name + " (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, temperature INT NOT NULL, humidity INT NOT NULL, dtime DATETIME)"
query_v    = "CREATE VIEW v_" + table_name + "s AS "
query_v   += 'SELECT DISTINCT  HOUR(dtime) as temps, CONCAT(DAY(dtime), "-", MONTH(dtime), "-", YEAR(dtime)) as d_time, AVG(temperature) as temperature,  AVG(humidity) as humidity'
query_v   += "FROM " + table_name + " GROUP BY temps, d_time"
sql        = "INSERT INTO dht(temperature, humidity, dtime) VALUES (%s, %s, %s)"
####         ####

try:
    ########  DATABASE   #########
    connection = database.buildDB(db_name, host, username, password)
    cursor = database.getCursor(connection)
    cursor.execute("SHOW TABLES")
    dp = 0
    for table in cursor:
        if table[0] == table_name or table[0] == "v_" + table_name + "s":
            dp = dp + 1
    if dp != 2:
        cursor.execute(query)
        print("Table created...")
        cursor.execute(query_v)
        print("View created...")

    ######## Serial COM  #########
    port = Serial(serialport, frequence)
    print("\n")
    print(port.readline().decode('utf-8'))
    while(1):            
        # Measure
        humidity = port.readline().decode('utf-8').split('\r\n')[0]
        temperature = port.readline().decode('utf-8').split('\r\n')[0]    
        
        # Time
        now = datetime.now()
        dtime = now.strftime('%Y-%m-%d %H:%M:%S')
        
        #Database insertion
        val = (temperature, humidity, dtime)
        cursor.execute(sql, val)
        connection.commit()
        # print
        print(now.strftime('%H:%M:%S'))
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