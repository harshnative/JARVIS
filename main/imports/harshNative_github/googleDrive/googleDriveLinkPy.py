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

