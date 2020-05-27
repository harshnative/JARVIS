import sqlite3
from tabulate import tabulate
import os
from getpass import getpass
import onetimepad
from packages.loggerPackage.loggerFile import *
import sys
import time
import pyperclip


class PasswordStorerClass:

    """
This class is the main class of the password module

methods included - 

driverFunc()        ->  this is the only method that you need to use this methods
                        this method accepts 1 argument - onlyAuthenticate Value
                        which is set to False by default 
                        
                        If the value passed is False , the the function is self sufficient
                        It will ask for input and show output on the inside itself
                        
                        If the value is True then it asks for the password 
                        and if you enter the correct password then it returns the entered password
                        if the entered password is incorrect then it will repeatedly ask for correct password
    """

    # constructor
    def __init__(self , troubleShootValuePass):
        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)
        self.tableNameForDB = "PASSWORDSTORER"
        self.dataBaseFileName = "Jarvis.db"
        self.connectionObj = None
        self.password = None
        self.oldPassword = None
        self.onlyAuthenticate = None
    

    # function to find whether a word is present in string or not
    def isSubString(self , string , subString):
        try:
            lengthOfSubString = len(subString)
            for i,j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        self.cLog.log("isSubStringFunc in mainForPassword" , "i")
                        return True 
                    else:
                        pass
            self.cLog.log("isSubStringFunc in mainForPassword" , "i")
            return False
        except Exception as e:
            self.cLog.log("isSubString function failed" , "e")
            self.cLog.exception(str(e) , "mainForPassword.py/isSubString_func")
            return False
        


    # function to connect to the dataBase file
    def connectToDB(self):
        try:
            self.connectionObj = sqlite3.connect("C:/programData/Jarvis/" + self.dataBaseFileName)
            self.cLog.log("connected to database" , "i")
        except Exception as e:
            self.cLog.log("cannot connect to dataBase in main for password" , "e")
            self.cLog.exception(str(e) , "mainForPassword.py/connectToDB")


    # function to create table in data base file
    def createTable(self):
        # generating query for sqlite3 obj to execute
        stringToPass = "CREATE TABLE " + self.tableNameForDB + ''' (PASSWORD_FOR   TEXT   NOT NULL ,
                                                                    PASSWORD_VALUE   TEXT   NOT NULL
                                                                    );'''
        try:
            self.connectionObj.execute(stringToPass)
            self.cLog.log("table created successfully in main for password" , "i")
        except Exception:
            self.cLog.log("table already exsist" , "w")


    # function to add contents to the table in DB
    def addToTable(self , key , value):
        # generating query for sqlite3 obj to execute
        try:
            stringToPass = "INSERT INTO " + self.tableNameForDB + " (PASSWORD_FOR , PASSWORD_VALUE) VALUES ( " + "'" + str(key) + "'" + " , " + "'" + str(value) + "'" + " )"
            self.connectionObj.execute(stringToPass)
            self.connectionObj.commit()
            self.cLog.log("added to table successfully in main for password" , "i")
        except Exception as e:
            toLog = "cannot add to table in main for password - query: " + stringToPass
            self.cLog.log(str(toLog) , "e")
            self.cLog.exception(str(e) , "mainForPassword.py/addToTable")


    # function to update contents to the table in DB
    def updateInTable(self, key , updateValue):
        # generating query for sqlite3 obj to execute
        try:
            stringToPass = "UPDATE " + self.tableNameForDB + " set PASSWORD_VALUE = " + "'" + str(updateValue) + "'" + " where PASSWORD_FOR = " + "'" + str(key) + "'"
            cursor = self.connectionObj.execute(stringToPass)
            self.connectionObj.commit()
            self.cLog.log("updated in table successfully in main for password" , "i")
        except Exception as e:
            toLog = "cannot update table in main for password - query: " + stringToPass
            self.cLog.log(str(toLog) , "e")
            self.cLog.exception(str(e) , "mainForPassword.py/updateInTable_func")


    # function to delete content from table in DB
    def deleteFromTable(self , key):
        try:
            # generating query for sqlite3 obj to execute
            stringToPass = "DELETE from " + self.tableNameForDB + " where PASSWORD_FOR = " + "'" + str(key) + "'" + ";"
            cursor = self.connectionObj.execute(stringToPass)
            self.connectionObj.commit()
            self.cLog.log("deleted in table successfully in main for password" , "i")
        except Exception as e:
            toLog = "cannot delete in table in main for password - query: " + stringToPass
            self.cLog.log(str(toLog) , "e")
            self.cLog.exception(str(e) , "mainForPassword.py/connectToDB")


    # function to display all the contents from the table in DB
    def displayAll(self):
        try:
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
            self.cLog.log("displayAll function runned successfully in main for password" , "i")
        except Exception as e:
            print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            self.cLog.log("error while displaying all", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/displayAll")


    # function to display certain items only based on search
    def displaySearch(self , searchItem):
        try:
            # generating query for sqlite3 obj to execute
            stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
            cursor = self.connectionObj.execute(stringToPass)
            tabulateList = []
            indexOfToCopy = []
            dictToHelpInCopying = {}
            countForTabulate = 1
            for row in cursor:
                if(row[0] == "!@#$%^&*("):
                    pass
                else:
                    if(self.isSubString(row[0] , searchItem)):
                        # generating list for tabulate module
                        tempList = []
                        tempList.append(str(countForTabulate))
                        tempList.append(str(row[0]))
                        tempList.append(self.decryptThing(str(row[1]) , self.password))
                        tabulateList.append(tempList)

                        # adding things to dict to help in copying - 
                        dictToHelpInCopying[str(countForTabulate)] = str(self.decryptThing(str(row[1]) , self.password))
                        countForTabulate += 1
            
            # showing the data
            os.system("cls")
            if(countForTabulate <= 1):
                print("\nno password found related to search term")
            
            else:
                print(tabulate(tabulateList, headers=['Index' , 'Site' , 'Password']))

                indexOfToCopy = input("\n\nEnter the index number of site to copy its password : ")
                try:
                    toCopy = dictToHelpInCopying[indexOfToCopy]
                    pyperclip.copy(str(toCopy))
                    pyperclip.paste()
                    print("\nPassword copied to the clipboard")
                except KeyError:
                    print("\nWrong index number entered")
                    self.cLog.log("Wrong index number entered in display search function in main for password" , "e")
                except Exception:
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                    self.cLog.log("error while displaying search after index number entered", "e")
                    self.cLog.exception(str(e) , "mainForPassword.py/displaySearch")

            self.cLog.log("display search function runned successfully in main for password" , "i")
        except Exception as e:
            self.cLog.log("error while displaying search", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/displaySearch")


    # function to set Password for encryption
    def setPass(self):
        try:
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
            self.cLog.log("setPass func runned successfully in main for password" , "i")
        except Exception as e:
            self.cLog.log("error while setting password in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/setPass")


    # function to authenticate - checking whether the password stored in the database is this or not
    # we do this by getting the password from the DB and decrypting it with the key = password enter , now if both match then we got the rigth user
    # returns bool value
    def authenticate(self):
        try:
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

            self.cLog.log("authenticate function runned successfully in main for password" , "i")

        except Exception as e:
            self.cLog.log("error while authenticating", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/authenticate")


    # function for changing the password
    # it is bit more complicated as we to encrypt all passwords again with the key = newPassword    
    def changePassword(self):
        try:
            while(1):

                # you can only change password if you are rigth user
                if(self.authenticate()):
                    self.deleteFromTable("!@#$%^&*(")
                    self.setPass()

                    # generating query for sqlite3 obj to execute
                    stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                    cursorForCounting = self.connectionObj.execute(stringToPass)
                    cursor = self.connectionObj.execute(stringToPass)
                    
                    # just to create "\n"
                    print()
                    countInCursor = 0

                    # for loading animation
                    for row in cursorForCounting:
                        countInCursor += 1
                    
                    countForCursor = 1

                    
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
                        
                        # for loading animation
                        print("\rUpdating database : {}/{}".format(countForCursor , countInCursor),end = "")
                        countForCursor += 1
                    
                    print()
                    print("\nPasswod change process completed")
                    break

                else:
                    print("Wrong password...")
                    os.system("pause")
            self.cLog.log("change password function runned successfully in main for password" , "i")
        except Exception as e:
            self.cLog.log("error while changing password in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/changePassword")


    # function for encrypting a thing with the key passed
    def encryptThing(self , thing , key):
        try:
            stringToReturn = onetimepad.encrypt(thing , key)
            self.cLog.log("encrypting thing func runned successfully in main for password" , "i")
            return str(stringToReturn)
        except Exception as e:
            print("\nSomething went wrong while encrypting, Please Try again, if error persist, run troubleShoot command")
            os.system("pause")
            self.cLog.log("error while encrypting thing in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/encryptThing")


    # function for decrypting a thing with the key passed
    def decryptThing(self , thing , key):
        try:
            stringToReturn = onetimepad.decrypt(thing , key)
            self.cLog.log("decrypting thing func runned successfully in main for password" , "i")
            return str(stringToReturn)
        except Exception as e:
            print("\nSomething went wrong while decrypting, Please Try again, if error persist, run troubleShoot command")
            os.system("pause")
            self.cLog.log("error while decrypting in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/decryptingThing")


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

                print("\nAdded successfully...")
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

                    print("\nPress enter to confirm delete , Notice - ones deleted you cannot get them back")
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
                        print("Old Password - " , self.decryptThing(row[1] , self.password))
                        toUpdateList.append(row[0])  

                indexInput = int(input("\nEnter Index for update\n"))

                for i,j in enumerate(toUpdateList):
                    if(i+1 == indexInput):
                        print("Enter the Updated Password : ")
                        updated = input()
                        updated = self.encryptThing(updated , self.password)
                        self.updateInTable(str(j) , str(updated))
                
                print("Value updated successfully")
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            # for seeing all the things in the DB
            elif("-sa" in commandList):
                self.displayAll()
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            # displaying things in the DB according to search query
            elif("-s" in commandList):
                os.system("cls")
                searchItem = input("Enter the website name to display Password : ")
                self.displaySearch(searchItem)
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            # for changing password
            elif("-c" in commandList):
                self.changePassword()
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            self.cLog.log("getDone func runned successfully in main for password" , "i")
            return False

        except Exception as e:
            self.cLog.log("error while performing the function getDone in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/getDone")
            print("Oops something went wrong :( ")

    # fuction for driving all the things
    def driverFunc(self , onlyAuthenticate = False):
        self.connectToDB()
        self.createTable()
        self.onlyAuthenticate = onlyAuthenticate

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

                # if the outside inside the password
                if(self.onlyAuthenticate == True):
                    return self.password
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
            try:
                commandList = list(stringOfCommandInput.split())
            except Exception as e:
                self.cLog.log("error while list in driver function", "e")
                self.cLog.exception(str(e) , "mainForPassword.py/driverFunc")
            if("exit" in commandList):
                print("\nYou are going to exit Password manager in Jarvis\n")
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
    # obj.driverFunc()
    # print(obj.__doc__)
