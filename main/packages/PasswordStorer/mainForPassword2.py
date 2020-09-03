import sqlite3
from tabulate import tabulate
import os
import onetimepad
from packages.loggerPackage.loggerFile import *
import stdiomask
import pyperclip
from cryptography.fernet import Fernet


folderPathWindows = r"C:\programData\Jarvis"
folderPathLinux = r"~/.config/Jarvis"
folderPathWindows_simpleSlash = r"C:/programData/Jarvis"



import subprocess as sp

isOnWindows = False
isOnLinux = False

# Checking weather the user is on windows or not
try:
    temp = os.environ
    tempUserName = temp["USERNAME"]
    isOnWindows = True
except Exception:
    isOnLinux = True


# clear screen function 
def customClearScreen():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)


def hashPasswordInput(message):
    password = stdiomask.getpass(message)
    return password



from easyTypeWriter import typeWriter

# creating objects of typewriter module
typeWriterObj = typeWriter.EasyInput()

# setting paths required for typeWriterObj
typeWriterObj.setEnterAudioPath("sounds/ding3.wav")
typeWriterObj.setKeyboardAudioPath("sounds/keysound30.wav")



class PasswordStorerClass2:

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
        self._key = None
        self.oldPassword = None
        self.onlyAuthenticate = None
        if(isOnWindows):
            self.toDataBasePath = folderPathWindows_simpleSlash
        elif(isOnLinux):
            self.toDataBasePath = folderPathLinux

    
    # typeWriter input function
    def customInput(self , messagePrompt = ""):
        toMakeTypingSound = self.makeKeyboardSound
            
        x = typeWriterObj.takeInput(toMakeTypingSound , messagePrompt)
        return str(x)
        
        
    

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
                toCompare = self.decryptThing(row[0] , self.password)

                if(row[0] == "!@#$%^&*("):
                    pass
                
                elif(toCompare == "self.password"):
                    pass

                else:
                    tempDecrypt = self.decryptThing2(row[0])
                    # getting list for tablute module to show data
                    tempList = []
                    tempList.append(str(tempDecrypt))
                    tempList.append(self.decryptThing2(str(row[1])))
                    tabulateList.append(tempList)
            
            # showing the data 
            customClearScreen()
            print(tabulate(tabulateList, headers=['Site', 'Password']))
            self.cLog.log("displayAll function runned successfully in main for password" , "i")
        except Exception as e:
            if(self.cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
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

                toCompare = self.decryptThing(row[0] , self.password)

                if(row[0] == "!@#$%^&*("):
                    pass
                
                elif(toCompare == "helloIAmJarvis&IAmHereToAssistYou"):
                    pass

                else:
                    tempDecrypt = self.decryptThing2(row[0])
                    if(self.isSubString(tempDecrypt , searchItem)):
                        # generating list for tabulate module
                        tempList = []
                        tempList.append(str(countForTabulate))
                        tempList.append(str(tempDecrypt))
                        tempList.append(self.decryptThing2(str(row[1])))
                        tabulateList.append(tempList)

                        # adding things to dict to help in copying - 
                        dictToHelpInCopying[str(countForTabulate)] = str(self.decryptThing2(str(row[1])))
                        countForTabulate += 1
            
            # showing the data
            customClearScreen()
            if(countForTabulate <= 1):
                print("\nno password found related to search term")
            
            else:
                print(tabulate(tabulateList, headers=['Index' , 'Site' , 'Password']))
                print("\n")
                indexOfToCopy = self.customInput("Enter the index number of site to copy its password : ")
                try:
                    toCopy = dictToHelpInCopying[indexOfToCopy]
                    pyperclip.copy(str(toCopy))
                    pyperclip.paste()
                    print("\nPassword copied to the clipboard")
                except KeyError:
                    print("\nWrong index number entered")
                    self.cLog.log("Wrong index number entered in display search function in main for password" , "e")
                except Exception as e:
                    if(self.cLog.troubleShoot == False):
                        print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
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
                        print("\nalso password length must be more than 8 digits and should be of even length")
                        print("\neasy password's are easy to crack and unsecure")
                        print("\n")
                        self.customInput("Press enter to continue : ")
                        continue

                    

                    key = Fernet.generate_key()
                    newKey = key.decode("utf-8")

                    toAdd0 = self.encryptThing("helloIAmJarvis&IAmHereToAssistYou", passwordInput2)
                    toAdd1 = self.encryptThing(newKey , passwordInput2)


                    # adding password to data base and class variable
                    self.addToTable(toAdd0 , toAdd1)
                    self.addToTable("!@#$%^&*(" , "!@#$%^&*(")
                    self.password = passwordInput2
                    print("congo , new Password setted successfully")
                    break

                # if the password does not match , continue the loop
                else:
                    print("\nPassword did not match\n")
                    self.customInput("press enter to continue...")
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

            # generating query for sqlite3 obj to execute
            stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
            cursor = self.connectionObj.execute(stringToPass)
            for row in cursor:
                toCompare = self.decryptThing(row[0] , passwordInput)
                if(toCompare == "helloIAmJarvis&IAmHereToAssistYou"):
                    self.password = passwordInput
                    key = self.decryptThing(row[1] , passwordInput)
                    self._key = bytes(key , "utf-8")
                    self.cLog.log("authenticate function runned successfully in main for password" , "i")
                    return True
            
            
            self.cLog.log("authenticate function runned successfully in main for password" , "i")
            return False


        except Exception as e:
            self.cLog.log("error while authenticating", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/authenticate")


    # function for changing the password
    # it is bit more complicated as we to encrypt all passwords again with the key = newPassword    
    def changePassword(self , transfer = False):
        try:
            while(1):
                

                # you can only change password if you are rigth user
                if(self.authenticate()):

                    # generating query for sqlite3 obj to execute
                    stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                    cursor = self.connectionObj.execute(stringToPass)

                    for row in cursor:
                        toCompare = self.decryptThing(row[0] , self.password)
                        if(toCompare == "helloIAmJarvis&IAmHereToAssistYou"):
                            self.deleteFromTable(toCompare)
                        
                    self.setPass()
                    
                    tempList = []
                    
                    print("\nGetting old database")
                    for row in cursor:
                        # do not want to change master password as it as already been updated
                        toCompare = self.decryptThing(row[0] , self.password)
                        if(toCompare == "helloIAmJarvis&IAmHereToAssistYou"):
                            pass
                        else:
                            # getting keys
                            oldKey = row[0]
                            # decrypting it
                            oldKeyD = self.decryptThing2(oldKey)
                            # encrypting it
                            newKey = self.encryptThing2(oldKeyD)

                            # getting passwords
                            oldPass = row[1]
                            # decryting it 
                            oldPassD = self.decryptThing2(oldPass)
                            # encrypting it again with new password
                            newPass = self.encryptThing2(oldPassD)
                       
                            
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
                    self.customInput("press enter to continue...")
            self.cLog.log("change password function runned successfully in main for password" , "i")
        except Exception as e:
            self.cLog.log("error while changing password in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/changePassword")

    
    def changePassword2(self , tranfer = False):
        try:
            while(1):
                

                # you can only change password if you are rigth user
                if(tranfer):

                    # generating query for sqlite3 obj to execute
                    stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                    cursor = self.connectionObj.execute(stringToPass)

                    for row in cursor:
                        if(row[0] == "!@#$%^&*("):
                            self.deleteFromTable("!@#$%^&*(")
                    
                    self.setPass()
                    
                    tempList = []
                    
                    print("\nGetting old database")
                    for row in cursor:
                        # do not want to change master password as it as already been updated
                        toCompare = self.decryptThing(row[0] , self.password)
                        if(toCompare == "helloIAmJarvis&IAmHereToAssistYou"):
                            pass
                        else:
                            # getting keys
                            oldKey = row[0]
                            # decrypting it
                            oldKeyD = self.decryptThing(oldKey , self.oldPassword)
                            # encrypting it
                            newKey = self.encryptThing2(oldKeyD)

                            # getting passwords
                            oldPass = row[1]
                            # decryting it 
                            oldPassD = self.decryptThing(oldPass, self.oldPassword)
                            # encrypting it again with new password
                            newPass = self.encryptThing2(oldPassD)
                       
                            
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
                    self.customInput("press enter to continue...")
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
            self.customInput("press enter to continue...")
            self.cLog.log("error while encrypting thing in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/encryptThing")


    # function for decrypting a thing with the key passed
    def decryptThing(self , thing , key):
        try:
            stringToReturn = onetimepad.decrypt(thing , key)
            self.cLog.log("decrypting thing func runned successfully in main for password" , "i")
            return str(stringToReturn)
        except Exception as e:
            if(self.cLog.troubleShoot == False):
                print("\nSomething went wrong while decrypting, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
            self.customInput("press enter to continue...")
            self.cLog.log("error while decrypting in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/decryptingThing")


    # function for encrypting a thing with the key passed
    def encryptThing2(self , thing):
        try:
            cipher_suite = Fernet(self._key)
            stringToPass = bytes(thing , "utf-8")
            encoded_text = cipher_suite.encrypt(stringToPass)
            self.cLog.log("encrypting thing func runned successfully in main for password" , "i")
            return encoded_text.decode("utf-8")
        except Exception as e:
            print("\nSomething went wrong while encrypting, Please Try again, if error persist, run troubleShoot command")
            self.customInput("press enter to continue...")
            self.cLog.log("error while encrypting thing in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/encryptThing2")


    # function for decrypting a thing with the key passed
    def decryptThing2(self , thing):
        try:
            cipher_suite = Fernet(self._key)
            stringToPass = bytes(thing , "utf-8")
            decoded_text = cipher_suite.decrypt(stringToPass)
            stringToReturn = decoded_text.decode("utf-8")
            self.cLog.log("decrypting thing func runned successfully in main for password" , "i")
            return str(stringToReturn)
        except Exception as e:
            if(self.cLog.troubleShoot == False):
                print("\nSomething went wrong while decrypting, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
            self.customInput("press enter to continue...")
            self.cLog.log("error while decrypting in main for password", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/decryptingThing2")


    # function for Getting things done
    def getDone(self , commandList):

        try:
            # for adding things to DB
            if("-a" in commandList):
                customClearScreen()
                x = self.customInput("Enter Website name for future referencing : ") 
                y = self.customInput("Enter the Password : ")
                
                x = self.encryptThing2(x)
                y = self.encryptThing2(y)

                self.addToTable(str(x) , str(y))

                print("\nAdded successfully...")
                return True

            # for deleting things
            elif("-d" in commandList):
                customClearScreen()
                webDelete = self.customInput("Enter the Website name for deletion : ")
                # generating query for sqlite3 obj to execute
                stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
                cursor = self.connectionObj.execute(stringToPass)

                listToDelete = []
                indexCount = 1
                count = 0

                customClearScreen()
                for row in cursor:

                    toCompare = self.decryptThing2(row[0])

                    if(row[0] == "!@#$%^&*("):
                        pass

                    elif(toCompare == self.password):
                        pass

                    else:
                        tempDecrypt = self.decryptThing2(row[0])
                        if(self.isSubString(tempDecrypt , webDelete)):
                            print(indexCount , end = " : ")
                            print("Site - ", tempDecrypt)
                            listToDelete.append(row[0])
                            indexCount += 1
                            count += 1
                    
                if(count > 0):
                    print("\nEnter Index for deletion (space seperated for multiple) , Enter 0 to delete all : ")
                    indexList = [int(x) for x in self.customInput().split()]

                    print("\nPress enter to confirm delete , Notice - ones deleted you cannot get them back")
                    self.customInput()

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
                
                toUpdate = self.customInput("Enter the website name to update : ")
                toUpdateList = []

                indexCount = 1
                
                for row in cursor:

                    toCompare = self.decryptThing2(row[0])

                    if(row[0] == "!@#$%^&*("):
                        pass
                    
                    elif(toCompare == self.password):
                        pass
     
                    else:
                        tempDecrypt = self.decryptThing2(row[0])
                        if(self.isSubString(tempDecrypt , toUpdate)):
                            print(indexCount , end = " : ")
                            print("Site - ", tempDecrypt , end = "    ")
                            print("Old Password - " , self.decryptThing2(row[1]))
                            toUpdateList.append(row[0])  
                print()
                indexInput = int(self.customInput("Enter Index for update : "))
                
                ifUpdatedSomething = False

                for i,j in enumerate(toUpdateList):
                    if(i+1 == indexInput):
                        print()
                        updated = self.customInput("Enter the Updated Password : ")
                        updated = self.encryptThing2(updated)
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
                searchItem = self.customInput("Enter the website name to display Password : ")
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

    def authenticatePrev(self):
        try:
            customClearScreen()
            passwordInput = str(hashPasswordInput("Enter Master Password : "))

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
                        self.cLog.log("authenticate function runned successfully in main for password" , "i")
                        return True
            
            
            self.cLog.log("authenticate function runned successfully in main for password" , "i")
            return False


        except Exception as e:
            self.cLog.log("error while authenticating", "e")
            self.cLog.exception(str(e) , "mainForPassword.py/authenticate")

    # fuction for driving all the things
    def driverFunc(self , onlyAuthenticate = False):
        self.connectToDB()
        self.createTable()
        self.onlyAuthenticate = onlyAuthenticate

        # generating query for sqlite3 obj to execute
        stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
        cursor = self.connectionObj.execute(stringToPass)
        count = 0
        previous = 1

        for row in cursor:
            if(row[0] == "!@#$%^&*("):
                count = 1

        for row in cursor:
            if((row[0] == "!@#$%^&*(") and (row[1] == "!@#$%^&*(")):
                previous = 0

        
        # if it is first time then required to set a password
        if(count == 0):
            self.setPass()
            print("\n\n")
            self.customInput("press enter to continue...")

        # checking whether the user is right or not
        while(1):
            if(previous == 0):
                if(self.authenticatePrev()):
                    # if the outside inside the password
                    if(self.onlyAuthenticate == True):
                        return self.password
                    break
                else:
                    print("\nwrong password....\n")
                    self.customInput("press enter to continue...")
            
            else:
                if(self.authenticate()):

                    # if the outside inside the password
                    if(self.onlyAuthenticate == True):
                        return self.password
                    break
                else:
                    print("\nwrong password....\n")
                    self.customInput("press enter to continue...")
        
        customClearScreen()

        # starting module
        while(1):
            # generating query for sqlite3 obj to execute
            stringToPass = "SELECT PASSWORD_FOR , PASSWORD_VALUE from " + self.tableNameForDB
            cursor = self.connectionObj.execute(stringToPass)
            for row in cursor:
                if((row[0] == "!@#$%^&*(") and (row[1] != "!@#$%^&*(")):
                    customClearScreen()
                    print("jarvis encryption as been updated , so you have to set a new password ...")
                    input("\n\npress enter to continue ...")
                    self.changePassword2(True)

            
            # taking command
            stringOfCommandInput = self.customInput("Enter Command For Password Manager in JARVIS : ")
            
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
            self.customInput("press enter to continue...")
            customClearScreen()


# just for testing purpose
if __name__ == "__main__":
    obj = PasswordStorerClass()
    # obj.driverFunc()
    # print(obj.__doc__)
