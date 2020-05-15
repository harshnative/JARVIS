import os
import time

class Setting():

    # constructor
    def __init__(self):
        self.myDictionary = { }


    # method for making dictionary by reading the txt file
    def makeDictionaryFromTxt(self):

        try:
            # opening the txt file
            with open(r"C:\programData\Jarvis\settings.txt" , "r+") as fil:

                
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
                            # print(newSplitedList)
                            # print(newSplitedList[0], newSplitedList[1])
                            # adding to dictionary
                            self.myDictionary[str(newSplitedList[0])] = str(newSplitedList[1])
                            
                    except Exception:
                        pass

        except FileNotFoundError:
            os.system("cls")
            print("something went wrong in settings module")
            time.sleep(1)
            exit()


    # function to return the dictionary
    def getDictionary(self):
        self.makeDictionaryFromTxt()
        return self.myDictionary


    # function to regenerate the deleted settings file
    def regenerateFile(self):
        try:
            fil = open("C:/programData/Jarvis/settings.txt" , "w+")
            fil.write("# Your defualt city\n")
            fil.write("City = london\n\n")

            fil.write("# Directories of backup - seperated by comma's in "" - ex - D:/myfiles/images , E:/data/documents\n")
            fil.write("Directories = \n\n")

            fil.write("# path to backup - ex - F:/myBackup\n")
            fil.write("backUpPath = \n\n")

            fil.write("# User Name :\n")
            fil.write("userName = \n\n")

            fil.write("# Greeting :\n")
            fil.write("greeting = Welcome\n\n")

            fil.close()
            return True
            
        except Exception:
        	os.system("cls")
        	print("Jarvis do not have write permission in this folder")
        	os.system("pause")
        	os.system("cls")
        	return False


    # funnction to open the settings file in default txt viewer
    def openFile(self):
        try:
            os.startfile(r"C:\programData\Jarvis\settings.txt")
        except FileNotFoundError:
            os.system("cls")
            print("Generating Settings File")
            generateStatus = self.regenerateFile()
            time.sleep(0.3)
            print("." , end="" , flush=True)
            time.sleep(0.4)
            print("." , end="" , flush=True)
            time.sleep(0.5)
            print("." , end="" , flush=True)
            if(generateStatus == True):
                print("\nFile Generated Sucessfully")
                print("\nOpening File.....")
                os.startfile(r"C:\programData\Jarvis\settings.txt")
                time.sleep(2)
                os.system("cls")
                
            elif(generateStatus == False):
                print("\nError Occured\n")
                os.system("cls")
            
# driver code - only for testing purpose
if __name__ == "__main__":
    obj = Setting()
    print(obj.makeDictionaryFromTxt())