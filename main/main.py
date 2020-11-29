# declaring global variables -
class GlobalData_main:
    # global variable for making sound while typing
    toMakeTypingSound = False
    
    # setting TroubleShoot Value
    troubleShootValue = True

    # initialising the global variable to False so that it can be changed if the operating system is supported
    isOnWindows = False
    isOnLinux = False

    # setting default port number for file share 
    portNumberForFileShare = 5000
    
    # global variable for running loading animation is set to true 
    runLoadingAnimation = True
    loadingAnimationCount = 10

    # list of currenlty opened thread
    threadOpenedList = []  

    # file share obj
    fileShareObj = None

    # default paths for program data 
    folderPathWindows = r"C:\programData\Jarvis"
    folderPathLinux = r"~/.config/Jarvis"
    folderPathWindows_simpleSlash = r"C:/programData/Jarvis"

    # global variable for knowing if the jarvis is runned by cmd arguments
    directRunFromCmd = False














# importing some essential modules
import os
import platform
from subprocess import SubprocessError
import time
import subprocess as sp
import time
from threading import Thread
import sys







# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_main.isOnLinux = True
elif(osUsing == "Windows"):
    GlobalData_main.isOnWindows = True
else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    sys.exit()









# clear screen function 
def customClearScreen():
    if(GlobalData_main.isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)








# loading animation thread
class LoadingAnimation(Thread):

    def run(self):

        customClearScreen()
        string = ""

        while(GlobalData_main.runLoadingAnimation and GlobalData_main.loadingAnimationCount):
            string = string + "."
            time.sleep(0.5)
            print("\rloading , please wait " , string , sep = "" , end = "")
            GlobalData_main.loadingAnimationCount -= 1

        print()

if __name__ == "__main__":
    # loading animation thread started 
    lAnimation = LoadingAnimation()
    lAnimation.start()

# this function sets the global runLoadingAnimation variable to False so that the while loop in thread stops and it indicates the jarvis is fully loaded now
def changeRunLoadingAnimation():

    GlobalData_main.runLoadingAnimation = False






  
# importing additional modules
import pyperclip
from tabulate import tabulate
import getpass as getUserName
from playsound import playsound
import datetime
import shutil
import ctypes
from os import execlp, path
import multiprocessing
from tkinter import filedialog
from tkinter import *
import subprocess




# importing custom modules
from imports.harshNative_github.googleDrive.googleDriveLinkPy import *
from imports.harshNative_github.txtCompare.txtComparePy import *
from imports.harshNative_github.hangMan_game.hangmanGame import *
from packages.loggerPackage.loggerFile import *
from packages.PasswordStorer.newMainForPassword import *
from packages.PasswordStorer.mainForPasswordStorer import PasswordStorerClass as PasswordStorerClassOld
from packages.settings.jarvisSetting import *
from packages.weather.getWeather import *
from packages.backUp_utility.backUp import *
from packages.speedTest_utility.speedTestFile import *
from packages.fileShare import FS



# checking if the jarvis is runned directly from the cmd arguments
if(len(sys.argv) > 1):
    GlobalData_main.directRunFromCmd = True


# generating jarvis folder were the data will be stored
try:
    if(GlobalData_main.isOnWindows):
        os.makedirs(GlobalData_main.folderPathWindows , exist_ok=True)
    else:
        os.makedirs(GlobalData_main.folderPathLinux , exist_ok=True)

except Exception:
    customClearScreen()
    print("Critical Error - could not generate jarvis folder in program data - contact developer")
    input("press enter to continue...")





# generating some objects of important classes
# importing tkinter
root = Tk()
root.withdraw()

# creating global object of class Clogger (custom log module)
cLog = Clogger()






# some function's
# function to restart everything - just call the main again
def restart_program():

    customClearScreen()
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
        customClearScreen()

        try:
            with open("txtFiles/help.txt") as fil:
                for line in fil:
                    print(line)
            cLog.log("if case in get help method runned successfully", "i")
        except FileNotFoundError:
            customClearScreen()

            cLog.log("help.txt file not found", "e")
            print(
                "oops , the help file in missing , try reinstalling the program or visit the website for help")
        except Exception as e:
            customClearScreen()

            cLog.log("error while opening the help file", "e")
            cLog.exception(str(e), "In main.py/getHelp_func-If_Part")
            if(cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")

    # for displaying specific help by searching for the keyords as substring in line
    else:
        customClearScreen()

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
            customClearScreen()

            cLog.log("help.txt file not found", "e")
            print(
                "oops , the help file in missing , try reinstalling the program or visit the website for help")
        except Exception as e:
            customClearScreen()

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
                customClearScreen()

                cLog.log("help.txt file not found", "e")
                print(
                    "oops the help.txt is missing ,try reinstalling the program or visit website for help")
            except Exception as e:
                customClearScreen()

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
    GlobalData_main.troubleShootValue = True
    cLog.setTroubleShoot(GlobalData_main.troubleShootValue)

    # starting customised main()
    objMainClass = MainClass()
    objMainClass.setUserName()
    customClearScreen()

    # getting user name so that we can output the log file to desktop
    tempUserName = getUserName.getuser()
    pathToDesktop = ""
    # setting up paths to copy log file to desktop at the end
    if(GlobalData_main.isOnWindows):
        pathToDesktop = "C:/Users/" + str(tempUserName) + "/Desktop"
    elif(GlobalData_main.isOnLinux):
        pathToDesktop =  os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 

    pathToLog = str(cLog.logFileName)

    while(1):
        customClearScreen()

        #main command copied below with some modification
        print(f"welcome {objMainClass.returnUserName()}\n")
        print("You are in touble shoot mode : enter exit to exit troubleShootMode\n")
        commandInput = input("Enter Command in which you faced error and try to repeat the process : ")
        if(handleGetHelp(commandInput)):
            pass
        if(isSubString(commandInput , "troubleshoot") or isSubString(commandInput , "TroubleShoot") or isSubString(commandInput , "troubleShoot") or isSubString(commandInput , "Troubleshoot")):
            customClearScreen()

            print("Trouble shoot command is already running ...")
        if(isSubString(commandInput , "Exit") or isSubString(commandInput , "exit") or isSubString(commandInput , "EXIT")):
            return False

        else:
            if(executeCommands(commandInput)):
                print("\n\n")
                input("press enter to continue...")

                customClearScreen()
                
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
                input("press enter to continue...")
                break

            else:
                customClearScreen()

                print("oops could not regonise the command , please enter the same command in which you previously faced error")

        print("\n\n")
        input("press enter to continue...")
    
    GlobalData_main.troubleShootValue = False
    cLog.setTroubleShoot(GlobalData_main.troubleShootValue)
    return True





# function to handle file sharing using easyFileShare - module 
def handleFileShare(folderPass , portNumber = 8000 , passIpOnly = False):
    obj = FS.FileShareClass()

    if(passIpOnly):
        return str(obj.get_ip_address())

    # multi process starts the whole program again
    changeRunLoadingAnimation()
    lAnimation.join()

    customClearScreen()
    obj.start_fileShare(str(folderPass) , int(portNumber))





# function to get the folder path of folder selected from the file explorer
def get_folderPath_fromFileExplorer():
    folder_selected = filedialog.askdirectory()
    return folder_selected





# function to compare two strings ignoring case changes
def isSubStringsNoCase(string , subString):
    string = string.upper()
    subString = subString.upper()

    subStringList = subString.split()

    count1 = 0
    count2 = 0

    for i in subStringList:
        i = i.strip()
        count1 += 1
        if(isSubString(string , i)):
            count2 += 1
        else:
            return False


    if((count1 == count2) and count1 > 0):
        return True
    else:
        return False





class startingSound(Thread):
    def run(self):
        playsound("sounds/jarvisIntro.mp3")






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
        objSetting = Setting(GlobalData_main.troubleShootValue ,GlobalData_main.toMakeTypingSound)
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
        tempUserName = getUserName.getuser()
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
                customClearScreen()

                cLog.log("user as not setted city in setting", "i")
                print("\nit looks like you have not setted any city in setting , run setting command to open settings\n")
                input("press enter to continue...")

                # this is a critical error , so calling main again to restart the program
                main()

        # making a object of weather data class
        objGetWeatherData = WeatherData(GlobalData_main.troubleShootValue , GlobalData_main.toMakeTypingSound)

        # getting the result
        result = objGetWeatherData.getWeatherData(self.cityName, self.weatherArgumentList)

        # showing the result in tabular form
        customClearScreen()

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
            customClearScreen()

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

    # statement to run commands passed for cmd in windows
    if(command[:3] == ("cmd" or "CMD" or "Cmd")):
        customClearScreen()
        newCommand = str(command[4:])
        customClearScreen()
        os.system(newCommand)
        return True

    # statement to run commands passed for cmd in windows
    elif(isSubStringsNoCase(command , "git")):
        customClearScreen()

        message = "no message"

        messageFrom = 0

        for i,j in enumerate(command):
            if(j == "-"):
                messageFrom = i
                if(command[i+1] == "m"):
                    message = command[i+3:]  
                    break      

        if(messageFrom == 0):
            commandForCompare = command
        else:
            commandForCompare = command[:messageFrom]

        if((isSubStringsNoCase(commandForCompare , "log"))):
            print("Generating logs ... , press q to quit , or press ENTER to see more\n\n")
            os.system("git log --graph --oneline --all --decorate")
            return True

        
        if(isSubStringsNoCase(commandForCompare , "commit")):

            # initialising repo
            try:
                result = subprocess.check_output("git init", shell=True)
            except Exception:
                print("failed to git init")
                return True

            if(not(result == b'')):
                print(result)
            print("\n\ninitialised repo..")

            time.sleep(1)
            customClearScreen()

            # adding
            try:
                result = subprocess.check_output("git add .", shell=True)
            except Exception:
                print("failed to git add .")
                return True

            if(not(result == b'')):
                print(result)
            print("\n\nadded to repo..")

            time.sleep(1)
            customClearScreen()
            
            # commiting
            stringToPass = "git commit -m " + '"' + message + '"'

            try:
                result = subprocess.check_output(stringToPass, shell=True)
            except Exception:
                print("failed to git commit with message = {}".format(message))
                return True
                
            if(not(result == b'')):
                print(result)
            print("\n\ncommited to repo..")
            time.sleep(1)
            customClearScreen()

            print("process completed (^_^)")
            return True
            
            
            return True

        elif(isSubStringsNoCase(commandForCompare , "all")):
            
            # adding
            try:
                result = subprocess.check_output("git add .", shell=True)
            except Exception:
                print("failed to git add .")
                return True

            if(not(result == b'')):
                print(result)
            print("\n\nadded to repo..")

            time.sleep(1)
            customClearScreen()
            
            # commiting
            stringToPass = "git commit -m " + '"' + message + '"'

            try:
                result = subprocess.check_output(stringToPass, shell=True)
            except Exception:
                print("failed to git commit with message = {}".format(message))
                return True
                
            if(not(result == b'')):
                print(result)
            print("\n\ncommited to repo..")
            time.sleep(1)
            customClearScreen()
            
            #pushing
            print("pushing to repo, make sure you are connected to internet ...\n\n")

            try:
                result = subprocess.check_output("git push", shell=True)
            except Exception:
                print("failed to git push")
                return True

            if(not(result == b'')):
                print(result)
            print("\n\npushed to repo..")

            time.sleep(1)   
            customClearScreen()

            print("process completed (^_^)")
            return True

        return False

    # hello command handling
    elif(isSubStringsNoCase(command , "hello")):
        customClearScreen()
        print("Hello sir, What can i do for you. You can ask for help also (^_^)")
        print("\n")
        command = input("Enter Command : ")
        executeCommands(command)
        return True
    

    # checking for weather commands
    elif(isSubStringsNoCase(command , "weather")):

        # checking weather api key status
        if((WeatherData.getApiKey() == "") or (WeatherData.returnApiKeyStatus() == False)):
            customClearScreen()
            print("weather api key is either empty or not setted")
            return True

        customClearScreen()
        print("please wait while jarvis fetches weather data")

        # creating object of main weather class
        objMainWeatherClass = MainWeatherClass()
        commandList = command.split()

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
    elif(isSubStringsNoCase(command , "restore")):

        if(isSubStringsNoCase(command , "setting")):
            objSetting = Setting(GlobalData_main.troubleShootValue , GlobalData_main.toMakeTypingSound)
            objSetting.regenerateFile()
            customClearScreen()

            print("you have restored the settings successfully")
            cLog.log("restore command runned successfully", "i")
            return True

        if(isSubStringsNoCase(command , "jarvis")):
            customClearScreen()

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
                shutil.copytree(pathToBackupForJarvis + "/" + "JarvisBackup" , GlobalData_main.folderPathWindows_simpleSlash , dirs_exist_ok=True)
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
    elif(isSubStringsNoCase(command , "open setting")):
        objSetting = Setting(GlobalData_main.troubleShootValue , GlobalData_main.toMakeTypingSound)
        objSetting.openFile()
        customClearScreen()

        print("the settings file is opened, make sure to save the file run update command in jarvis")
        cLog.log("setting command runned successfully", "i")
        return True

    # function for updating the settings
    elif(isSubStringsNoCase(command , "update")):
        customClearScreen()

        print("settings have been updated , programm will restart now\n\n")
        input("press enter to continue...")
        restart_program()

    # calling for backup command
    elif(isSubStringsNoCase(command , "backup")):
        customClearScreen()

        # for backupUp jarvis things i.e things in folder program data - jarvis
        if(isSubStringsNoCase(command , "jarvis")):
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
                shutil.copytree(GlobalData_main.folderPathWindows_simpleSlash , pathToBackupForJarvis + "/" + "JarvisBackup" ,  dirs_exist_ok=True)
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
        commandList = command.split()
        commandListCopy = commandList.copy()
        if("backup" in commandList):
            commandListCopy.remove("backup")
        elif("Backup" in commandList):
            commandListCopy.remove("Backup")

        customClearScreen()

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
        objBackUp = BackUp(GlobalData_main.troubleShootValue , GlobalData_main.toMakeTypingSound)

        # creating object of class setting
        objSetting = Setting(GlobalData_main.troubleShootValue , GlobalData_main.toMakeTypingSound)

        # creating some required assets
        directoriesListEditted = []
        dictionaryFromSetting = objSetting.getDictionary()
        pathToBackup = ""

        if(dictionaryFromSetting["backUpPath"] == ""):
            customClearScreen()

            print(
                "it looks like you have not added any folder's to backup in setting file")
            print(
                "\n\ntype open settings in the command to open the file and then run update command")
            print("\n\ntype help settings for additional help")
            return True
        else:
            pathToBackup = str(dictionaryFromSetting["backUpPath"])
            try:
                os.mkdir(pathToBackup + "/" + "jarvisBackup")
                pathToBackup = pathToBackup + "/" + "jarvisBackup"
            except OSError as e:
                customClearScreen()

                pathToBackup = pathToBackup + "/" + "jarvisBackup"
                cLog.log("OSError for execute command under backup", "e")
                cLog.exception(str(e), "In main.py/executeCommmand_func_backupCommand")
                print("folder in path to backup in settings already exit or may be the path is not found")
                print("\n\nif the folder already exit - then all the file's will be overRidden")
                print("\n\npress enter to continue with backup or close the program to stop it")
                input()
                customClearScreen()

        # checking if -d is in command
        if("-d" in commandList):

            # if backup path is correct then if need to ckeck if the directories are listed in setting's file or not
            if(dictionaryFromSetting["Directories"] == ""):
                customClearScreen()

                print(
                    "it looks like you have not added any folder's to directories in setting file")
                print(
                    "\n\ntype open settings in the command to open the file and then run update command")
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
        customClearScreen()

        print("\nBackUp in process - This may take several minutes....")
        print("\nplease do not close the program , otherWise files may get corrupted\n")
        objBackUp.startBackUp(
            commandListCopy, directoriesListEditted, pathToBackup + "/")


        customClearScreen()

        print("\n\nCopy completed\nlog file is generated at the desktop , their may me some files that may not have been copied due to permission errors :(")
        cLog.log("executeCommand function runned backupCommand successfully", "i")
        return True

    # calling for hangman game
    elif(isSubStringsNoCase(command , "hangman game")):
        customClearScreen()

        # calling the game function
        boolValue = mainForHangmanGame()

        customClearScreen()

        if(boolValue == True):
            print("thanks for playing game")
        else:
            print("some error ocurred :( , try reinstalling the program")
            cLog.log("some error occured in hangman game", "e")
        return True


    # calling for txt compare
    elif(isSubStringsNoCase(command , "compare txt")):
        customClearScreen()

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
    elif(isSubStringsNoCase(command , "google drive") or isSubStringsNoCase(command , "link convert")):
        customClearScreen()

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
    elif(isSubStringsNoCase(command , "generate random")):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\anyRandom.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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
    elif((isSubStringsNoCase(command , "num") or isSubStringsNoCase(command , "no")) and (isSubStringsNoCase(command , "conv")) and (isSubStringsNoCase(command , "sys"))):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\NSC.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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
    elif(isSubStringsNoCase(command , "average") or isSubStringsNoCase(command , "avg")):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\average_finder.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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
    elif(isSubStringsNoCase(command , "coin toss")):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\coin_toss.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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
    elif(isSubStringsNoCase(command , "generate group")):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\group_Generator.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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
    elif(isSubStringsNoCase(command , "calc int")):
        customClearScreen()

        try:
            if(GlobalData_main.isOnWindows):
                os.startfile(r"external_exe\harshNative_github\interest_Calculator.exe")
                print("The file is opened in other window :)")
            else:
                print("only for windows users :(")
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

    
    # function to start the jarvis in updated code base - only for developer
    elif(isSubStringsNoCase(command , "start new ins")):
        customClearScreen()
        if(GlobalData_main.troubleShootValue == False):
            return False
        else:
            if(GlobalData_main.isOnWindows):
                os.system("python main/main.py")
                sys.exit()

            elif(GlobalData_main.isOnLinux):
                os.system("python3 main/main.py")
                sys.exit()
                
            return False

    # calling for password manager old
    elif(isSubStringsNoCase(command , "old password")):
        objPasswordStorerClass = PasswordStorerClassOld(GlobalData_main.troubleShootValue)
        objPasswordStorerClass.driverFunc()
        return True
 

    # calling for password manager old
    elif(isSubStringsNoCase(command , "password")):
        objPasswordStorerClass = PasswordStorerClass()
        objPasswordStorerClass.driverFunc()
        return True

    


    # handling cmd commands
    elif(isSubStringsNoCase(command , "start cmd")):
        customClearScreen()
        print("opening jarvis in command prompt")
        try:
            os.startfile(r"jarvis_CMD.bat")
        except FileNotFoundError:
            customClearScreen()
            print("cmd bat file not found, please try reinstalling the software or contact developer")
            return True
            
        print("\njarvis opened in command prompt")
        print("\nExisting this instance of jarvis")
        time.sleep(1)
        sys.exit()


    # process for stoping file share
    elif(isSubStringsNoCase(command , "stop file")):
        customClearScreen()
        # try:
        if(GlobalData_main.fileShareObj == None):
            print("File sharing is not currently active")
            return True
        
        GlobalData_main.fileShareObj.stopFileShare()

        for i in GlobalData_main.threadOpenedList:
            if(isSubStringsNoCase(i , "file sharing")):
                GlobalData_main.threadOpenedList.remove(i)
                break

        print("file sharing stopped successfully")
        return True

        # except Exception as e:
        #     print("could not stop file share , if the error persist , run the troubleshoot command")
        #     cLog.log("error on stop file share execute command in main.py", "e")
        #     cLog.exception(str(e), "In stop file share function main.py")
        #     return True


    # process for starting file share
    elif(isSubStringsNoCase(command , "start file")):
            
        folderShare = ""
        
        customClearScreen()
        print("select the folder from the pop window to share")
        
        try:    
            # folderShare = get_folderPath_fromFileExplorer()
            folderShare = r"C:/Users/harsh/desktop"
            # folderShare = r"F:\Etc"
            
        except Exception:
            print("could not start the file explorer , enter the path manually\n")
            
            while(1):

                folderShare = input("Enter the folder path to share or enter 0 to quit : ")

                if(path.exists(str(folderShare)) == True):
                    break

                elif(folderShare == "0"):
                    return True

                else:
                    customClearScreen()
                    print("system could find the entered path, please try again or enter 0 to quit")
                    print("\n\n")
                    input("press enter to continue ...")

            print("\n\n")
            input("press enter to continue...")

        
        # try:
        customClearScreen()

        GlobalData_main.fileShareObj = FS.FileShareClass()
        # stoping the loading animation
        changeRunLoadingAnimation()
        lAnimation.join() 

        returned = []

        if(isSubStringsNoCase(command , "2")):
            returned = GlobalData_main.fileShareObj.start_fileShare(str(folderShare) , http = True)
            toAppend = "File sharing is currently active at http://" + str(GlobalData_main.fileShareObj.get_ip_address()) + ":8000"
            
            GlobalData_main.threadOpenedList.append(toAppend)
        else:
            returned = GlobalData_main.fileShareObj.start_fileShare(str(folderShare) , http = False)
            
            toAppend = "File sharing is currently active at ftp://" + str(GlobalData_main.fileShareObj.get_ip_address()) + ":8000"
            GlobalData_main.threadOpenedList.append(toAppend)
            toAppend = "And at ftp://user:225588@" + str(GlobalData_main.fileShareObj.get_ip_address()) + ":8000"
            GlobalData_main.threadOpenedList.append(toAppend)

        for i in returned:
            print("\n" , i )


        # except Exception as e:
        #     print("could not start file share , make sure you are connected to the internet .\nif the error persist run the troubleshoot command ")
        #     cLog.log("error on handle file share function in main.py", "e")
        #     cLog.exception(str(e), "In handleFileShare function main.py")

        return True



    # handling utc time and date
    elif(isSubStringsNoCase(command , "utc time")):
        newObj = str(datetime.datetime.utcnow())
        currentDate = newObj[8:10] + "/" + newObj[5:7] + "/" + newObj[:4]
        currentTime = newObj[11:19] 

        customClearScreen()

        print("UTC TIME = {}".format(currentTime))
        print("UTC DATE = {}".format(currentDate))
        return True

    # handling simple time command
    elif(isSubStringsNoCase(command , "time")):
        newObj = str(datetime.datetime.now())
        currentDate = newObj[8:10] + "/" + newObj[5:7] + "/" + newObj[:4]
        currentTime = newObj[11:19] 

        customClearScreen()

        print("TIME = {}".format(currentTime))
        print("DATE = {}".format(currentDate))
        return True

    # handling font size command
    elif(isSubStringsNoCase(command , "font size")):
        customClearScreen()
        if(GlobalData_main.isOnLinux):
            print("Only for windows users :(")
            return True
            

        print("To change the font size follow these steps : ") 
        print("\n1. right click on the jarvis logo on top left corner")
        print("\n2. click on the defaults button")
        print("\n3. navigate to font panel and change the font size")
        print("\n4. restart the program by closing it")
        print("\nRecommended font size is 18")
        print("\nTo change the font size temporarily - click on properties instead of defaults")
        return True

    # handling font colour command
    elif(isSubStringsNoCase(command , "font col")):
        customClearScreen()
        if(GlobalData_main.isOnLinux):
            print("Only for windows users :(")
            return True

        print("To change the font colour follow these steps : ") 
        print("\n1. right click on the jarvis logo on top left corner")
        print("\n2. click on the defaults button")
        print("\n3. navigate to colours panel and make sure screen text is selected")
        print("\n4. select the colour and restart the program by closing it")
        print("\nRecommended font colour is green or grey")
        print("\nTo change the font size temporarily - click on properties instead of defaults")
        return True
    
    # handling speed test command
    elif(isSubStringsNoCase(command , "speed test")):
        commandList = command.split()
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
        objSpeedTestClass = SpeedTestClass(GlobalData_main.troubleShootValue)

        # calling method of class for execution
        objSpeedTestClass.runSpeedTestUtility(inBytes , numberOfTime)
        return True     # as all runned successfully

    # handling troubleshoot command
    elif(isSubStringsNoCase(command , "trouble")):
        status = troubleShootFunc()

        customClearScreen()

        if(status == True):
            print("Trouble shooting complete, don't forget to mail us the log file at myjarvispa@gmail.com")
        else:
            print("toubleshooting stopped in between")
        return True

    # calling for exit command
    elif(isSubStringsNoCase(command , "exit") or isSubStringsNoCase(command , "bye")):

        if(not(GlobalData_main.directRunFromCmd)):
            customClearScreen()
            print("existing the program , please wait ...")

        # terminating the file share threading
        try:
            if(GlobalData_main.fileShareObj == None):
                pass
            else:
                GlobalData_main.fileShareObj.stopFileShare()

        except Exception as e:
            print("could not exit the program , please stop the file sharing first using stop file share command")
            cLog.log("error on stop file share execute command in main.py", "e")
            cLog.exception(str(e), "In  exit function main.py")
            return True
        
        if(not(GlobalData_main.directRunFromCmd)):
            customClearScreen()

        sys.exit()

    # if none of the above command is executed than return false to tell the user that the command entered was incorrect
    return False


def main():

    # setting api key's

    # for weather module - get your api key from open weather and pass it here
    WeatherData.setApiKey("")

    # checking the api key's
    if(WeatherData.returnApiKeyStatus() == False):
        raise NotImplementedError("Set the open weather api")
    
    # setting trouble shoot value
    cLog.setTroubleShoot(GlobalData_main.troubleShootValue)

    objMainClass = MainClass()

    dictFromMainClass = objMainClass.returnDict()

    try:
        if(dictFromMainClass["makeKeyBoardSound"] == "true"):
            GlobalData_main.toMakeTypingSound = True
    except Exception as e:
        cLog.log("error on getting value of makeKeyBoardSound from dictionary in main function in main.py", "e")
        cLog.exception(str(e), "In getting value of makeKeyBoardSound from dictionary in main function main.py")

    while(1):


        if(GlobalData_main.directRunFromCmd):
            commandListFromCmd = sys.argv

            # deleting first argument
            trimmedCommandListFromCmd = commandListFromCmd[1:]

            # generating string from list arguments
            seperator = " "
            commandString = seperator.join(trimmedCommandListFromCmd)

            if(handleGetHelp(commandString)):
                pass
            else:
                if(executeCommands(commandString)):
                    pass
                else:
                    customClearScreen()

                    print("oops could not regonise the command try typing help for info")

            print("\n\n")
            executeCommands("exit")

        else:

            objMainClass.setUserName()

            customClearScreen()

            # printing details for currently running threads in background
            if(len(GlobalData_main.threadOpenedList) > 0):
                for i in GlobalData_main.threadOpenedList:
                    print(i)

                print("\n") 
            

            print(f"Welcome {objMainClass.returnUserName()}\n")
            commandInput = input("Enter Command : ")
                    
            if(handleGetHelp(commandInput)):
                pass
            else:
                if(executeCommands(commandInput)):
                    pass
                else:
                    customClearScreen()

                    print("oops could not regonise the command try typing help for info")

            print("\n\n")
            input("press enter to continue...")


def driverForMain():

    # calling main
    main()


if __name__ == "__main__":
    
    # stoping the loading animation
    changeRunLoadingAnimation()
    lAnimation.join() 

    # playing the starting sound
    startingSoundObj = startingSound()
    objMainClass = MainClass()

    dictFromMainClass = objMainClass.returnDict()

    # sound will not play if the jarvis is runned by cmd arguments
    if(not(GlobalData_main.directRunFromCmd)):
        if(dictFromMainClass["makeStartSound"] == "true"):
            startingSoundObj.start()

    # checking if in developer mode
    if(GlobalData_main.troubleShootValue):
        print("\nIn dev mode\n")
        time.sleep(0.5)

    print("\n")

    customClearScreen()

    driverForMain()
