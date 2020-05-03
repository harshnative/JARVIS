import sqlite3

class passwordStorerClass:

    def __init__(self):
        self.tableNameForDB = "PASSWORDSTORER"
        self.dataBaseFileName = "PASSWORD_DB.db"
        self.connectionObj = None
    
    def connectToDB(self):
        self.connectionObj = sqlite3.connect("DataBaseFiles/" + self.dataBaseFileName)

    def CreateTable(self):
        stringToPass = "CREATE TABLE " + self.tableNameForDB + ''' (PASSWORD_FOR   TEXT   NOT NULL ,
                                                                    PASSWORD_VALUE   TEXT   NOT NULL
                                                                    );'''
        try:
            self.connectionObj.execute(stringToPass)
        except Exception:
            pass

    def AddToTable(self , key , value):
        stringToPass = "INSERT INTO " + self.tableNameForDB + " (PASSWORD_FOR , PASSWORD_VALUE) VALUES ( " + "'" + str(key) + "'" + " , " + "'" + str(value) + "'" + " )"
        self.connectionObj.execute(stringToPass)
        self.connectionObj.commit()

    def displayAll(self):
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        for row in cursor:
            print("key : ", row[0] , end="    ")
            print("Value : ", row[1])

    def test(self):
        self.connectToDB()
        print("connected")
        self.CreateTable()
        print("table created")
        for i in range(3):
            self.AddToTable(input("enter key: ") , input("enter value: "))
        input()
        print("\n\n")
        self.displayAll()
        

if __name__ == "__main__":
    obj = passwordStorerClass()
    obj.test()
    print("\n\ndone")
