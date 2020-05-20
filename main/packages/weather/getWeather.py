import requests
import json
import logging
import os
from packages.loggerPackage.loggerFile import *
""" this is using the open weather api """

class WeatherData():

    # building up constructor to set the defualt value's
    def __init__(self , troubleShootValuePass):

        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)

        self._apiKey = "fe82651e607e46db61dba45e39aa7e17"
        self.cityName = "london"
        self.stringKey = "https://api.openweathermap.org/data/2.5/weather?q="
        self.data = None
        self.jsonData = None
        self.resultList = []
        self.listPass = []
        self.tempInK = 273
        self.tempInC = 0
        self.tempInF = 0


    # function to set the cityName for which the weather data will be pulled
    def giveCityName(self , cityNamePassed):
        self.cityName = str(cityNamePassed)


    # function to make the final url which will be used to make request
    def makeUrl(self):  
        self.stringKey = self.stringKey + self.cityName + "&appid=" + self._apiKey


    # function to get the weather data from the open weather server
    def getDataFromWeb(self):
        try:
            self.data = requests.get(self.stringKey).text
            self.cLog.log("getDataFromWeb runned successfully" , "i")
        except Exception as e:
            self.cLog.log("cannot make request in getDataFromWeb" , "w")
            self.cLog.exception(str(e) , "In getWeather.py/WeatherData_class-getDataFromWeb")
            # just logging the exception because defualt value of self.data is None


    # function to convert the data from the web to json format
    def loadDataIntoJson(self):
        if self.data == None:
            # just pass as by default json data is also none
            pass
        else:
            self.jsonData = json.loads(self.data)
            self.cLog.log("loadDataIntoJson runned successfully" , "i")


    # function to read the list of infomation need and append the result to resultList by getting the values from the json
    # read the function docs for getting the info on listPassing
    def extractInfo(self):
        """ the list is passed containing exact name of which the information will be returned 
            , if the listElement is not in the Json file Then a None value is added to list in its place"""

        """ these are the elements that can be found 
        temp	:	280.32
        pressure	:	1012
        humidity	:	81
        temp_min	:	279.15
        temp_max	:	281.15
        visibility	:	10000
        tempInC : get the temp in celcius
        tempInF : get the temp in faraniet """
        
        cCount = 0
        fCount = 0
        for i in self.listPassed:
            if(self.jsonData == None):
                self.resultList.append(None)
            elif(i == "tempInC"):
                self.resultList.append(self.tempInC)
                cCount += 1
            elif(i == "tempInF"):
                self.resultList.append(self.tempInF)
                fCount += 1
            else:
                try:
                    toappend = self.jsonData["main"][str(i)]
                    # checking to convertor temp min and mac to c or f as required
                    if(str(i) == "temp_min" or str(i) == "temp_max"):
                        if(cCount > 0):
                            toappend = self.convTempToC(float(toappend))
                        elif(fCount > 0):
                            toappend = self.convTempToC(float(toappend))
                            toappend = self.convTempToF(float(toappend))

                    self.resultList.append(str(toappend))
                except KeyError:
                    self.cLog.log("key error in extractInfo function - self.jsonData[main][str(i)]" , "i")
                    self.resultList.append(None)
                except Exception as e:
                    os.system("cls")
                    self.cLog.log("critical error in extract info function" , "e")
                    self.cLog.exception(str(e) , "In getWeather.py/WeatherData_class-extractInfo_func")
                    print("something went wrong , try again.\n\n")
                    print("if the error remains follow instructions : ")
                    print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
                    print("step 2 - {}".format(self.cLog.getLogFileMessage))
        return True
    
    # function to convert the json temp which is in kelvin to 'c
    def getTempInC(self):
        try:
            self.tempInK = self.jsonData["main"]["temp"]
        except KeyError:
            self.tempInK = None
            return False
        except Exception as e:
            os.system("cls")
            self.cLog.log("error while opening the help file" , "e")
            self.cLog.exception(str(e) , "In getWeather.py/WeatherData_class-convTempToC_func")
            print("something went wrong , try again.\n\n")
            print("if the error remains follow instructions : ")
            print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
            print("step 2 - {}".format(self.cLog.getLogFileMessage))
        self.tempInC = self.tempInK - 273
        return True
    
    def convTempToC(self , tempInKPass):
        return (tempInKPass - 273)
    
    def convTempToF(self , tempInCPass):
        return (( tempInCPass * (9/5) ) + 32)


    # function to convert the 'C to 'F
    def getTempInF(self):
        if(self.tempInC == None):
            self.tempInF = None
            self.cLog.log("temp in c was none in getTempInF in weather Data class in get weather.py" , "e")
        else:
            self.tempInF = ( self.tempInC * (9/5) ) + 32


    # function that the user will be using to get the data
    # function to do all the above stuff line wise 
    def getWeatherData(self , give_cityName , give_listOfValueToGet):
        """Read the extractInfo() docs to get info on give_listOfValueToGet and the info on the things that are returned in list"""
        self.listPassed = give_listOfValueToGet
        self.giveCityName(give_cityName)
        self.makeUrl()
        self.getDataFromWeb()
        self.loadDataIntoJson()
        self.getTempInC()
        self.getTempInF()
        self.cLog.log("runned till get temp in F in getweather data in weather data class in get weather.py" , "i")
        status = self.extractInfo()

        if(status == False):
            self.cLog.log("weather module failed to work properly" , "i")
            return self.resultList
        else:
            return self.resultList
   

# driver code for test run
if __name__ == "__main__":
    
    obj = WeatherData()
    myList = [ "tempInC" ,
               "pressure" , 
               "humidity" , "hello" ]

    print(obj.getWeatherData("delhi" , myList))



