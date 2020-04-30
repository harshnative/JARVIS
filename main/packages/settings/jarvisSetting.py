import os

class setting():

    # constructor
    def __init__(self):
        self.myDictionary = {}


    # method for making dictionary by reading the txt file
    def makeDictionaryFromTxt(self):

        try:
            # opening the txt file
            with open("txtFiles/settings.txt" , "r+") as fil:

                # reading line by line
                for line in fil:
                    line = line.strip()
                    line = str(line)

                    # try block for empty lines
                    try:
                        if(line[0] == "#"): # as it is a comment
                            pass
                        elif(line[0] == " " or line[0] == ""):
                            pass
                        else :
                            splitedList = line.split("=")
                            newSplitedList = []

                            for i in splitedList:
                                i = i.strip()
                                newSplitedList.append(i)
                            
                            # adding to dictionary
                            self.myDictionary[newSplitedList[0]] = newSplitedList[1]
                    except Exception:
                        pass

        except FileNotFoundError:
            self.regenerateFile()


    # function to return the dictionary
    def getDictionary(self):
        self.makeDictionaryFromTxt()
        return self.myDictionary


    # function to regenerate the deleted settings file
    def regenerateFile(self):
        with open("txtFiles/settings.txt" , "w+") as fil:
            fil.write("# your defualt city\n")
            fil.write("City : london\n\n")

            fil.write("# font size\n")
            fil.write("Font Size : 24\n\n")

            fil.write("# Directories of backup - seperated by comma's in "" - ex - D:/myfiles/images , E:/data/documents\n")
            fil.write("Directories : \n\n")

            fil.write("# user Name :\n")
            fil.write("userName : \n\n")

            fil.write("# greeting :\n")
            fil.write("greeting : Welcome\n\n")


    # funnction to open the settings file in default txt viewer
    def openFile(self):
        try:
            os.startfile('settings.txt')
        except FileNotFoundError:
            self.regenerateFile()
            os.startfile('settings.txt')

    
# driver code - only for testing purpose
if __name__ == "__main__":
    obj = setting()
    obj.makeDictionaryFromTxt()