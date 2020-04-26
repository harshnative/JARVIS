# importing modules
from packages.backUp_utility.backUp import *
from packages.weather.getWeather import *
from packages.settings.jarvisSetting import *
import os
from tabulate import tabulate
import sys
import psutil
import logging


# outsourced function 
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception:
        pass

    python = sys.executable
    os.execl(python, python, *sys.argv)


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
            with open("help.txt") as fil:
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
            with open("help.txt") as fil:
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
        for i,j in zip(self.weatherArgumentList , result):
            tempList = []
            i = str(i)
            j = int(j)
            tempList.append(i)
            tempList.append(j)
            tabulateList.append(tempList)
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

# TODO : integrate the backup system and build a exe file for publishing

if __name__ == "__main__":
    main()
