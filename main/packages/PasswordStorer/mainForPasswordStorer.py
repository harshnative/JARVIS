from enum import Flag
import sqlite3
from tabulate import tabulate
import os
import onetimepad
from packages.loggerPackage.loggerFile import *
import stdiomask
import pyperclip


folderPathWindows = r"C:\programData\Jarvis"
folderPathLinux = r"~/.config/Jarvis"
folderPathWindows_simpleSlash = r"C:/programData/Jarvis"



import subprocess as sp

isOnWindows = False
isOnLinux = False

import platform
import time

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Linux"):
    isOnLinux = True
elif(osUsing == "Windows"):
    isOnWindows = True
else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    exit()


# clear screen function 
def customClearScreen():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)


def hashPasswordInput(message):
    password = stdiomask.getpass(message)
    return password




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
    def __init__(self , troubleShootValuePass , makeKeyboardSound):
        self.makeKeyboardSound = makeKeyboardSound
        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)
        self.tableNameForDB = "PASSWORDSTORER"
        self.dataBaseFileName = "Jarvis.db"
        self.connectionObj = None
        self.password = None
        self.oldPassword = None
        self.onlyAuthenticate = None
        if(isOnWindows):
            self.toDataBasePath = folderPathWindows_simpleSlash
        elif(isOnLinux):
            self.toDataBasePath = folderPathLinux


        
        
    

    def checkPass(self , string):
        lowerCase = ['a','s','d','f','g','h','j','k','l','z','x',
                    'c','v','b','n','m','q','w','e','r','t','y','u'
                    ,'i','o','p']
        upperCase = []
        for i in lowerCase:
            upperCase.append(i.upper())
        spChar = ['~','!','@','$','%','^','&','*','(',')','_','-','=',
                '`','/','+','/','<','>','[',']','{','}','.',':',';',
                '|','#']
        nums = ['1','2','3','4','5','6','7','8','9','0']
        count = [0,0,0,0] #lowercase,uppercase,specialtype,numbers
        for p in string:
            if ((p in lowerCase) and (count[0]==0) and len(string)>=8 and (len(string)%2 == 0)):
                count[0]=1
            if ((p in upperCase) and (count[1]==0) and len(string)>=8 and (len(string)%2 == 0)):
                count[1]=1
            if ((p in spChar) and (count[2]==0) and len(string)>=8 and (len(string)%2 == 0)):
                count[2]=1
            if ((p in nums) and (count[3]==0)  and len(string)>=8 and (len(string)%2 == 0)):
                count[3]=1
                
        type_num = 0
        for i in count:
            type_num+=i
        return type_num

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
            self.connectionObj = sqlite3.connect(self.toDataBasePath + "/" + self.dataBaseFileName)
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
                    tempDecrypt = self.decryptThing(row[0] , self.password)
                    # getting list for tablute module to show data
                    tempList = []
                    tempList.append(str(tempDecrypt))
                    tempList.append(self.decryptThing(str(row[1]) , self.password))
                    tabulateList.append(tempList)
            
            # showing the data 
            customClearScreen()
            print(tabulate(tabulateList, headers=['Site', 'Password']))
            self.cLog.log("displayAll function runned successfully in main for password" , "i")
        except Exception as e:
            # if(self.cLog.troubleShoot == False):
            #     print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            # else:
            #     print("\nerror has been logged - continue...")
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
                    tempDecrypt = self.decryptThing(row[0] , self.password)
                    if(self.isSubString(tempDecrypt , searchItem)):
                        # generating list for tabulate module
                        tempList = []
                        tempList.append(str(countForTabulate))
                        tempList.append(str(tempDecrypt))
                        tempList.append(self.decryptThing(str(row[1]) , self.password))
                        tabulateList.append(tempList)

                        # adding things to dict to help in copying - 
                        dictToHelpInCopying[str(countForTabulate)] = str(self.decryptThing(str(row[1]) , self.password))
                        countForTabulate += 1
            
            # showing the data
            customClearScreen()
            if(countForTabulate <= 1):
                print("\nno password found related to search term")
            
            else:
                print(tabulate(tabulateList, headers=['Index' , 'Site' , 'Password']))
                print("\n")
                indexOfToCopy = input("Enter the index number of site to copy its password : ")
                try:
                    toCopy = dictToHelpInCopying[indexOfToCopy]
                    pyperclip.copy(str(toCopy))
                    pyperclip.paste()
                    print("\nPassword copied to the clipboard")
                except KeyError:
                    print("\nWrong index number entered")
                    self.cLog.log("Wrong index number entered in display search function in main for password" , "e")
                except Exception as e:
                    # if(self.cLog.troubleShoot == False):
                    #     print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                    # else:
                    #     print("\nerror has been logged - continue...")
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
                customClearScreen()
                passwordInput1 = str(hashPasswordInput("Enter  New  Master Password : "))
                passwordInput2 = str(hashPasswordInput("Enter Master Password again : "))

                # checking if the password are same or not to avoid miss entering of password
                if(passwordInput1 == passwordInput2):
                    
                    if(self.checkPass(passwordInput1) < 2):
                        print("please use combination of characters, numbers and special characters as your password")
                        print("\nalso password length must be more than 8 digits")
                        print("\neasy password's are easy to crack and unsecure")
                        print("\n")
                        input("Press enter to continue : ")
                        continue

                    passwordInput1 = self.encryptThing(passwordInput1 , passwordInput2)

                    # adding password to data base and class variable
                    self.addToTable("!@#$%^&*(" , passwordInput1)
                    self.password = passwordInput2
                    print("congo , new Password setted successfully")
                    break

                # if the password does not match , continue the loop
                else:
                    print("\nPassword did not match\n")
                    input("press enter to continue...")
            self.cLog.log("setPass func runned successfully in main for password" , "i")
        except Exception as e:
            self.cLog.log("error while setting password in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/setPass")


    # function to authenticate - checking whether the password stored in the database is this or not
    # we do this by getting the password from the DB and decrypting it with the key = password enter , now if both match then we got the rigth user
    # returns bool value
    def authenticate(self):
        try:
            customClearScreen()
            passwordInput = str(hashPasswordInput("Enter Master Password : "))

            if(passwordInput == ""):
                return False

            # generating query for sqlite3 obj to execute
            stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
            cursor = self.connectionObj.execute(stringToPass)
            for row in cursor:
                if(row[0] == "!@#$%^&*("):
                    passwordFromDataBase = row[1]
                    passwordFromDataBase = self.decryptThing(passwordFromDataBase , passwordInput)
                    # print(passwordFromDataBase , passwordInput)
                    if(passwordFromDataBase == passwordInput):
                      
                        self.password = passwordInput
                        self.oldPassword = passwordInput
                        self.cLog.log("authenticate function runned successfully in main for password" , "i")
                        return True
            
            else:
                self.cLog.log("authenticate function runned successfully in main for password" , "i")
                return False


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
                    
                    countForCursor = 1          
                    tempList = []
                    
                    print("\nGetting old database")
                    for row in cursor:
                        # do not want to change master password as it as already been updated
                        if(row[0] == "!@#$%^&*("):
                            pass
                        else:
                            # getting keys
                            oldKey = row[0]
                            # decrypting it
                            oldKeyD = self.decryptThing(oldKey , self.oldPassword)
                            # encrypting it
                            newKey = self.encryptThing(oldKeyD , self.password)

                            # getting passwords
                            oldPass = row[1]
                            # decryting it 
                            oldPassD = self.decryptThing(oldPass, self.oldPassword)
                            # encrypting it again with new password
                            newPass = self.encryptThing(oldPassD, self.password)
                       
                            
                            # adding to table for latter updation
                            innerTempList = []
                            innerTempList.append(newKey)
                            innerTempList.append(newPass)
                            tempList.append(innerTempList)

                            # deleting existing values form data base
                            self.deleteFromTable(oldKey)
                    
                    # adding new values to the data base
                    print("\nImplementing new database")
                    for i in tempList:
                        self.addToTable(i[0] , i[1])
                    
                    print("\n\nPassword change process completed")
                    break

                else:
                    print("Wrong password...")
                    input("press enter to continue...")
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
            input("press enter to continue...")
            self.cLog.log("error while encrypting thing in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/encryptThing")


    # function for decrypting a thing with the key passed
    def decryptThing(self , thing , key):
        try:
            stringToReturn = onetimepad.decrypt(thing , key)
            self.cLog.log("decrypting thing func runned successfully in main for password" , "i")
            return str(stringToReturn)
        except Exception as e:
            # if(self.cLog.troubleShoot == False):
            #     print("\nSomething went wrong while decrypting, Please Try again, if error persist, run troubleShoot command")
            # else:
            #     print("\nerror has been logged - continue...")
            # input("press enter to continue...")
            self.cLog.log("error while decrypting in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/decryptingThing")


    # function for Getting things done
    def getDone(self , commandList):

        try:
            # for adding things to DB
            if("-a" in commandList):
                customClearScreen()
                x = input("Enter Website name for future referencing : ") 
                y = input("Enter the Password : ")
                
                x = self.encryptThing(x , self.password)
                y = self.encryptThing(y , self.password)

                self.addToTable(str(x) , str(y))

                print("\nAdded successfully...")
                return True

            # for deleting things
            elif("-d" in commandList):
                customClearScreen()
                webDelete = input("Enter the Website name for deletion : ")
                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)

                listToDelete = []
                indexCount = 1
                count = 0

                customClearScreen()
                for row in cursor:
                    if(row[0] == "!@#$%^&*("):
                        pass
                    else:
                        tempDecrypt = self.decryptThing(row[0] , self.password)
                        if(self.isSubString(tempDecrypt , webDelete)):
                            print(indexCount , end = " : ")
                            print("Site - ", tempDecrypt)
                            listToDelete.append(row[0])
                            indexCount += 1
                            count += 1
                    
                if(count > 0):
                    print("\nEnter Index for deletion (space seperated for multiple) , Enter 0 to delete all : ")
                    indexList = [int(x) for x in input().split()]

                    print("\nPress enter to confirm delete , Notice - ones deleted you cannot get them back")
                    input()

                    somethingDeleted = False

                    for i,j in enumerate(listToDelete):
                        if(i+1 in indexList):
                            self.deleteFromTable(str(j))
                            somethingDeleted = True
                        elif(0 in indexList):
                            self.deleteFromTable(str(j))
                            somethingDeleted = True
                        
                    if(somethingDeleted == True):
                        print("\nDeleted successfully :)")
                    else:
                        print("\nNothing deleted...")

                else:
                    customClearScreen()
                    print("No website found........")
                
                return True
        
            # for updating things
            elif("-u" in commandList):
                customClearScreen()
                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)
                
                toUpdate = input("Enter the website name to update : ")
                toUpdateList = []

                indexCount = 1
                
                for row in cursor:
                    if(row[0] == "!@#$%^&*("):
                        pass
                    else:
                        tempDecrypt = self.decryptThing(row[0] , self.password)
                        if(self.isSubString(tempDecrypt , toUpdate)):
                            print(indexCount , end = " : ")
                            print("Site - ", tempDecrypt , end = "    ")
                            print("Old Password - " , self.decryptThing(row[1] , self.password))
                            toUpdateList.append(row[0])  
                print()
                indexInput = int(input("Enter Index for update : "))
                
                ifUpdatedSomething = False

                for i,j in enumerate(toUpdateList):
                    if(i+1 == indexInput):
                        print()
                        updated = input("Enter the Updated Password : ")
                        updated = self.encryptThing(updated , self.password)
                        self.updateInTable(str(j) , str(updated))
                        ifUpdatedSomething = True
                
                if(ifUpdatedSomething == True):
                    print("\nValue updated successfully")
                else:
                    print("\nUpdated nothing...")
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            # for seeing all the things in the DB
            elif("-sa" in commandList):
                self.displayAll()
                self.cLog.log("getDone func runned successfully in main for password" , "i")
                return True

            # displaying things in the DB according to search query
            elif("-s" in commandList):
                customClearScreen()
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
            input("press enter to continue...")

        # checking whether the user is right or not
        while(1):
            if(self.authenticate()):

                # if the outside inside the password
                if(self.onlyAuthenticate == True):
                    return self.password
                break
            else:
                print("\nwrong password....\n")
                input("press enter to continue...")
        
        customClearScreen()

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
                    customClearScreen()
                    print("Sorry , cannot recognise the command :(\n")
            
            print("\n\n")
            input("press enter to continue...")
            customClearScreen()


# just for testing purpose
if __name__ == "__main__":
    obj = PasswordStorerClass()
    # obj.driverFunc()
    # print(obj.__doc__)
