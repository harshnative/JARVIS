isOnWindows = False
isOnLinux = False
import os

# Checking weather the user is on windows or not
try:
    temp = os.environ
    tempUserName = temp["USERNAME"]
    isOnWindows = True
except Exception:
    isOnLinux = True
    
import subprocess as sp

def customClearScreen():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)


def mainForGoogleDriveLink(stringPassed):

    inputString = stringPassed

    trimmedString = inputString[32:]

    print(trimmedString)

    try:
        string , d = trimmedString.split('/')
    except ValueError:
        return False
        
    preString = "https://drive.google.com/uc?export=download&id="

    downloadableLink = preString + string

    return downloadableLink


if __name__ == "__main__":
    driverFunc()

