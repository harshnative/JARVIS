class GlobalData_mainForPasswordStorer:

    folderPathWindows = r"C:\programData\Jarvis"
    folderPathLinux = r"~/.config/Jarvis"
    folderPathWindows_simpleSlash = r"C:/programData/Jarvis"

    isOnWindows = False
    isOnLinux = False



import platform
import time
import subprocess as sp
import os
from typing import ValuesView
import stdiomask
from .eSqlite import SQLiteConnect
import getpass
import sys

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_mainForPasswordStorer.isOnLinux = True
elif(osUsing == "Windows"):
    GlobalData_mainForPasswordStorer.isOnWindows = True
else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    sys.exit()




# clear screen function 
def customClearScreen():
    if(GlobalData_mainForPasswordStorer.isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)


def hashPasswordInput(message):
    password = stdiomask.getpass(message)
    return password







class PasswordStorerClass:

    def __init__(self):

        # data base name
        self.dataBaseName = "jarvisPassDB.db"

        # setting the actaul path with name
        if(GlobalData_mainForPasswordStorer.isOnWindows):
            self.DataBasePath = GlobalData_mainForPasswordStorer.folderPathWindows_simpleSlash + "/" + self.dataBaseName
        elif(GlobalData_mainForPasswordStorer.isOnLinux):
            self.DataBasePath = GlobalData_mainForPasswordStorer.folderPathLinux + "/" + self.dataBaseName

        # table name for db
        self.tableNameForDB = "pass table"

        # self data base db
        self.dbObj = SQLiteConnect()


    # function to find whether a word is present in string or not
    def isSubString(self , string , subString):
        try:
            lengthOfSubString = len(subString)
            for i,j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        return True 
                    else:
                        pass
            return False
        except Exception as e:
            return False

    
    def driverFunc(self):

        self.dbObj.setDatabase(self.DataBasePath)

        customClearScreen()

        if(self.dbObj.checkForPasswordTable()):
            while(True):
                    print()
                    password = hashPasswordInput('enter password : ')
                    pin = 0
                    try:
                        pin = int(hashPasswordInput("enter pin : "))
                    except Exception:
                        print("\n\nPin should only consist of numbers...")
                        input("\npress enter to continue...")
                        continue

                    status = self.dbObj.setPassword(password , pin)

                    if(status):
                            self.dbObj.setSecurityStatus(True)
                            del password
                            del pin
                            break
                    else:
                            print("\n wrong password")


        else:
            
            while(True):
                customClearScreen()
                print()
                password = hashPasswordInput('enter password : ')
                pin = 0
                try:
                    pin = int(hashPasswordInput("enter pin : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                
                print()

                password1 = hashPasswordInput('enter password again : ')
                pin1 = 0
                try:
                    pin1 = int(hashPasswordInput("enter pin again : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                if((password != password1) and (pin != pin1)):
                        print("\nPassword and pin does not match")
                else:
                        status = self.dbObj.setPassword(password , pin)
                        if(status == None):
                                break
                        else:
                                print("\nsome error occur")

        contentList = [["data" , "TEXT" , 0] , ["pass" , "TEXT" , 0]]
        self.dbObj.createTable(self.tableNameForDB , contentList)

        self.dbObj.setSecurityStatus(True)

        while(1):
            customClearScreen()

            command = input("Enter command for password manager : ")

            if(command.strip() == "exit"):
                break

            if(command.strip() == "exit all"):
                sys.exit()
            

            self.executeCommand(command)



    def displayAll(self):
        self.dbObj.printData()

    
    def executeCommand(self , command):

        command = command.strip()

        if(command == "-a"):
            customClearScreen()
            data = input("Enter the website name for reference : ")
            password = input("Enter the password : ")

            if((data == "") and (password == "")):
                return

            valuesList = [data , password]
            self.dbObj.insertIntoTable(valuesList=valuesList)

            input("\nAdded successfully ...")

        elif(command == "-sa"):
            customClearScreen()
            self.displayAll()
            input()

        elif(command == "-u"):
            customClearScreen()
            self.displayAll()

            key = 0

            try:
                key = int(input("\nEnter the index to update : "))
            except Exception:
                print("\n please enter valid index no")
                return

            customClearScreen()

            try:
                self.dbObj.printDataOfKey(key)
            except Exception:
                print("\n please enter valid index no")
                return

            newPass = input("\nEnter new password for above website : ")

            self.dbObj.updateRow("pass" , newPass , key)

            print("\npassword updated successfully")

            input("\npress enter to continue")

        elif(command == "-d"):

            customClearScreen()
            self.displayAll()

            key = 0

            try:
                key = int(input("\nEnter the index to delete : "))
            except Exception:
                print("\n please enter valid index no")
                return

            customClearScreen()

            try:
                self.dbObj.printDataOfKey(key)
            except Exception:
                print("\n please enter valid index no")
                return

            temp = input("\nabove website is going to be deleted , enter 1 to continue or anything else to skip : ")

            if(temp == "1"):
                self.dbObj.deleteRow(key , updateId=True)

                print("\ndeleted successfully")

                input("\npress enter to continue")

            else:

                print("\noperation cancelled")

                input("\npress enter to continue")


        elif(command == "-s"):
            customClearScreen()

            searchTerm = input("Enter a search keyword for search the website : ")

            returnedData = self.dbObj.returnData()

            printList = []

            for i in returnedData[1:]:
                
                if(self.isSubString(i[1] , searchTerm)):
                    printList.append(i)

            print("\n")

            self.dbObj.tabulatePrinter(printList , returnedData[0])

            input()

        elif(command == "-c"):

            oldPass = ""
            oldPin = 123456
            
            while(True):
                customClearScreen()
                oldPass = hashPasswordInput("Enter old password : ")
                try:
                    oldPin = int(hashPasswordInput("Enter old pin : "))
                except Exception:
                    print("\nenter valid pin , press enter to continue")
                    input()
                    return

                status = self.dbObj.setPassword(oldPass , oldPin)

                if(status):
                        self.dbObj.setSecurityStatus(True)
                        break
                else:
                        print("\n wrong password")
                        input()

            password = ""
            pin = 123456

            while(True):

                customClearScreen()
                print()
                password = hashPasswordInput('enter new password : ')
                pin = 0
                try:
                    pin = int(hashPasswordInput("enter new pin : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                
                print()

                password1 = hashPasswordInput('enter password again : ')
                pin1 = 0
                try:
                    pin1 = int(hashPasswordInput("enter pin again : "))
                except Exception:
                    print("\n\nPin should only consist of numbers...")
                    input("\npress enter to continue...")
                    continue

                if((password != password1) and (pin != pin1)):
                        print("\nPassword and pin does not match")
                else:
                        break

            returnedData = self.dbObj.returnData()
            
            try:
                self.dbObj.changePassword(oldPassword=oldPass , newPassword=password , oldPin=oldPin , newPin=pin)
                print("\npassword changed successfully")
                input("\npress enter to continue ...")
                return
            except Exception as e:
                print("\n error while changing password with exception =  {} , restoring current password ...".format(e))
                self.dbObj.delEntireTable()
                contentList = [["data" , "TEXT" , 0] , ["pass" , "TEXT" , 0]]
                self.dbObj.createTable(self.tableNameForDB , contentList)

                self.dbObj.setSecurityStatus(True)

                for i in returnedData[1:]:
                    self.dbObj.insertIntoTable(valuesList=i[1:])
                
                input("\n press enter to continue")
                return 

        else:
            customClearScreen()
            print("wrong command , try -a , -s , -sa , -c , -d , -u , exit , exit all instead..")
            input("\n\npress enter to continue...")



        



            


