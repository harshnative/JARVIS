import sqlite3
from tabulate import tabulate
import os
from getpass import getpass
import onetimepad


class PasswordStorerClass:

    # constructor
    def __init__(self):
        self.tableNameForDB = "PASSWORDSTORER"
        self.dataBaseFileName = "Jarvis.db"
        self.connectionObj = None
        self.password = None
        self.oldPassword = None
    

    # function to find whether a word is present in string or not
    def isSubString(self , string , subString):
        lengthOfSubString = len(subString)
        for i,j in enumerate(string):
            if(j == subString[0]):
                if(subString == string[i:i+lengthOfSubString]):
                    return True 
                else:
                    pass
        return False


    # function to connect to the dataBase file
    def connectToDB(self):
        self.connectionObj = sqlite3.connect("C:/programData/Jarvis/" + self.dataBaseFileName)


    # function to create table in data base file
    def createTable(self):
        # generating query for sqlite3 obj to execute
        stringToPass = "CREATE TABLE " + self.tableNameForDB + ''' (PASSWORD_FOR   TEXT   NOT NULL ,
                                                                    PASSWORD_VALUE   TEXT   NOT NULL
                                                                    );'''
        try:
            self.connectionObj.execute(stringToPass)
        except Exception:
            pass


    # function to add contents to the table in DB
    def addToTable(self , key , value):
        # generating query for sqlite3 obj to execute
        stringToPass = "INSERT INTO " + self.tableNameForDB + " (PASSWORD_FOR , PASSWORD_VALUE) VALUES ( " + "'" + str(key) + "'" + " , " + "'" + str(value) + "'" + " )"
        self.connectionObj.execute(stringToPass)
        self.connectionObj.commit()


    # function to update contents to the table in DB
    def updateInTable(self, key , updateValue):
        # generating query for sqlite3 obj to execute
        stringToPass = "UPDATE " + self.tableNameForDB + " set PASSWORD_VALUE = " + "'" + str(updateValue) + "'" + " where PASSWORD_FOR = " + "'" + str(key) + "'"
        cursor = self.connectionObj.execute(stringToPass)
        self.connectionObj.commit()


    # function to delete content from table in DB
    def deleteFromTable(self , key):
        # generating query for sqlite3 obj to execute
        stringToPass = "DELETE from " + self.tableNameForDB + " where PASSWORD_FOR = " + "'" + str(key) + "'" + ";"
        cursor = self.connectionObj.execute(stringToPass)
        self.connectionObj.commit()


    # function to display all the contents from the table in DB
    def displayAll(self):
        # generating query for sqlite3 obj to execute
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        tabulateList = []
        for row in cursor:
            # master password stored - so cannot be shown in which we have stored it to user
            if(row[0] == "!@#$%^&*("):
                    pass
            else:
                # getting list for tablute module to show data
                tempList = []
                tempList.append(str(row[0]))
                tempList.append(self.decryptThing(str(row[1]) , self.password))
                tabulateList.append(tempList)
        
        # showing the data 
        os.system("cls")
        print(tabulate(tabulateList, headers=['Site', 'Password']))


    # function to display certain items only based on search
    def displaySearch(self , searchItem):
        # generating query for sqlite3 obj to execute
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        tabulateList = []
        for row in cursor:
            if(self.isSubString(row[0] , searchItem)):
                if(row[0] == "!@#$%^&*("):
                    pass
                else:
                    # generating list for tabulate module
                    tempList = []
                    tempList.append(str(row[0]))
                    tempList.append(self.decryptThing(str(row[1]) , self.password))
                    tabulateList.append(tempList)
        
        # showing the data
        os.system("cls")
        print(tabulate(tabulateList, headers=['Site', 'Password']))


    # function to set Password for encryption
    def setPass(self):

        # infinite loop for if the password does not match while entering
        while(1):
            os.system("cls")
            passwordInput1 = str(getpass("Enter  New  Master Password : "))
            passwordInput2 = str(getpass("Enter Master Password again : "))

            # checking if the password are same or not to avoid miss entering of password
            if(passwordInput1 == passwordInput2):
                passwordInput1 = self.encryptThing(passwordInput1 , passwordInput2)

                # adding password to data base and class variable
                self.addToTable("!@#$%^&*(" , passwordInput1)
                self.password = passwordInput2
                print("congo , new Password setted successfully")
                break

            # if the password does not match , continue the loop
            else:
                print("\nPassword did not match\n")
                os.system("pause")


    # function to authenticate - checking whether the password stored in the database is this or not
    # we do this by getting the password from the DB and decrypting it with the key = password enter , now if both match then we got the rigth user
    # returns bool value
    def authenticate(self):
        os.system("cls")
        passwordInput = str(getpass("Enter Master Password : "))

        # generating query for sqlite3 obj to execute
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        for row in cursor:
            if(row[0] == "!@#$%^&*("):
                passwordFromDataBase = row[1]
                passwordFromDataBase = self.decryptThing(passwordFromDataBase , passwordInput)
                if(passwordFromDataBase == passwordInput):
                    self.password = passwordInput
                    self.oldPassword = passwordInput
                    return True
        
        else:
            return False


    # function for changing the password
    # it is bit more complicated as we to encrypt all passwords again with the key = newPassword    
    def changePassword(self):
        while(1):

            # you can only change password if you are rigth user
            if(self.authenticate()):
                self.deleteFromTable("!@#$%^&*(")
                self.setPass()

                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)
                
                # just to create "\n"
                print()

                for row in cursor:
                    # do not want to change master password as it as already been updated
                    if(row[0] == "!@#$%^&*("):
                        pass
                    else:
                        # getting passwords
                        old = row[1]
                        # decryting it 
                        new = self.decryptThing(old, self.oldPassword)
                        # encrypting it again with new password
                        new = self.encryptThing(new, self.password)
                        key = row[0]
                        value = new
                        # updating the values in the DB
                        self.updateInTable(key , value)

                print("\n\nPassword changed successfully")
                break

            else:
                print("Wrong password...")
                os.system("pause")


    # function for encrypting a thing with the key passed
    def encryptThing(self , thing , key):
        stringToReturn = onetimepad.encrypt(thing , key)
        return str(stringToReturn)


    # function for decrypting a thing with the key passed
    def decryptThing(self , thing , key):
        stringToReturn = onetimepad.decrypt(thing , key)
        return str(stringToReturn)


    # function for Getting things done
    def getDone(self , commandList):

        try:
            # for adding things to DB
            if("-a" in commandList):
                os.system("cls")
                x = input("Enter Website name for future referencing : ") 
                y = input("Enter the Password : ")

                y = self.encryptThing(y , self.password)

                self.addToTable(str(x) , str(y))
                return True

            # for deleting things
            elif("-d" in commandList):
                os.system("cls")
                webDelete = input("Enter the Website name for deletion : ")
                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)

                listToDelete = []
                indexCount = 1
                count = 0

                os.system("cls")
                for row in cursor:
                    if(self.isSubString(row[0] , webDelete)):
                        print(indexCount , end = " : ")
                        print("Site - ", row[0])
                        listToDelete.append(row[0])
                        indexCount += 1
                        count += 1
                    
                if(count > 0):
                    print("\nEnter Index for deletion (space seperated for multiple) , Enter 0 to delete all : ")
                    indexList = [int(x) for x in input().split()]

                    print("Press enter to confirm delete , Notice - ones deleted you cannot get them back")
                    input()

                    for i,j in enumerate(listToDelete):
                        if(i+1 in indexList):
                            self.deleteFromTable(str(j))
                        elif(0 in indexList):
                            self.deleteFromTable(str(j))

                    print("\nDeleted successfully :)")

                else:
                    os.system("cls")
                    print("No website found........")
                
                return True
        
            # for updating things
            elif("-u" in commandList):
                os.system("cls")
                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)
                
                toUpdate = input("Enter the website name to update : ")
                toUpdateList = []

                indexCount = 1
                
                for row in cursor:
                    if(self.isSubString(row[0] , toUpdate)):
                        print(indexCount , end = " : ")
                        print("Site - ", row[0] , end = "    ")
                        print("Old Password - " , row[1])
                        toUpdateList.append(row[0])  

                indexInput = int(input("\nEnter Index for update\n"))

                for i,j in enumerate(toUpdateList):
                    if(i+1 == indexInput):
                        print("Enter the Updated Password : ")
                        updated = input()
                        updated = self.encryptThing(updated , self.password)
                        self.updateInTable(str(j) , str(updated))
                
                print("Value updated successfully")
                return True

            # for seeing all the things in the DB
            elif("-sa" in commandList):
                self.displayAll()
                return True

            # displaying things in the DB according to search query
            elif("-s" in commandList):
                os.system("cls")
                searchItem = input("Enter the website name to display Password : ")
                self.displaySearch(searchItem)
                return True

            # for changing password
            elif("-c" in commandList):
                self.changePassword()
                return True
            
            return False

        except Exception:
            os.system("cls")
            print("Oops something went wrong :( ")

    # fuction for driving all the things
    def driverFunc(self):
        self.connectToDB()
        self.createTable()

        # generating query for sqlite3 obj to execute
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        count = 0

        # checking whether it is users first time or not
        for row in cursor:
            if (row[0] == "!@#$%^&*("):
                self.passwordFromDB_encrypted = row[1]
                count += 1
        
        # if it is first time then he is required to set a password
        if(count == 0):
            self.setPass()
            print("\n\n")
            os.system("pause")

        # checking whether the user is right or not
        while(1):
            if(self.authenticate()):
                break
            else:
                print("wrong password....")
                os.system("pause")
        
        os.system("cls")

        # starting module
        while(1):
            # taking command
            stringOfCommandInput = input("Enter Command For Password Manager in JARVIS : ")
            
            # generating commandList from input
            commandList = list(stringOfCommandInput.split())
            if("exit" in commandList):
                break
            else:
                # calling function to execute command
                if(self.getDone(commandList)):
                    pass
                else:
                    os.system("cls")
                    print("Sorry , cannot recognise the command :(\n")
            
            print("\n\n")
            os.system("pause")
            os.system("cls")


# just for testing purpose
if __name__ == "__main__":
    obj = PasswordStorerClass()
    obj.driverFunc()
