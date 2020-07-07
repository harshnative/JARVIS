# showing loading jarvis message just before everything loads up as some times while opening the program for first time, antivirus may scan all the included dlls when importing them into code and it takes time
print("\nLoading Jarvis.....")
print("\nThis may take few minutes for the first time :)")

isOnWindows = False
isOnLinux = False

# Checking weather the user is on windows or not
try:
    temp = os.environ
    tempUserName = temp["USERNAME"]
    isOnWindows = True
except Exception:
    isOnLinux = True

import time
import pyperclip
import psutil
import sys
from tabulate import tabulate
import os
import subprocess as sp

# generating jarvis folder
try:
    os.makedirs(r"C:\programData\Jarvis", exist_ok=True)
    print("folder check...")
except Exception:
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)
    print("Critical Error - could not generate jarvis folder in program data - contact developer")
    os.system("pause")

import datetime
import shutil
import ctypes
import logging
from imports.harshNative_github.googleDrive.googleDriveLinkPy import *
from imports.harshNative_github.txtCompare.txtComparePy import *
from imports.harshNative_github.hangMan_game.hangmanGame import *
from packages.loggerPackage.loggerFile import *
from packages.PasswordStorer.mainForPasswordStorer import *
from packages.settings.jarvisSetting import *
from packages.weather.getWeather import *
from packages.backUp_utility.backUp import *
from packages.speedTest_utility.speedTestFile import *



 

# creating global object of class Clogger
cLog = Clogger()

# setting TroubleShoot Value
troubleShootValue = False


# function to restart everything - just call the main again
def restart_program():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)
    cLog.log("program restarting..", "i")
    main()

# function to check if the script is running in administrative mode or not
# returns True ot Flase
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

# function to check for a substring in a string - returns true or false
def isSubString(string, subString):
    lengthOfSubString = len(subString)
    try:
        for i, j in enumerate(string):
            if(j == subString[0]):
                if(subString == string[i:i+lengthOfSubString]):
                    cLog.log("isSubString method runned successfully", "i")
                    return True
                else:
                    pass
        cLog.log("isSubString method runned successfully", "i")
        return False
    except Exception as e:
        cLog.log("isSubString function failed", "e")
        cLog.exception(str(e), "main.py/isSubString_func")
        return False


# function for displaying help
def getHelp(passObj):

    # for displaying all the help available
    if(passObj == "all"):
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        try:
            with open("txtFiles/help.txt") as fil:
                for line in fil:
                    print(line)
            cLog.log("if case in get help method runned successfully", "i")
        except FileNotFoundError:
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            cLog.log("help.txt file not found", "e")
            print(
                "oops , the help file in missing , try reinstalling the program or visit the website for help")
        except Exception as e:
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            cLog.log("error while opening the help file", "e")
            cLog.exception(str(e), "In main.py/getHelp_func-If_Part")
            if(cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")

    # for displaying specific help by searching for the keyords as substring in line
    else:
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        try:
            count = 0
            with open("txtFiles/help.txt") as fil:
                for line in fil:
                    for i in passObj:
                        if(isSubString(line, i)):
                            print(line)
                            count += 1
                if(count == 0):
                    print(
                        "oops no help found for entered prase , try writting only help for seeing all help available")
            cLog.log("else case in get help method runned successfully", "i")
        except FileNotFoundError:
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            cLog.log("help.txt file not found", "e")
            print(
                "oops , the help file in missing , try reinstalling the program or visit the website for help")
        except Exception as e:
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            cLog.log("error while opening the help file", "e")
            cLog.exception(str(e), "In main.py/getHelp_func-elsePart")
            if(cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")


# function for handling the get help
def handleGetHelp(command):
    commandList = command.split()
    # for getting the help - all - or specific things
    if(("help" in commandList) or ("Help" in commandList)):
        if(("open" in commandList) or ("Open" in commandList)):
            try:
                os.startfile(r"txtFiles\help.txt")
                cLog.log("help open command runned successfully", "i")
            except FileNotFoundError:
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                cLog.log("help.txt file not found", "e")
                print(
                    "oops the help.txt is missing ,try reinstalling the program or visit website for help")
            except Exception as e:
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                cLog.log("error while opening the help file", "e")
                cLog.exception(str(e), "In main.py/handleGetHelp_func")
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
            return True

        elif(len(commandList) > 1):
            getHelp(commandList)
            cLog.log("getHelp method called successfully", "i")
            return True

        else:
            getHelp("all")
            cLog.log("getHelp method called successfully", "i")
            return True

    return False


# function for handling troubleshooting
def troubleShootFunc():

    # setting troubleshoot value to true for logger module
    global troubleShootValue
    troubleShootValue = True
    cLog.setTroubleShoot(troubleShootValue)

    # starting customised main()
    objMainClass = MainClass()
    objMainClass.setUserName()
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)

    # getting user name so that we can output the log file to desktop
    temp = os.environ  # generates a object with the property called USERNAME containing the info
    tempUserName = temp["USERNAME"]

    # setting up paths to copy log file to desktop at the end
    pathToDesktop = "C:/Users/" + str(tempUserName) + "/Desktop" 
    pathToLog = str(cLog.logFileName)

    while(1):
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        #main command copied below with some modification
        print(f"welcome {objMainClass.returnUserName()}\n")
        print("You are in touble shoot mode : enter exit to exit troubleShootMode\n")
        commandInput = input("Enter Command in which you faced error and try to repeat the process : ")
        if(handleGetHelp(commandInput)):
            pass
        if(isSubString(commandInput , "troubleshoot") or isSubString(commandInput , "TroubleShoot") or isSubString(commandInput , "troubleShoot") or isSubString(commandInput , "Troubleshoot")):
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            print("Trouble shoot command is already running ...")
        if(isSubString(commandInput , "Exit") or isSubString(commandInput , "exit") or isSubString(commandInput , "EXIT")):
            return False

        else:
            if(executeCommands(commandInput)):
                print("\n\n")
                os.system("pause")

                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)
                
                try:
                    shutil.copy(pathToLog , pathToDesktop)
                    print("A log file is generated at the desktop")
                    print("\n" , cLog.getLogFileMessage)
                    print("\nNOTE : log file only contains diagnos data , NO personal information is stored")
                except Exception as e:
                    cLog.log("Could not generate log file at desktop" , "e")
                    cLog.exception(str(e) ,"In main.py/troubleshootfunc")
                    print("oops could make log file at desktop \nplease go to ", cLog.logFileName)
                    print("\n" , cLog.getLogFileMessage)
                    print("\nNOTE : log file only contains diagnos data , NO personal information is stored")
                    
                print("\n\n")
                os.system("pause")
                break

            else:
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                print("oops could not regonise the command , please enter the same command in which you previously faced error")

        print("\n\n")
        os.system("pause")
    
    troubleShootValue = False
    cLog.setTroubleShoot(troubleShootValue)
    return True


class MainClass():

    """
This class is used to generate dictionary from settings so that it can be used in program
                  
methods include - getDict()           ->  To generate dictionary - not for outside use
                
                - returnDict()        ->  To get the dictionary for use - returns dictionary directly when called
                
                - setUserName()       ->  To generate the user name from reading opearting system object - not for outside use
                
                - returnUserName()    ->  To get the username - returns user name in string format directly when called 
    """

    # contructor
    def __init__(self):
        self.settingsDict = {}
        self.getDict()

    # function to get the Dictionary from the settings module
    def getDict(self):
        objSetting = Setting(troubleShootValue)
        self.settingsDict = objSetting.getDictionary()
        if(self.settingsDict == False):
            cLog.log("Their was some error in the settings module so we cannot retreive the dictionary", "e")
            return False
        else:
            cLog.log("getDict function runned successfully", "i")
            return True
    
    def returnDict(self):
        status = self.getDict()
        if(status == True):
            return self.settingsDict
        else:
            return None

    def setUserName(self):
        temp = os.environ  # generates a object with the property called USERNAME containing the info
        tempUserName = temp["USERNAME"]
        try:
            if(self.settingsDict == False):
                self.settingsDict = {}
                self.settingsDict["userName"] = tempUserName
            elif(self.settingsDict["userName"] == ""):
                self.settingsDict["userName"] = tempUserName
                
        except KeyError:
            cLog.log("cannot get the username from setting", "i")
            try:
                self.settingsDict["userName"] = tempUserName
            except Exception as e:
                cLog.log("cannot get the username from system", "e")
                cLog.exception(str(e), "In main.py/class_mainClass-setUserName_function")

    def returnUserName(self):
        return self.settingsDict["userName"]


class MainWeatherClass(MainClass):

    """
This Class is a child of the MainClass and is used for handling the weather command

methods include - setCityName()          ->    used to set the city name  
                
                - addToList()            ->    used to add argument to the command list that will passed to weather module
                
                
                - toDeleteFromList()     ->    used to Delete the passed element from the command list
               
                - modifyList()           ->    used to modify the element in command list - both element to modify 
                                               & element to modify with arguments are to be passed
               
                - printWeatherDetails()  ->    used to print the finalweather details in a tablular format

their are some default things in the command list which if present , the print weather details will print them

default things in command list ["tempInC", "pressure", "humidity" , "temp_min" , "temp_max"] 
- you can change these with list modifications function provided
    """

    # constructor
    def __init__(self):
        self.cityName = None
        self.weatherArgumentList = ["tempInC", "pressure", "humidity" , "temp_min" , "temp_max"]
        self.humidityDetail = 0
        self.currentTempInC = -277


    # function to set the cityName

    def setCityName(self, cityPass):
        self.cityName = cityPass

    # function to add another elements to list to get their info as well

    def addToList(self, element):
        self.weatherArgumentList.append(element)


    # function to delete from list
    def toDeleteFromList(self , element):
        try:
            self.weatherArgumentList.remove(element)
            return True
        except Exception as e:
            cLog.log("connot delete from list in MainWeatherClass-toDeleteFromList function" , "e")
            cLog.exception(str(e) , "In main.py/MainWeatherClass-toDeleteFromList function")
            return False

    # function to modify item in list
    def modifyList(self , elementToModify , elementToModifyWith):
        listCopy = self.weatherArgumentList.copy()
        for i,j in enumerate(self.weatherArgumentList):
            if(j == elementToModify):
                listCopy[i] = elementToModifyWith
        self.weatherArgumentList = listCopy



    # function to print the weather details

    def printWeatherDetails(self):
        self.getDict()
        # if the cityName is not passed then we will take it from dictionary generated from settings app
        if(self.cityName == None):
            try:
                self.cityName = self.settingsDict["City"]
            except Exception:
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                cLog.log("user as not setted city in setting", "i")
                print("\nit looks like you have not setted any city in setting , run setting command to open settings\n")
                os.system("pause")

                # this is a critical error , so calling main again to restart the program
                main()

        # making a object of weather data class
        objGetWeatherData = WeatherData(troubleShootValue)

        # getting the result
        result = objGetWeatherData.getWeatherData(self.cityName, self.weatherArgumentList)

        # showing the result in tabular form
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        print(f"weather details of {self.cityName} are - \n")
        tabulateList = []
        errorYES = False
        for i, j in zip(self.weatherArgumentList, result):
            tempList = []
            if ((j == None)):
                toPass = "none for " + str(i)
                cLog.log(toPass , "e")
                errorYES = True
            else:
                i = str(i)
                if(i == "humidity"):
                    self.humidityDetail = float(j)
                elif(i == "tempInC"):
                    self.currentTempInC = float(j)
                elif(i == "tempInF"):
                    self.currentTempInC = (( float(j) - 32 ) * (5/9))
                j = str(j)
                tempList.append(i)
                tempList.append(j)
                tabulateList.append(tempList)
        if (errorYES):
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            print("Error While printing weather details")
            cLog.log("error while getting the wheather details in main.py", "e")
            print("\n\nif the error remains follow instructions : ")
            print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(cLog.logFileName))
            print("step 2 - {}".format(cLog.getLogFileMessage))
            cLog.log(
                "error while printing whether details , some things will be None", "e")
        else:
            print(tabulate(tabulateList, headers=['Query', 'Data']))
            print("\n")
            if(self.currentTempInC != -277):
                if(self.currentTempInC < 0):
                    print("Its pretty cold outside..")
                elif(self.currentTempInC < 12):
                    print("Its cold outside...")
                elif(self.currentTempInC < 25):
                    print("Its cozy outside...")
                elif(self.currentTempInC < 35):
                    print("Its Warm outside...")
                else:
                    print("Its pretty hot outside")
            else:
                cLog.log("Error while if condition for self.currentTempInC" , "e")
            
            print()
            if((self.humidityDetail >= 95) and (self.currentTempInC > 10)):
                print("Their is high probability of rain today , please carry your umbrella :)")
            elif((self.humidityDetail >= 90) and (self.currentTempInC > 10)):
                print("Their is some probability of rain today , you can carry your umbrella :)")
            elif((self.humidityDetail >= 95) and (self.currentTempInC <= 10)):
                print("Their is fog outside :)")
            elif((self.humidityDetail >= 90) and (self.currentTempInC <= 10)):
                print("Their is some fog outside :)")
            else:
                print("No chance of rain and fog today :)")


# function to execute the passed command by analysing it
def executeCommands(command):
    # spliting with " " to form a command list
    commandList = command.split()
    # checking for weather commands
    if(("weather" in commandList) or ("Weather" in commandList)):

        # creating object of main weather class
        objMainWeatherClass = MainWeatherClass()

        # looping through command list to get the cityname if present
        for com in commandList:

            # getting the city name - as to be city-cityName
            if(isSubString(str(command), "city")):
                for i, j in enumerate(com):
                    if(j == "c"):
                        if(com[i:i+4] == "city"):
                            cityName = com[i+5:]
                            cityNameEdit = ""
                            for i, j in enumerate(cityName):
                                if(j == "_"):
                                    cityNameEdit = cityName[:i] + \
                                        " " + cityName[i+1:]
                            if(cityNameEdit == ""):
                                pass
                            else:
                                cityName = cityNameEdit

            else:
                cityName = None

        # passing the city name to the class
        objMainWeatherClass.setCityName(cityName)

        # checking for additional commands
        if("-f" in commandList or "-F" in commandList):
            objMainWeatherClass.modifyList("tempInC" , "tempInF")

        # executing the command
        objMainWeatherClass.printWeatherDetails()
        cLog.log("weather command executed successfully", "i")
        return True

    # for restoring the defualt setting
    if(("restore" in commandList) or ("Restore" in commandList)):

        if(("setting" in commandList) or ("settings" in commandList) or ("Setting" in commandList) or ("Settings" in commandList)):
            objSetting = Setting(troubleShootValue)
            objSetting.regenerateFile()
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            print("you have restored the settings successfully")
            cLog.log("restore command runned successfully", "i")
            return True

        if(("jarvis" in commandList) or ("Jarvis" in commandList) or ("JARVIS" in commandList)):
            if(isOnWindows == True):
                os.system("cls")
            else:
                sp.call('clear',shell=True)

            #getting backup path
            objMainClass = MainClass()
            dictGet = objMainClass.returnDict()

            if(dictGet == None):
                print("Oops cannot restore jarvis :(")
                cLog.log("dictGet gets None value from returnDict" , "e")
                print("\nTry again, if error persist, run troubleShoot command")
                return True
            
            try:
                pathToBackupForJarvis = dictGet["backUpPathForJarvis"]
            except KeyError:
                print("it looks like you have not setted up path to backup for jarvis in setting , please set the path and try again ")
                print("\nif the error persist try running restore command")
                cLog.log("key error in jarvis backup in main.py" ,"e")
                return True
            except Exception as e:
                cLog.log("Exception occured in executeCommand in restore jarvis" , "e")
                cLog.exception(str(e) , "In main.py/executeCommand_function - restore jarvis")
                print("\nTry again, if error persist, run troubleShoot command")

            #running restore
            print("running restore , please wait...")
            try:
                shutil.copytree( pathToBackupForJarvis + "/" + "JarvisBackup" , "C:/programData/Jarvis" , dirs_exist_ok=True)
            except Exception as e:
                print("Cannot restore jarvis properly")
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("Some exception occured while restoring jarvis" , "e")
                cLog.exception(str(e) , "In main.py/ececuteCommand_func-in jarvis restore")
                return True
            
            print("\nRestore completed...")
            return True

    # for changing teh setting - this function opens the settings.txt in the defualt txt viewer of the system
    if(("Setting" in commandList) or ("setting" in commandList) or ("Settings" in commandList) or ("settings" in commandList)):
        objSetting = Setting(troubleShootValue)
        objSetting.openFile()
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        print("the settings file is opened, make sure to save the file run update command in jarvis")
        cLog.log("setting command runned successfully", "i")
        return True

    # function for updating the settings
    if(("update" in commandList) or ("Update" in commandList)):
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        print("settings have been updated , programm will restart now\n\n")
        os.system("pause")
        restart_program()

    # calling for backup command
    if(("backup" in commandList) or ("Backup" in commandList)):
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        # for backupUp jarvis things i.e things in folder program data - jarvis
        if(("jarvis" in commandList) or ("Jarvis" in commandList) or ("JARVIS" in commandList)):
            objMainClass = MainClass()
            dictGet = objMainClass.returnDict()

            if(dictGet == None):
                print("Oops cannot backup jarvis :(")
                cLog.log("dictGet gets None value from returnDict" , "e")
                print("\nTry again, if error persist, run troubleShoot command")
                return True
            
            try:
                pathToBackupForJarvis = dictGet["backUpPathForJarvis"]
            except KeyError:
                print("it looks like you have not setted up path to backup for jarvis in setting , please set the path and try again ")
                print("\nif the error persist try running restore command")
                cLog.log("key error in jarvis backup in main.py" ,"e")
                return True
            except Exception as e:
                cLog.log("Exception occured in executeCommand in backupjarvis" , "e")
                cLog.exception(str(e) , "In main.py/executeCommand_function - backup jarvis")
                print("\nTry again, if error persist, run troubleShoot command")
                return True

            print("backing up jarvis , please wait...")
            # running backup
            try:
                shutil.copytree("C:/programData/Jarvis" , pathToBackupForJarvis + "/" + "JarvisBackup" ,  dirs_exist_ok=True)
            except Exception as e:
                print("Cannot backup jarvis properly")
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("Some exception occured while backuping up jarvis" , "e")
                cLog.exception(str(e) , "In main.py/ececuteCommand_func-in jarvis backup")
                return True

            print("\nBackup completed.....")
            return True
            # backup jarvis code ends here


        # excecuting backup module functionalities
        # creating a copy of backup command without the backup keyword so that we can pass it to the startBackup function of the class backUp
        commandListCopy = commandList.copy()
        if("backup" in commandList):
            commandListCopy.remove("backup")
        elif("Backup" in commandList):
            commandListCopy.remove("Backup")

        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        if(isAdmin()):
            pass
        else:
            print("Please restart the jarvis in the administrative mode and run command again")
            print("\nAs right now some important files will not be backed up due to permission issues")
            print("\nIf you still want to continue then type continue below or press enter to exit\n")

            inputForContinueOrNot = input(" : ")

            if(inputForContinueOrNot == "continue"):
                pass
            else:
                restart_program()

        # creating object of class backUp
        objBackUp = BackUp(troubleShootValue)

        # creating object of class setting
        objSetting = Setting(troubleShootValue)

        # creating some required assets
        directoriesListEditted = []
        dictionaryFromSetting = objSetting.getDictionary()

        # checking if -d is in command
        if("-d" in commandList):
            if(dictionaryFromSetting["backUpPath"] == ""):
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                print(
                    "it looks like you have not added any folder's to backup in setting file")
                print(
                    "\n\ntype change settings in the command to open the file and then run update command")
                print("\n\ntype help settings for additional help")
                return True
            else:
                pathToBackup = str(dictionaryFromSetting["backUpPath"])
                try:
                    os.mkdir(pathToBackup + "/" + "jarvisBackup")
                    pathToBackup = pathToBackup + "/" + "jarvisBackup"
                except OSError as e:
                    if(isOnWindows == True):
                        os.system("cls")
                    else:
                        sp.call('clear',shell=True)

                    pathToBackup = pathToBackup + "/" + "jarvisBackup"
                    cLog.log("OSError for execute command under backup", "e")
                    cLog.exception(str(e), "In main.py/executeCommmand_func_backupCommand")
                    print("folder in path to backup in settings already exit or may be the path is not found")
                    print("\n\nif the folder already exit - then all the file's will be overRidden")
                    print("\n\npress enter to continue with backup or close the program to stop it")
                    input()
                    if(isOnWindows == True):
                        os.system("cls")
                    else:
                        sp.call('clear',shell=True)

            # if backup path is correct then if need to ckeck if the directories are listed in setting's file or not
            if(dictionaryFromSetting["Directories"] == ""):
                if(isOnWindows == True):
                    os.system("cls")
                else:
                    sp.call('clear',shell=True)

                print(
                    "it looks like you have not added any folder's to directories in setting file")
                print(
                    "\n\ntype change settings in the command to open the file and then run update command")
                print("\n\ntype help settings for additional help")
                cLog.log(
                    "no folder added to directory error in execute command function in backup command", "e")
                return True
            else:
                directoriesGenerated = str(
                    dictionaryFromSetting["Directories"])
                directoriesList = directoriesGenerated.split(",")

                # created a list of directories to pass on to the function startbackup of class backup
                for i in directoriesList:
                    i = i.strip()
                    directoriesListEditted.append(i)

        # calling the function to start the copy process
        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)

        print("\nBackUp in process - This may take several minutes....")
        print("\nplease do not close the program , otherWise files may get corrupted")
        objBackUp.startBackUp(
            commandListCopy, directoriesListEditted, pathToBackup + "/")

        if(isOnWindows == True):
            os.system("cls")
        else:
            sp.call('clear',shell=True)
            
        print("\n\nCopy completed\nlog file is generated at the desktop , their may me some files that may not have been copied due to permission errors :(")
        cLog.log("executeCommand function runned backupCommand successfully", "i")
        return True

    # calling for hangman game
    if(("hangman" in commandList) or ("Hangman" in commandList)):
        if(("game" in commandList) or ("Game" in commandList)):
            os.system("cls")
            # calling the game function
            boolValue = mainForHangmanGame()
            os.system("cls")
            if(boolValue == True):
                print("thanks for playing game")
            else:
                print("some error ocurred :( , try reinstalling the program")
                cLog.log("some error occured in hangman game", "e")
            return True


    # calling for txt compare
    if(("compare" in commandList) or ("Compare" in commandList)):
        if(("txt" in commandList) or ("Txt" in commandList) or ("TXT" in commandList)):
            os.system("cls")
            print("starting txtCompare program :)\n\n")
            try:
                mainForTxtCompare()
            except Exception:
                cLog.log("some error occured while comparing txt files", "e")
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
            return True


    # calling for google drive link
    if(("google" in commandList) or ("Google" in commandList)):
        if(("drive" in commandList) or ("Drive" in commandList)):
            os.system("cls")
            print("Go to the file saved in google drive and click get shareable link\n")
            linkGet = input("Paste the link here : ")
            linkFinal = mainForGoogleDriveLink(linkGet)
            if(linkFinal == False):
                print("\n\nThe link is in valid :(")
                cLog.log(
                    "google drive command runned succesfully , but the link was invalid", "i")
                return True
            else:
                pyperclip.copy(str(linkFinal))
                pyperclip.paste()
                print("\n\nThe link is {} and is been copied to clipboard :)".format(linkFinal))
                cLog.log("google drive command runned succesfully", "i")
                return True

    # calling for random generator
    if(("generate" in commandList) or ("Generate" in commandList)):
        if(("random" in commandList) or ("Random" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\anyRandom.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                cLog.log("external exe file not found", "e")
                print("The random generator file is missing")
            except Exception as e:
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("error on generate random command", "e")
                cLog.exception(str(e), "In generate random command")
            return True


    # calling for number system convertor
    if(("number" in commandList) or ("Number" in commandList) or ("num" in commandList) or ("Num" in commandList) or ("no" in commandList) or ("No" in commandList) or ("NO" in commandList)):
        if(("convert" in commandList) or ("conv" in commandList) or ("convertor" in commandList) or ("Convert" in commandList) or ("Conv" in commandList) or ("Convertor" in commandList)):
            if(("system" in commandList) or ("sys" in commandList) or ("System" in commandList) or ("Sys" in commandList)):
                os.system("cls")
                try:
                    os.startfile(r"external_exe\harshNative_github\NSC.exe")
                    print("The file is opened in other window :)")
                except FileNotFoundError:
                    cLog.log("external exe file not found", "e")
                    print("The number convert file is missing")
                except Exception as e:
                    if(cLog.troubleShoot == False):
                        print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
                    cLog.log("error on number system command", "e")
                    cLog.exception(str(e), "In number system convertor command")
                return True


    # calling for average finder
    if(("average" in commandList) or ("Average" in commandList) or ("avg" in commandList) or ("Avg" in commandList) or ("AVG" in commandList)):
        os.system("cls")
        try:
            os.startfile(r"external_exe\harshNative_github\average_finder.exe")
            print("The file is opened in other window :)")
        except FileNotFoundError:
            cLog.log("external exe file not found", "e")
            print("The average finder file is missing")
        except Exception as e:
            if(cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
            cLog.log("error on average finder command", "e")
            cLog.exception(str(e), "In average finder command")
        return True

    # calling for coin toss
    if(("Coin" in commandList) or ("coin" in commandList)):
        if(("toss" in commandList) or ("Toss" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\coin_toss.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                cLog.log("external exe file not found", "e")
                print("The coin toss file is missing")
            except Exception as e:
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("error on coin toss command", "e")
                cLog.exception(str(e), "In coin toss command")
            return True


    # calling for group generator
    if(("group" in commandList) or ("Group" in commandList)):
        if(("generate" in commandList) or ("Generate" in commandList)):
            os.system("cls")
            try:
                os.startfile(
                    r"external_exe\harshNative_github\group_Generator.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                cLog.log("external exe file not found", "e")
                print("The group generator file is missing")
            except Exception as e:
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("error on group generate command", "e")
                cLog.exception(str(e), "In group generate command")
            return True


    # calling for interest calculator
    if(("calculator" in commandList) or ("Calculator" in commandList) or ("calc" in commandList) or ("Calc" in commandList)):
        if(("Interest" in commandList) or ("interest" in commandList)):
            os.system("cls")
            try:
                os.startfile(
                    r"external_exe\harshNative_github\interest_Calculator.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                cLog.log("external exe file not found", "e")
                print("The interest calculator file is missing")
            except Exception as e:
                if(cLog.troubleShoot == False):
                    print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                cLog.log("error on calc interest command", "e")
                cLog.exception(str(e), "In calc interest command")
            return True
 

    # calling for password manager
    if(("Password" in commandList) or ("password" in commandList) or ("pass" in commandList) or ("Pass" in commandList)):
        objPasswordStorerClass = PasswordStorerClass(troubleShootValue)
        objPasswordStorerClass.driverFunc()
        return True

    # handling command to run in jarvis in cmd window
    if(("cmd" in commandList) or ("Cmd" in commandList) or ("CMD" in commandList)):
        os.system("cls")
        print("opening jarvis in command prompt")
        os.startfile(r"jarvis_CMD.bat")
        print("\njarvis opened in command prompt")
        print("\nExisting this instance of jarvis")
        time.sleep(1)
        exit()
    
    # handling utc time and date
    if(("utc" in commandList) or ("UTC" in commandList) or ("Utc" in commandList)):
        if(("time" in commandList) or ("Time" in commandList)):
            newObj = str(datetime.datetime.utcnow())
            currentDate = newObj[8:10] + "/" + newObj[5:7] + "/" + newObj[:4]
            currentTime = newObj[11:19] 
            os.system("cls")
            print("UTC TIME = {}".format(currentTime))
            print("UTC DATE = {}".format(currentDate))
            return True

    # handling simple time command
    if(("time" in commandList) or ("Time" in commandList)):
        newObj = str(datetime.datetime.now())
        currentDate = newObj[8:10] + "/" + newObj[5:7] + "/" + newObj[:4]
        currentTime = newObj[11:19] 
        os.system("cls")
        print("TIME = {}".format(currentTime))
        print("DATE = {}".format(currentDate))
        return True

    # handling font size command
    if(("Font" in commandList) or ("font" in commandList)):
        if(("Size" in commandList) or ("size") in commandList):
            os.system("cls")
            print("To change the font size follow these steps : ") 
            print("\n1. right click on the jarvis logo on top left corner")
            print("\n2. click on the defaults button")
            print("\n3. navigate to font panel and change the font size")
            print("\n4. restart the program by closing it")
            print("\nRecommended font size is 18")
            print("\nTo change the font size temporarily - click on properties instead of defaults")
            return True

    # handling font colour command
    if(("Font" in commandList) or ("font" in commandList)):
        if(("colour" in commandList) or ("Colour" in commandList) or ("Color" in commandList) or ("color" in commandList)):
            os.system("cls")
            print("To change the font colour follow these steps : ") 
            print("\n1. right click on the jarvis logo on top left corner")
            print("\n2. click on the defaults button")
            print("\n3. navigate to colours panel and make sure screen text is selected")
            print("\n4. select the colour and restart the program by closing it")
            print("\nRecommended font colour is green or grey")
            print("\nTo change the font size temporarily - click on properties instead of defaults")
            return True
    
    # handling speed test command
    if(("speed" in commandList) or ("Speed" in commandList)):
        if(("test" in commandList) or ("Test" in commandList)):
            commandListCopy = commandList.copy()

            # removing speed and test word from the command list
            try:
                commandListCopy.remove("speed")
            except Exception:
                try:
                    commandListCopy.remove("Speed")
                except Exception as e:
                    print("Failed to run speed test")
                    cLog.log("could not delete speed from command list copy in speed test command in executecommand in main.py" , "e")
                    cLog.exception(str(e) , "in main.py/executeCommand_function - running command speed test")
                    return True
            
            try:
                commandListCopy.remove("test")
            except Exception:
                try:
                    commandListCopy.remove("Test")
                except Exception as e:
                    print("Failed to run speed test")
                    cLog.log("could not delete test from command list copy in speed test command in executecommand in main.py" , "e")
                    cLog.exception(str(e) , "in main.py/executeCommand_function - running command speed test")
                    return True
            
            # for getting result in bytes - default value is NO
            inBytes = False
            
            # number of time the result should average out - default value of module is also 2
            numberOfTime = 2
            
            # checking if user wants result in bytes 
            for i in commandListCopy:
                if("-b" in commandListCopy):
                    inBytes = True
                try:
                    numberOfTime = int(i)

                    # if the number of time is greator than 5 then it will take very long time to process to making it again default
                    if(numberOfTime >= 5):
                        numberOfTime = 2
                except Exception:
                    pass

            # creating object of class in module speed test utility 
            objSpeedTestClass = SpeedTestClass(troubleShootValue)

            # calling method of class for execution
            objSpeedTestClass.runSpeedTestUtility(inBytes , numberOfTime)
            return True     # as all runned successfully

    # handling troubleshoot command
    if(("troubleshoot" in commandList) or ("TroubleShoot" in commandList) or ("Troubleshoot" in commandList) or ("troubleShoot" in commandList)):
        status = troubleShootFunc()

        os.system("cls")
        if(status == True):
            print("Trouble shooting complete, don't forget to mail us the log file at myjarvispa@gmail.com")
        else:
            print("toubleshooting stopped in between")
        return True

    # calling for exit command
    if(("exit" in commandList) or ("EXIT" in commandList) or ("Exit" in commandList)):
        os.system("cls")
        print("See you soon :) , Exiting the program ", end="", flush=True)
        time.sleep(0.3)
        print(".", end="", flush=True)
        time.sleep(0.3)
        print(".", end="", flush=True)
        time.sleep(0.4)
        print(".", end="", flush=True)
        os.system("cls")
        exit()

    # if none of the above command is executed than return false to tell the user that the command entered was incorrect
    return False


def main():

    # setting api key's

    # for weather module - get your api key from open weather as pass it here
    WeatherData.setApiKey("fe82651e607e46db61dba45e39aa7e17")

    # checking the api key's
    if(WeatherData.returnApiKeyStatus() == False):
        raise NotImplementedError("Set the open weather api")

    # setting trouble shoot value
    cLog.setTroubleShoot(troubleShootValue)

    objMainClass = MainClass()
    while(1):
        objMainClass.setUserName()
        os.system("cls")
        print(f"welcome {objMainClass.returnUserName()}\n")
        commandInput = input("Enter Command : ")
        if(handleGetHelp(commandInput)):
            pass
        else:
            if(executeCommands(commandInput)):
                pass
            else:
                os.system("cls")
                print("oops could not regonise the command try typing help for info")

        print("\n\n")
        os.system("pause")


def driverForMain():
    
    # calling main
    main()

if __name__ == "__main__":
    driverForMain()
