import requests
import json

""" this is using the open weather api """

class weatherData():

    # building up constructor to set the defualt value's
    def __init__(self):
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
        except Exception:
            pass    # since the defualt value of the data is already None


    # function to convert the data from the web to json format
    def loadDataIntoJson(self):
        if self.data == None:
            pass
        else:
            self.jsonData = json.loads(self.data)


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

        for i in self.listPassed:
            if(self.jsonData == None):
                self.resultList.append(None)
            elif(i == "tempInC"):
                self.resultList.append(self.tempInC)
            elif(i == "tempInF"):
                self.resultList.append(self.tempInF)
            else:
                try:
                    self.resultList.append(self.jsonData["main"][str(i)])
                except KeyError:
                    self.resultList.append(None)

    
    # function to convert the json temp which is in kelvin to 'c
    def convTempToC(self):
        try:
            self.tempInK = self.jsonData["main"]["temp"]
        except KeyError:
            print("error while getting weather details")
        self.tempInC = self.tempInK - 273


    # function to convert the 'C to 'F
    def convTempToF(self):
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
        self.convTempToC()
        self.convTempToF()
        self.extractInfo()
        return self.resultList
   

# driver code for test run
if __name__ == "__main__":
    
    obj = weatherData()
    myList = [ "tempInC" ,
               "pressure" , 
               "humidity" , "hello" ]

    print(obj.getWeatherData("delhi" , myList))



