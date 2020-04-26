# importing modules
from packages.backUp_utility.backUp import *
from packages.weather.getWeather import *
from packages.settings.jarvisSetting import *
import os
from tabulate import tabulate



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
        if(self.settingsDict["userName"] == ""):
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
        print("\n")
        


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
    else:
        return False

def main():
    objMainClass = mainClass()
    objMainClass.setUserName()
    while(1):
        os.system("cls")
        print(f"welcome {objMainClass.returnUserName()}\n")
        commandInput = input("enter command : ")
        if(commandInput == "exit" or commandInput == "Exit" or commandInput == "EXIT"):
            break
        elif(commandInput == "help" or commandInput == "Help" or commandInput == "HELP"):
            os.system("cls")
        else:
            if(executeCommands(commandInput)):
                pass
            else:
                print("oops could not regonise the command try typing help for info")

        os.system("pause")

# weather city-panipat
# TODO : add help and what happens when the settings file is missing

if __name__ == "__main__":
    main()
