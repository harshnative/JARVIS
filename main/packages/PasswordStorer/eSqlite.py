# import easySQLite.SED as SED
from . import SED
import sqlite3 as sq
from tabulate import tabulate


# some of the global methods that will not be accesed by normal user of this module
class ESQLiteGlobalMethods:

    # function to tell if the string has the passed subString
    @classmethod
    def isSubString(cls , string, subString):
        string = str(string)
        subString = str(subString)

        lengthOfSubString = len(subString)
        try:
            for i, j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        return True
                    else:
                        pass
            return False
        except Exception:
            return False





# main class
class SQLiteConnect:

    def __init__(self):

        # to tell if the security is on in data base or not
        self.security = False

        # object for the SED module
        self.objSecurity = SED.ED()

        # connObj to the data base
        self.connObj = None

        # dataBase name
        self.dataBaseName = None

        # to add to table name when table is secured
        self.tableNameAdd = "secured_usingSED"

        # name of the password storing table
        self.passwordStorerTable = "password storer table , 0b242ba11ab4a144a48cd25e88b98d161a7ba1c68ad65646cb9207f66aee1a64"

        # table name which the module is currently working on
        self.tableName = None

    
    # function to enable to database encryption and to set password as well
    def setPassword(self , password , pin = 123456):
        """return None if the password not present in data base before (first time use)
        return True if the password and pin are setted correctly
        return False if the authentication failed"""

        self.objSecurity.setPassword_Pin(password , pin)

        # storing the current table name to restore it later
        tempTableName = self.tableName 

        # content list for generating the password table
        contentList = [["PASS" , "TEXT" , 1]]

        tempSecurity = self.security

        try:
            # exception will be raised if the table already exist or some problem occur

            # security needs to turned on to add self.tableNameAdd to tableName while creating table
            self.security = True

            # creating table
            self.createTable(self.passwordStorerTable , contentList , True)

            valuesList = [self.objSecurity.returnPassForStoring()]
            self.insertIntoTable(valuesList , forPass=True)

            # restoring data
            self.tableName = tempTableName
            self.security = tempSecurity
            return

        except Exception:

            # security needs to be off so that self.tbaleNameAdd is not added
            self.security = False

            # getting the current password stored in table
            data = self.returnDataOfKey(0 , self.passwordStorerTable + " " + self.tableNameAdd)
            
            data = data[0]
            data = data[1]

            self.security = tempSecurity
            self.tableName = tempTableName

            if(self.objSecurity.authenticatePassword(data , password , pin)):
                return True
            else:
                return False


    # function to encryt the things
    def encrypter(self , string):
        return self.objSecurity.encrypter(str(string))

    # function to decrypt the things
    def decrypter(self , string):
        return self.objSecurity.decrypter(str(string))


    # function for toggling the security status
    def setSecurityStatus(self , status = True):
        self.security = status

    
    # function to set the database name
    def setDatabase(self, dataBaseName):
        self.connObj = sq.connect(dataBaseName)
        self.dataBaseName = dataBaseName

    
    # function to get the database name
    def getDatabase(self):
        return self.dataBaseName
        

    # function to create the table
    def createTable(self, tableName , contentList , raiseException = False):
        """table parameters - 
        data types - INT TEXT REAL
        content List = [ [nameOfCol , dataBaseType , 0 for NULL or 1 for not NULL] , similar more objects ]
        
        raise exception is False so that if the table already exist it does not raise any exception
    
        but if you think their is some other problem then you make this true to see what is causing he problem"""
        
        # storing teh table name for further use
        self.tableName = str(tableName)

        # a secure tag will be added after the table name
        if(self.security and (not(ESQLiteGlobalMethods.isSubString(tableName , self.tableNameAdd)))):
            tableName = tableName + " " + self.tableNameAdd

        # generating the query string
        string = "CREATE TABLE " + "'" + tableName + "'" + " ("

        # adding ID
        string = string + "ID INT PRIMARY KEY     NOT NULL,"

        # adding rest of the content list
        for i in contentList:
            
            # adding the col name
            string = string + "'" + str(i[0]) + "'" + "    "

            # adding col data type 
            if(i[1] == "INT"):
                string = string + "INT" + "    "
            elif(i[1] == "REAL"):
                string = string + "REAL" + "    "
            else:
                string = string + "TEXT" + "    "

            # adding null or not null
            try:
                if(int(i[2]) == 1):
                    string = string + "NOT NULL,"
                else:
                    string = string + ","
            except IndexError:
                string = string + ","
        
        string = string[:-1] + ");"

        if(raiseException):
            self.connObj.execute(string)

        else:
            try:
                self.connObj.execute(string)
            except Exception:
                pass
            

    def getOperableTableName(self , tableName):

        # checking the module as some stored table name or not
        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        # self.tableNameAdd will be added so that secured table can be identified during password change 
        if(self.security):

            # need to be only added once
            if(not(ESQLiteGlobalMethods.isSubString(tableName , self.tableNameAdd))):
                tableName = tableName + " " + self.tableNameAdd


        return tableName



        
    
    # function to insert data into table
    def insertIntoTable(self, valuesList , keyPass = None , tableName = None , forPass = False , commit = True):

        tableName = self.getOperableTableName(tableName)

        # getting the key value if not passed
        if(keyPass == None):
            key = self.returnLastKey() 

            if(key == None):
                key = 0

            else:
                key = key + 1

        else:
            key = int(keyPass)

        # generating query string
        string = "INSERT INTO " + "'" + tableName + "'" + " ("

        # column list in the table
        colList = []

        # datatypes of the cols in the table
        dataTypeList = []

        # getting the table info
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        # generating col list and datatype list
        for i in cor:
            colList.append(i[1])
            dataTypeList.append(i[2])
        
        # adding cols to query
        for i in  colList:
            string = string + "'" + i + "'" + ","

        string = string[:-1] + " ) VALUES (" + str(key) + ","

        tempCount = 1
        
        # adding values to query
        for i in valuesList:

            # if the encryption is on then it will be always text 
            # also while insert data into the password table , it should not be encrypted further
            if(self.security and (not(forPass))):
                string = string + "'" + self.encrypter(i) + "'" + ","

            else:
                # checking the col data is of INT or REAL
                if((dataTypeList[tempCount] == "INT") or (dataTypeList[tempCount] == "REAL")):
                    string = string + str(i) + ","
                else:
                    string = string + "'" + i + "'" + ","

            tempCount += 1

        string = string[:-1] + " )"

        self.connObj.execute(string)

        if(commit):
            self.connObj.commit()


    # function to return the last ID
    # id will be none if no data is present in table
    def returnLastKey(self , tableName = None):

        tableName = self.getOperableTableName(tableName)

        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")

        id = None

        for row in cursor:
            id = int(row[0])

        return id

    
    # print data of a particular key
    def printDataOfKey(self, key , errorMessage = "key could not be found" , tableName = None):

        tableName = self.getOperableTableName(tableName)

        # column list in the table
        colList = []

        # datatypes of the cols in the table
        dataTypeList = []

        # getting the table info
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        # generating col list and datatype list
        for i in cor:
            colList.append(i[1])
            dataTypeList.append(i[2])

        table = []
        found = False

        # prasing through the table
        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")

        for row in cursor:
            tempTable = []
            
            # the key matches with id in table
            if(int(row[0] == key)):
                count = 0

                # adding all the cols data
                for i,j in zip(colList , dataTypeList):

                    # ID is not encryted
                    # things will be conv to respective data type after decryption
                    if(self.security and (i != "ID")):
                        if(j == "TEXT"):
                            try:
                                tempTable.append(self.decrypter((row[count])))
                            except Exception:
                                tempTable.append(None)
                        elif(j == "INT"):
                            try:
                                tempTable.append(int(self.decrypter((row[count]))))
                            except ValueError:
                                tempTable.append((self.decrypter((row[count]))))
                            except Exception:
                                tempTable.append(None)
                        else:
                            try:
                                tempTable.append(float(self.decrypter((row[count]))))
                            except ValueError:
                                tempTable.append((self.decrypter((row[count]))))
                            except Exception:
                                tempTable.append(None)

                    # if the data is not ecrypted
                    else:    
                        tempTable.append(row[count])
                    count += 1
                found = True
        
            if(len(tempTable) > 0):
                table.append(tempTable) 

        if(found):
            print(tabulate(table, headers=colList))
        else:
            print(errorMessage)


    
    # print entire data in a table
    def printData(self , errorMessage = "No data in table" , tableName = None):

        tableName = self.getOperableTableName(tableName)

        # column list in the table
        colList = []

        # datatypes of the cols in the table
        dataTypeList = []

        # getting the table info
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        # generating col list and datatype list
        for i in cor:
            colList.append(i[1])
            dataTypeList.append(i[2])

        table = []
        found = False

        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")

        for row in cursor:
            tempTable = []
        
            count = 0

            # getting all col data
            for i,j in zip(colList , dataTypeList):
                
                # ID is not encrypted
                if(self.security and (i != "ID")):
                    if(j == "TEXT"):
                        try:
                            tempTable.append(self.decrypter((row[count])))
                        except Exception:
                            tempTable.append(None)
                    elif(j == "INT"):
                        try:
                            tempTable.append(int(self.decrypter((row[count]))))
                        except ValueError:
                            tempTable.append((self.decrypter((row[count]))))
                        except Exception:
                            tempTable.append(None)
                    else:
                        try:
                            tempTable.append(float(self.decrypter((row[count]))))
                        except ValueError:
                            tempTable.append((self.decrypter((row[count]))))
                        except Exception:
                            tempTable.append(None)
                
                # if the data is not encrypted
                else:    
                    tempTable.append(row[count])
                count += 1
            found = True
        
            table.append(tempTable)

        if(found):
            print(tabulate(table, headers=colList))
        else:
            print(errorMessage)


    # in built tabulate printer
    def tabulatePrinter(self , table , headersList):
        print(tabulate(table, headers=headersList))



    # return data of a particular key
    # returns none if not found
    def returnDataOfKey(self, key , tableName = None):

        tableName = self.getOperableTableName(tableName)

        # column list in the table
        colList = []

        # datatypes of the cols in the table
        dataTypeList = []

        # getting the table info
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        # generating col list and datatype list
        for i in cor:
            colList.append(i[1])
            dataTypeList.append(i[2])

        table = []

        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")

        for row in cursor:
            tempTable = []
            
            if(int(row[0] == key)):
                count = 0

                # adding all the cols data
                for i,j in zip(colList , dataTypeList):
                    if(self.security and (i != "ID")):
                        if(j == "TEXT"):
                            try:
                                tempTable.append(self.decrypter((row[count])))
                            except Exception:
                                tempTable.append(None)
                        elif(j == "INT"):
                            try:
                                tempTable.append(int(self.decrypter((row[count]))))
                            except ValueError:
                                tempTable.append((self.decrypter((row[count]))))
                            except Exception:
                                tempTable.append(None)
                        else:
                            try:
                                tempTable.append(float(self.decrypter((row[count]))))
                            except ValueError:
                                tempTable.append((self.decrypter((row[count]))))
                            except Exception:
                                tempTable.append(None)
                    
                    # if not encrypted
                    else:    
                        tempTable.append(row[count])
                    count += 1

            
            if(len(tempTable) > 0):
                table.append(tempTable) 

        if(len(table) > 0):
            return table
        else:
            return None


    
    # return entire data in a table
    # returns None if no data is present
    # i[1] of this list is the list of col names 
    def returnData(self , tableName = None):

        tableName = self.getOperableTableName(tableName)

        # column list in the table
        colList = []

        # datatypes of the cols in the table
        dataTypeList = []

        # getting the table info
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        # generating col list and datatype list
        for i in cor:
            colList.append(i[1])
            dataTypeList.append(i[2])

        table = []

        table.append(colList)

        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")

        for row in cursor:
            tempTable = []
        
            count = 0

            # getting all col data
            for i,j in zip(colList , dataTypeList):
                
                if(self.security and (i != "ID")):
                    if(j == "TEXT"):
                        try:
                            tempTable.append(self.decrypter((row[count])))
                        except Exception:
                            tempTable.append(None)
                    elif(j == "INT"):
                        try:
                            tempTable.append(int(self.decrypter((row[count]))))
                        except ValueError:
                            tempTable.append((self.decrypter((row[count]))))
                        except Exception:
                            tempTable.append(None)
                    else:
                        try:
                            tempTable.append(float(self.decrypter((row[count]))))
                        except ValueError:
                            tempTable.append((self.decrypter((row[count]))))
                        except Exception:
                            tempTable.append(None)

                # if not encrypted
                else:    
                    tempTable.append(row[count])
                count += 1
        
            table.append(tempTable)

        if(len(table) > 0):
            return table
        else:
            return None



    # function for updating a col data in row of particular key
    # returns True if key was found and operation was sucessfull
    # return False else wise
    def updateRow(self , colName , value , key , tableName = None , commit = True):

        tableName = self.getOperableTableName(tableName)

        # query string
        string = "UPDATE " + "'" + tableName + "'" + " set " + "'" + str(colName) + "'" + " = "

        # gettign table info 
        cor = self.connObj.execute("PRAGMA table_info(" + "'" + tableName + "'" + ")")

        if(self.security):

            # id is not ecnrypted
            if(colName != "ID"):
                string = string + "'" + self.encrypter(value) + "' "
            else:
                string = string + str(value) + " "

        else:

            # finding if the value to be updated is text or not
            valueIsText = False

            for i in cor:
                if(i[1] == colName):
                    if(i[2] == 'TEXT'):
                        valueIsText = True

            if(valueIsText):
                string = string + "'" + value + "' "
            else:
                string = string + str(value) + " "

        string = string + "where ID = " + str(key)

        self.connObj.execute(string)

        if(commit):
            self.connObj.commit()


    # function for deleting a row
    def deleteRow(self, key , updateId = False , tableName = None , commit = True):

        tempTableName = tableName

        tableName = self.getOperableTableName(tableName)

        # query
        string = "DELETE from " + "'" + tableName + "'" + " where ID = " + str(key) + ";"

        self.connObj.execute(string)

        if(commit):
            self.connObj.commit()

        if(updateId):
            self.updateIDs(tempTableName , commit=commit)

    
    # updated id's function
    def updateIDs(self , tableName = None , commit = True):

        tempTableName = tableName

        tableName = self.getOperableTableName(tableName)

        # getting col list 
        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")
        colList = list(map(lambda x: x[0], cursor.description))

        # updating the ids
        string = "SELECT "

        for i in colList:
            string = string + "'" + i + "'" + ","
        
        string = string[:-1] + " from " + "'" + tableName + "'"

        cursor = self.connObj.execute(string)

        count = 0

        for row in cursor:
            if(row[0] == "ID"):
                pass
            elif(int(row[0]) == count):
                pass
            else:
                self.updateRow("ID" , count , row[0] , tempTableName , commit)
            
            count = count + 1

        if(commit):
            self.connObj.commit()


    # function to upadte the entire row corresponding to a key
    def updateEntireRow(self , valuesList , key , tableName = None , commit = True):

        tempTableName = tableName

        tableName = self.getOperableTableName(tableName)

        key = int(key)

        count = 1

        # getting col list
        cursor = self.connObj.execute('select * from ' + "'" + tableName + "'")
        colList = list(map(lambda x: x[0], cursor.description))

        for i in valuesList:
            self.updateRow(colList[count] , i , key , tempTableName , commit)
            count = count + 1 


    def delEntireTable(self , tableName = None , commit = True):

        tableName = self.getOperableTableName(tableName)
    
        string = "DROP TABLE " + "'" + tableName + "'"

        self.connObj.execute(string)

        if(commit):
            self.connObj.commit()

    
    # function to add a col to data base
    def addColToTable(self , colName , dataType = "TEXT" , NULL = False , tableName = None , commit = True):

        tableName = self.getOperableTableName(tableName)

        string = "alter table " + "'" + tableName + "'" + " add column " + "'" + colName + "'" + "    " + dataType + "    " +  "'" + str(int(NULL)) + "'"
        self.connObj.execute(string)

        if(commit):
            self.connObj.commit()

    
    def changePassword(self , oldPassword , newPassword , oldPin = 123456 , newPin = 123456):
        
        # if their is not password in db then no need to do operation
        # operation will fail if the wrong credentials are provided
        status = self.setPassword(oldPassword , oldPin)

        if(status == None):
            return True
        
        elif(status == False):
            return False

        # getting the tableNames
        tableNames = self.connObj.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # adding tableNames to a list
        tableNamesList = []

        for i in tableNames:
            tableNamesList.append(i[0])

        # reserving the current tableName in obj
        tempTableName = self.tableName
        tempSecurity = self.security

        # traversing each table
        for i in tableNamesList:

            # if the table contains secured by SED then we need to update that table as it has to be now encrypted and decrypted by the new password
            # also the password storer table is not affected , it is changed that last
            if(ESQLiteGlobalMethods.isSubString(i , self.tableNameAdd) and (not(ESQLiteGlobalMethods.isSubString(i , "0b242ba11ab4a144a48cd25e88b98d161a7ba1c68ad65646cb9207f66aee1a64")))):

                # setting the old credentails for decrypting
                self.objSecurity.setPassword_Pin(oldPassword , oldPin)

                # getting the table data 
                tableData = self.returnData(i)

                # getting the col details
                cor = self.connObj.execute("PRAGMA table_info(" + "'" + i + "'" + ")")

                contentList = []

                # setting new credentials for ecryption
                self.objSecurity.setPassword_Pin(newPassword , newPin)

                # generating the content list
                for j in cor:

                    if(not(j[1] == "ID")): 
                        tempList = []

                        # col name
                        tempList.append(j[1])

                        # data type
                        tempList.append(j[2])

                        # null or not null
                        tempList.append(j[3])
                        contentList.append(tempList)

                # deleting the old table
                self.delEntireTable(i)

                # creating new table 
                self.security = True
                self.createTable(i , contentList , True)

                # getting the no of cols
                lenCol = len(tableData[1])

                # the ids id in the table data will not be added to value list
                for j in tableData:
                    if(not(j[0] == "ID")):
                        valueList = []
                        count = 1

                        # adding data to value list - id will not be added
                        while(count < lenCol):
                            valueList.append(j[count])
                            count += 1

                        # inserting the data into table 
                        self.security = True
                        self.insertIntoTable(valueList)

        # restting the password table with new credentials
        self.delEntireTable(self.passwordStorerTable + " " + self.tableNameAdd)
        self.setPassword(newPassword , newPin)

        # restoring prev obj data
        self.security = tempSecurity
        self.tableName = tempTableName

    
    def checkForPasswordTable(self):
        tableNames = self.connObj.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for i in tableNames:
            if(i[0] == (self.passwordStorerTable + " " + self.tableNameAdd)):
                return True
        
        return False








# for testing purpose
if __name__ == "__main__":
    
    obj = SQLiteConnect()

    obj.setDatabase("test.db")

    print(obj.checkForPasswordTable())

    print(obj.setPassword("hello boi"))

    obj.setSecurityStatus(True)

    contentList = [["test1 456" , "TEXT" , 1] , ["test2  456" , "TEXT" , 1] , ["test3    456" , "INT" , 0]]

    obj.createTable("testTable" , contentList)

    valuesList = ["hello" , "world" , 123]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello1" , "world1" , 456]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello3" , "world3" , 789]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello4" , "world4" , 1234]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello5" , "world45" , 5678]

    obj.insertIntoTable(valuesList)

    obj.printData()

    obj.updateRow("test1 456" , "hello69" , 3)

    print("\n\n")
    obj.printData()

    obj.deleteRow(2)

    print("\n\n")
    obj.printData()

    valuesList = ["hello55" , "world455" , 91234]

    obj.insertIntoTable(valuesList)

    print("\n\n")
    obj.printData()

    obj.deleteRow(4 , True)

    print("\n\n")
    obj.printData()

    # obj.delEntireTable()

    valuesList = ["hello555" , "world4555" , 456789]
    obj.updateEntireRow(valuesList , 2)

    print("\n\n")
    obj.printData()

    print("\n\n")
    print(obj.returnData())

    # obj.addColToTable("next")

    print(obj.changePassword("hello boi" , "hello boi my name is harsh"))

    print("isTable = " , obj.checkForPasswordTable())
    print(obj.setPassword("hello boi my name is harsh"))
    print("isTable = " , obj.checkForPasswordTable())

    print("\n\n")
    obj.printData()


# make the db delete fucntion as well 
# if to commit or not
# del col function using copying the data from table -> del table -> create new table 
# raise exception or not if wrong data type is passed  
# None error