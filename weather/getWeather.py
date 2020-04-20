import requests
import json

""" this is using the open weather api """

def makeUrl(apiId , cityName):
    stringKey = "https://api.openweathermap.org/data/2.5/weather?q="
    stringKey = stringKey + str(cityName) + "&appid=" + str(apiId)
    return stringKey


def getDataFromWeb(url):
    try:
        data = requests.get(url).text
        return data
    except Exception:
        return False


def loadDataIntoJson(data):
    if data == False:
        return False
    else:
        j = json.loads(data)
        return j


def extractInfo(listPass , jsonData):
    """ the list is passed containing exact name of which the information will be returned 
        , if the listElement is not in the Json file Then a False Bool value is added to list in its place"""

    """ these are the elements that can be found 
    temp	:	280.32
    pressure	:	1012
    humidity	:	81
    temp_min	:	279.15
    temp_max	:	281.15
    visibility	:	10000"""

    resultList = []

    for i in listPass:
        if(jsonData == False):
            resultList.append(False)
        else:
            try:
                resultList.append(jsonData["main"][str(i)])
            except KeyError:
                resultList.append(False)

    return resultList
        

# driver code for test run
if __name__ == "__main__":
    url = makeUrl("fe82651e607e46db61dba45e39aa7e17", "london")

    apiData = getDataFromWeb(url)

    jData = loadDataIntoJson(apiData)

    myList = [ "temp" ,
               "pressure" , 
               "humidity" , "hello" ]

    result = extractInfo(myList , jData)

    print(result)


