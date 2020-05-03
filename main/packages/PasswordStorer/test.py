#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('DataBaseFiles/test.db')
print ("Opened database successfully")

stringToPass = "CREATE TABLE " + "HELL" + ''' (PASSWORD_FOR   TEXT   NOT NULL ,
                                                                    PASSWORD_VALUE   TEXT   NOT NULL
                                                                    );'''
# stringToPass = "'''" + stringToPass + "'''"

print(stringToPass)
input()
try: 
    conn.execute(stringToPass)
except Exception:
      print("table already exist")
print ("Table created successfully")

conn.execute("INSERT INTO PASSWORDSTORE (PASSWORD_FOR , PASSWORD_VALUE) \
      VALUES ('amazon' , 'amazon.h')")

conn.execute("INSERT INTO PASSWORDSTORE (PASSWORD_FOR , PASSWORD_VALUE) \
      VALUES ('google' , 'googles.h')")

conn.commit()
print ("Records created successfully")
conn.close()

input()
conn = sqlite3.connect('DataBaseFiles/test.db')
print ("Opened database successfully")

cursor = conn.execute("SELECT PASSWORD_FOR , PASSWORD_VALUE from PASSWORDSTORE")
for row in cursor:
   print ("password for : ", row[0])
   print ("password value : ", row[1])

conn.close()