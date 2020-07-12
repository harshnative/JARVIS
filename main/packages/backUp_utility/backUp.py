import os
import shutil
import distutils.dir_util
import datetime
from packages.loggerPackage.loggerFile import *
import getpass as getUserName

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



class BackUp():
    """ startBackUp is the main function of this , only this function is usefull as it can drive other function of this class itself
        
            This function excepts four arguments 

            1. commandList - list of command that are passed by the user to perform the actions
                
                commands that can be passed - 
                    -a                  ->  for generating the backup of all the things of all the users 
                    -a and -c           ->  for generating the backup of all the things of the current user
                    -a and -e           ->  for generating the backup of all the essential things of all the users , essential items include things within - desktop , videos , pictures , music , downloads
                    -a and -e and -c    ->  for generating the backup of all the essential things of the current user only
                    -d                  ->  this can be clubbed with above and is used to backup the folders of which the paths are send as list to additionalDirectoryList

            2. pass the list containing the exact paths of the folders of which you want to generate the backup of in case of -d command 

            3. pass the path for the backUp folder location 

            4. to generate log file or not - default Value is True 
            
            at the end of the process a log file will be generated at the desktop"""


    # constructor function
    def __init__(self , troubleShootValuePass):
        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)
        self.loggerObj = loggerObj
        self.userName = None
        self.pathToBackup = None
        self.exceptionList = []
        self.listOfDirectories = []


    # function to set the path of backup location 
    def setPathToBackup(self , pathPassed):
        self.pathToBackup = str(pathPassed)


    # function to get the userName of the current user
    def getUserName(self):
        try:
            self.userName = getUserName.getuser()
        except Exception as e:
            customClearScreen()
            self.cLog.log("Jarvis could not get the user name form os" , "e")
            self.cLog.exception(str(e) , "In backUp.py/BackUp_Class-getUserName_func")
            
            if(self.cLog.troubleShoot == False):
                print("ERROR : jarvis could not get userName")
                print("\nTry reinstalling the program with admistrative permissions\n")
                print("\n if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
            input("press enter to continue...")


    # function for copying the all stuff inside the c:/user
    def forCommand_A(self):
        self.exceptionList.clear()
        path = "C:/Users"
        try:
            shutil.copytree(path , self.pathToBackup , dirs_exist_ok=True)
        except Exception as e:
            self.exceptionList.append(str(e))
        self.cLog.log("for Command_A function runned successfully" ,"i")


    # function for copying the essentials of all the users inside "C:/"
    def forCommand_A_E(self):
        """ desktop , downloads , pictures , videos , music , documents will be copied , 
        if the file is already their in backup then they will be replaced by the comming new files"""

        # stuff to use
        pathList = []
        pathToCopy = []
        self.exceptionList.clear()
        folderList = ["Desktop" , "Downloads" , "Pictures" , "Videos" , "Music" , "Documents"]
        
        # getting the list of users or directory names under user 
        allUserList = [dI for dI in os.listdir("C:/Users") if os.path.isdir(os.path.join("C:/Users",dI))]

        # adding the user names to c:/users/ to generate the paths
        for i in allUserList:
            stringToAppend = "C:/Users"
            stringToAppend = stringToAppend + "/" + str(i) + "/"
            pathList.append(stringToAppend)

        # adding the folderNames to be copied to the previously generated paths
        for i in pathList:
            for j in folderList:
                stringToAppend = str(i) + str(j)
                if(os.path.isdir(stringToAppend)):
                    pathToCopy.append(stringToAppend)

        # stuff to use
        lengthToCopy = len(pathToCopy)
        count = 1

        # actual copying starts here
        for i in pathToCopy:
            print(f"on {count} out of {lengthToCopy}")
            # making sure that the path to backup exsist
            try:
                os.makedirs(self.pathToBackup + "/" + i[9:], exist_ok = True)
            except OSError as e:
                self.cLog.log("folder might be present for backUp_class-forCommand_A_E_func" ,"e")
                self.cLog.exception(str(e) , "In backUp.py/backUp_class-forCommand_A_E_func")
            
            # making the copy
            try:
                shutil.copytree(i , self.pathToBackup + "/" + i[9:], dirs_exist_ok=True)
            except Exception as e:
                self.exceptionList.append(str(e))     
            count += 1
        self.cLog.log("for Command_A_E function runned successfully" ,"i")


    # function for write the error data to a log file
    def logFileGenerator(self):
        """log file is located at desktop"""

        path = "C:/Users/" + self.userName + "/Desktop/logFileJarvis.txt"

        try:
            with open(path , "a+") as fil:

                #writing some info to log file
                currentDT = datetime.datetime.now()
                fil.write("\n\n")
                toWrite = "Process Time - " + str(currentDT)
                fil.write(toWrite)
                fil.write("\n")

                #writing some actaul errors 
                for i in self.exceptionList:
                    fil.write("Error - ")
                    fil.write(i)
                    fil.write("\n")

            self.cLog.log("for logFileGenerator function runned successfully" ,"i")
            
        except Exception as e:
            self.cLog.log("could not generate log file" , "e")
            self.cLog.exception(str(e) , "In backUp.py/backUp_class-logFileGenerator_Func")
            print("could not generate the log file")
            if(self.cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
        
                   

    #function for copying all the current user
    def forCommand_A_C(self):
        """copies all the things inside the current user folder"""

        # setting up the source path for copy function
        path = "C:/Users/" + self.userName

        # setting up the destination path for the copy function
        try:
            os.makedirs(self.pathToBackup + "/" + self.userName)
        except OSError as e:
            self.cLog.log("folder might be present for backUp_class-forCommand_A_C_func" , "e")
            self.cLog.exception(str(e) , "In backUp.py/backUp_class-forCommand_A_C_func")
            
        
        # copying
        try:
            shutil.copytree(path , self.pathToBackup + "/" + self.userName + "/" , dirs_exist_ok=True)
        except Exception as e:
            self.exceptionList.append(str(e))
        
        self.cLog.log("for forCommand_A_C function runned successfully" ,"i")


    # function for copying all the essential only of the current user
    def forCommand_A_C_E(self):
        pathList = []

        folderList = ["Desktop" , "Downloads" , "Pictures" , "Videos" , "Music" , "Documents"]

        for i in folderList:
            stringToAppend = "C:/Users/" + self.userName + "/"
            stringToAppend = stringToAppend + i
            pathList.append(stringToAppend)

        # stuff to use
        lengthToCopy = len(pathList)
        count = 1

        # actual copying starts here
        for i in pathList:
            print(f"on {count} out of {lengthToCopy}")
            # making sure that the path to backup exsist
            try:
                os.makedirs(self.pathToBackup + "/" + i[9:], exist_ok = True)
            except OSError:
                self.cLog.log("folder might be present for backUp_class-forCommand_A_C_E_func" , "e")
                self.cLog.exception(str(e) , "In backUp.py/backUp_class-forCommand_A_C_E_func")
            
            
            # making the copy
            try:
                shutil.copytree(i , self.pathToBackup + "/" + i[9:], dirs_exist_ok=True)
            except Exception as e:
                self.exceptionList.append(str(e))     
            count += 1
        
        self.cLog.log("for forCommand_A_C_E function runned successfully" ,"i")


    # function to get the list of additional directories
    def getListOfDirectories(self , listPassed):
        for i in listPassed:
            if(os.path.isdir(i)):
                self.listOfDirectories.append(i)
                status = True
            else:
                status = False
        
        if(status == False):
            self.cLog.log("path is incorrect error in getListOfDirectories" ,"e")


    # function for copying certain more directories from listPassed
    def forCopyListOfDirectories(self):

        for i in self.listOfDirectories:

            string = i[:1] + i[2:]

            try:
                os.makedirs(self.pathToBackup + "/additionalFiles/" + string, exist_ok = True)
            except OSError:
                self.cLog.log("folder might be present for backUp_class-forCopyListOfDirectories_func" , "e")
                self.cLog.exception(str(e) , "In backUp.py/backUp_class-forCopyListOfDirectories_func")
            
            # making the copy
            try:
                shutil.copytree(i ,self.pathToBackup + "/additionalFiles/" + string , dirs_exist_ok=True)
            except Exception as e:
                self.exceptionList.append(str(e))


    # driver function of the class this is what you will be calling
    def startBackUp(self, commandList , additionalDirectoryList , pathToBackup , toGenerateLogFile = True):
        
        self.getUserName()
        self.setPathToBackup(pathToBackup)
        self.getListOfDirectories(additionalDirectoryList)

        if(("-a" in commandList) and ("-c" in commandList) and ("-e" in commandList)):
           self.forCommand_A_C_E()
        elif(("-a" in commandList) and ("-c" in commandList) and ("-e" not in commandList)):
            self.forCommand_A_C()
        elif(("-a" in commandList) and ("-c" not in commandList) and ("-e" in commandList)): 
            self.forCommand_A_E()
        elif(("-a" in commandList) and ("-c" not in commandList) and ("-e" not in commandList)):
            self.forCommand_A()
        
        if("-d" in commandList):
            self.forCopyListOfDirectories()

        if(toGenerateLogFile == True):
            self.logFileGenerator()

        self.cLog.log("startBackUp function runned successfully", "i")


# driver code for testing purpose only
if __name__ == "__main__":
    obj = BackUp()
    commandList = ["-d"]
    obj.startBackUp(commandList , ["C:/Users/harsh/Desktop/kurskuzart"] , "C:/Users/harsh/desktop/jarvisBackup/")
