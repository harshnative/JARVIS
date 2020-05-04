# importing modules
from packages.backUp_utility.backUp import *
from packages.weather.getWeather import *
from packages.settings.jarvisSetting import *
from imports.harshNative_github.hangMan_game.hangmanGame import *
from imports.harshNative_github.txtCompare.txtComparePy import *
from imports.harshNative_github.googleDrive.googleDriveLinkPy import *
import os
from tabulate import tabulate
import sys
import psutil
import logging
import pyperclip
import time


# outsourced function 
def restart_program():
    os.system("cls")
    main()


# function to check for a substring in a string - returns true or false
def isSubString(string , subString):
    lengthOfSubString = len(subString)
    for i,j in enumerate(string):
        if(j == subString[0]):
            if(subString == string[i:i+lengthOfSubString]):
                return True 
            else:
                pass
    return False


# function for displaying help
def getHelp(passObj):

    # for displaying all the help available
    if(passObj == "all"):
        os.system("cls")
        try:
            with open("txtFiles/help.txt") as fil:
                for line in fil:
                    print(line)
        except FileNotFoundError:
            print("oops , the help file in missing , visit the website for help")
        
        print("\n\n")
        os.system("pause")
    
    # for displaying specific help by searching for the keyords as substring in line
    else:
        os.system("cls")
        try:
            count = 0
            with open("txtFiles/help.txt") as fil:
                for line in fil:
                    for i in passObj:
                        if(isSubString(line , i)):
                            print(line)
                            count += 1
                if(count == 0):
                    print("oops no help found , try writting only help for seeing all help available")
        except FileNotFoundError:
            print("oops , the help file in missing , visit the website for help")
            
        print("\n\n")


# function for handling the get help
def handleGetHelp(command):
    commandList = command.split()
    # for getting the help - all - or specific things
    if(("help" in commandList) or ("Help" in commandList)):
        if(("open" in commandList) or ("Open" in commandList)):
            try:
                os.startfile('help.txt')
            except FileNotFoundError:
                print("oops the help.txt is missing , visit website for help")
            return True

        elif(len(commandList) > 1):
            getHelp(commandList)
            return True

        else:
            getHelp("all")
            return True

        return False


class mainClass():

    # contructor
    def __init__(self):
        self.settingsDict = {}
        self.getDict()
    
    # function to get the Dictionary from the settings module
    def getDict(self):
       objSetting = setting()
       self.settingsDict = objSetting.getDictionary()
    
    def setUserName(self):
        temp = os.environ # generates a object with the property called USERNAME containing the info
        tempUserName = temp["USERNAME"]
        try:
            if(self.settingsDict["userName"] == ""):
                self.settingsDict["userName"] = tempUserName        
        except KeyError:
            self.settingsDict["userName"] = tempUserName

    def returnUserName(self):
        return self.settingsDict["userName"]

class mainWeatherClass(mainClass):

    # constructor
    def __init__(self):
        self.cityName = None
        self.weatherArgumentList = ["tempInC" , "pressure" , "humidity"]
    

    # function to set the cityName
    def getCityName(self , cityPass):
        self.cityName = cityPass


    # function to add another elements to list to get their info as well
    def addToList(self , element):
        self.weatherArgumentList.append(element)


    # function to print the weather details
    def printWeatherDetails(self):
        self.getDict()
        # if the cityName is not passed then we will take it from dictionary generated from settings app
        if(self.cityName == None):
            self.cityName = self.settingsDict["City"]
        
        # making a object of weather data class
        objGetWeatherData = weatherData()

        # getting the result
        result = objGetWeatherData.getWeatherData(self.cityName , self.weatherArgumentList)
        
        #showing the result in tabular form
        os.system("cls")
        print(f"weather details of {self.cityName} are - \n")
        tabulateList = []
        errorYES = False
        for i,j in zip(self.weatherArgumentList , result):
            tempList = []
            if ((i == None) or (j == None)):
                errorYES = True
            else:
                i = str(i)
                j = int(j)
                tempList.append(i)
                tempList.append(j)
                tabulateList.append(tempList)
        if (errorYES):
            print("error while getting wheather details")
        else:
            print(tabulate(tabulateList, headers=['Query', 'Data']))
        


# function to execute the passed command by analysing it
def executeCommands(command):
    # spliting with " " to form a command list
    commandList = command.split()
    # checking for weather commands
    if(("weather" in commandList) or ("Weather" in commandList)):

        # creating object of main weather class
        objMainWeatherClass = mainWeatherClass()

        # looping through command list to get the cityname if present 
        for com in commandList:

            # getting the city name - as to be city-cityName
            if(isSubString(str(command) , "city")):
                for i,j in enumerate(com):
                    if(j == "c"):
                        if(com[i:i+4] == "city"):
                            cityName = com[i+5:]
                            cityNameEdit = ""
                            for i,j in enumerate(cityName):
                                if(j == "_"):
                                    cityNameEdit = cityName[:i] + " " + cityName[i+1:]
                            if(cityNameEdit == ""):
                                pass
                            else:
                                cityName = cityNameEdit

            else:
                cityName = None

        # passing the city name to the class
        objMainWeatherClass.getCityName(cityName)

        # checking for additional commands 
        if("-f" in commandList or "-F" in commandList):
            objMainWeatherClass.addToList("tempInF")
        
        # executing the command
        objMainWeatherClass.printWeatherDetails()

        return True
    
    # for restoring the defualt setting
    elif(("restore" in commandList) or ("Restore" in commandList)):
        objSetting = setting()
        objSetting.regenerateFile()
        os.system("cls")
        print("you have restored the settings successfully")
        return True

    # for changing teh setting - this function opens the settings.txt in the defualt txt viewer of the system
    elif(("Change" in commandList) or ("change" in commandList)):
        if(("Setting" in commandList) or ("setting" in commandList) or ("Settings" in commandList) or ("settings" in commandList)):
            objSetting = setting()
            objSetting.openFile()
            os.system("cls")
            print("the settings file is opened")
            return True
        
        # as you can change settings only
        else:
            return False

    # function for updating the settings
    elif(("update" in commandList) or ("Update" in commandList)):
        os.system("cls")
        print("settings have been updated , programm will restart now\n\n")
        os.system("pause")
        restart_program()
        return False

    # calling for backup command
    elif(("backup" in commandList) or ("Backup" in commandList)):

        # creating a copy of backup command without the backup keyword so that we can pass it to the startBackup function of the class backUp
        commandListCopy = commandList.copy()
        if("backup" in commandList):
            commandListCopy.remove("backup")
        elif("Backup" in commandList):
            commandListCopy.remove("Backup")

        # creating object of class backUp
        objBackUp = backUp()

        # creating object of class setting
        objSetting = setting()

        # creating some required assets
        directoriesListEditted = []
        dictionaryFromSetting = objSetting.getDictionary()

        # checking if -d is in command
        if("-d" in commandList):
            if(dictionaryFromSetting["backUpPath"] == ""):
                os.system("cls")
                print("it looks like you have not added any folder's to backup in setting file")
                print("\n\ntype change settings in the command to open the file and then run update command")
                print("\n\ntype help settings for additional help")
                return True
            else:
                pathToBackup = str(dictionaryFromSetting["backUpPath"])
                try:
                    os.mkdir(pathToBackup + "/" + "jarvisBackup")
                    pathToBackup = pathToBackup + "/" + "jarvisBackup"
                except OSError:
                    os.system("cls")
                    pathToBackup = pathToBackup + "/" + "jarvisBackup"
                    print("folder in path to backup in settings already exit or may be the path is not found")
                    print("\n\nif the folder already exit - then all the file's will be overRidden")
                    print("\n\npress enter to continue with backup or close the program to stop it")
                    input()
                    os.system("cls")

            # if backup path is correct then if need to ckeck if the directories are listed in setting's file or not 
            if(dictionaryFromSetting["Directories"] == ""):
                os.system("cls")
                print("it looks like you have not added any folder's to directories in setting file")
                print("\n\ntype change settings in the command to open the file and then run update command")
                print("\n\ntype help settings for additional help")
                return True
            else:
                directoriesGenerated = str(dictionaryFromSetting["Directories"])
                directoriesList = directoriesGenerated.split(",")
                
                # created a list of directories to pass on to the function startbackup of class backup
                for i in directoriesList:
                    i = i.strip()
                    directoriesListEditted.append(i)

        # calling the function to start the copy process
        os.system("cls")
        print("\nBackUp in process - This may take several minutes....")
        print("\nplease do not close the program , otherWise files may get corrupted")
        objBackUp.startBackUp(commandListCopy , directoriesListEditted , pathToBackup + "/")
        os.system("cls")
        print("\n\nCopy completed\nlog file is generated at the desktop , their may me some files that may not have been copied due to permission errors :(")
        return  True

    # calling for hangman game
    elif(("hangman" in commandList) or ("Hangman" in commandList)):
        if(("game" in commandList) or ("Game" in commandList)):
            os.system("cls")
            #calling the game function 
            boolValue = mainForHangmanGame()
            os.system("cls")
            if(boolValue == True):
                print("thanks for playing game")
            else:
                print("some error ocurred :( , visit website for more info")

            return True
        else:
            return False

    # calling for txt compare
    elif(("compare" in commandList) or ("Compare" in commandList)):
        if(("txt" in commandList) or ("Txt" in commandList) or ("TXT" in commandList)):
            os.system("cls")
            print("starting txtCompare program :)\n\n")
            mainForTxtCompare()
            return True
        else:
            return False

    # calling for google drive link
    elif(("google" in commandList) or ("Google" in commandList)):
        if(("drive" in commandList) or ("Drive" in commandList)):
            os.system("cls")
            print("Go to the file saved in google drive and click get shareable link\n")
            linkGet = input("Paste the link here : ")
            linkFinal = mainForGoogleDriveLink(linkGet)
            if(linkFinal == False):
                print("\n\nThe link is in valid :(")
                return True
            else:
                pyperclip.copy(str(linkFinal))
                pyperclip.paste()
                print("\n\nThe link is {} and is been copied to clipboard :)".format(linkFinal))
                return True

    # calling for random generator
    elif(("generate" in commandList) or ("Generate" in commandList)):
        if(("random" in commandList) or ("Random" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\anyRandom.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                print("This is the minimal version, download complete version for this functionality :)")
            return True
        else:
            return False

    # calling for number system convertor
    elif(("number" in commandList) or ("Number" in commandList) or ("num" in commandList) or ("Num" in commandList) or ("no" in commandList) or ("No" in commandList) or ("NO" in commandList)):
        if(("convert" in commandList) or ("conv" in commandList) or ("convertor" in commandList) or ("Convert" in commandList) or ("Conv" in commandList) or ("Convertor" in commandList)):
            if(("system" in commandList) or ("sys" in commandList) or ("System" in commandList) or ("Sys" in commandList)):
                os.system("cls")
                try:
                    os.startfile(r"external_exe\harshNative_github\NSC.exe")
                    print("The file is opened in other window :)")
                except FileNotFoundError:
                    print("This is the minimal version, download complete version for this functionality :)")
                return True
            else:
                return False
        else:
            return False

    # calling for average finder
    elif(("average" in commandList) or ("Average" in commandList) or ("avg" in commandList) or ("Avg" in commandList) or ("AVG" in commandList)):
        os.system("cls")
        try:
            os.startfile(r"external_exe\harshNative_github\average_finder.exe")
            print("The file is opened in other window :)")
        except FileNotFoundError:
            print("This is the minimal version, download complete version for this functionality :)")
        return True

    # calling for coin toss
    elif(("Coin" in commandList) or ("coin" in commandList)):
        if(("toss" in commandList) or ("Toss" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\coin_toss.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                print("This is the minimal version, download complete version for this functionality :)")
            return True
        else:
            return False

    # calling for group generator
    elif(("group" in commandList) or ("Group" in commandList)):
        if(("generate" in commandList) or ("Generate" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\group_Generator.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                print("This is the minimal version, download complete version for this functionality :)")
            return True
        else:
            return False

    # calling for interest calculator 
    elif(("calculator" in commandList) or ("Calculator" in commandList) or ("calc" in commandList) or ("Calc" in commandList)):
        if(("Interest" in commandList) or ("interest" in commandList)):
            os.system("cls")
            try:
                os.startfile(r"external_exe\harshNative_github\interest_Calculator.exe")
                print("The file is opened in other window :)")
            except FileNotFoundError:
                print("This is the minimal version, download complete version for this functionality :)")
            return True
        else:
            return False

    # calling for exit command
	elif(("exit" in commandList) or ("EXIT" in commandList) or ("Exit" in commandList)):
		print("Exiting the program" , end="")
		time.sleep(0.3)
		print("." , end="")
		time.sleep(0.3)
		print("." , end="")
		time.sleep(0.3)
		print("." , end="")
		exit()

    else:
        return False

def main():
    objMainClass = mainClass()
    while(1):
        objMainClass.setUserName()
        os.system("cls")
        print(f"welcome {objMainClass.returnUserName()}\n")
        commandInput = input("enter command : ")
        if(commandInput == "exit" or commandInput == "Exit" or commandInput == "EXIT"):
            break
        elif(handleGetHelp(commandInput)):
            pass
        else:
            if(executeCommands(commandInput)):
                pass
            else:
                os.system("cls")
                print("oops could not regonise the command try typing help for info")

        print("\n\n")
        os.system("pause")


if __name__ == "__main__":
    main()
