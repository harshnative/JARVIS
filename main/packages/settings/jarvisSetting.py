import os
import time
from packages.loggerPackage.loggerFile import *

class Setting():

    # constructor
    def __init__(self , troubleShootValuePass):
        self.myDictionary = { }
        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)


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

                            # adding to dictionary
                            self.myDictionary[str(newSplitedList[0])] = str(newSplitedList[1])
                    
                            
                    except Exception:
                        # sometimes accessing line[0] throws error , but we don't need to deal with it so just pass in exception
                        pass
            
            # returning true if everything went right
            return True

        except FileNotFoundError:
            os.system("cls")
            print("settings file cannot be found , try restarting or reinstalling the program , or go to website for help")
            return False

        except Exception as e:
            os.system("cls")
            self.cLog.log("error while opening the help file" , "e")
            self.cLog.exception(str(e) , "In jarvisSetting.py/makeDictionaryFromTxt_func")
            print("something went wrong , try again.\n\n")
            print("if the error remains follow instructions : ")
            print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
            print("step 2 - {}".format(self.cLog.getLogFileMessage))
            return False



    # function to return the dictionary
    def getDictionary(self):
        status = self.makeDictionaryFromTxt()
        if(status == False):
            return False
        else:
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
            print("It seems like Jarvis do not have write permission in this folder")
            print("try reinstalling the program with administrative premission\n")
            print("if the error remains follow instructions : ")
            print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
            print("step 2 - {}\n\n".format(self.cLog.getLogFileMessage))
            os.system("pause")
            os.system("cls")
            return False


    # funnction to open the settings file in default txt viewer
    def openFile(self):
        try:
            os.startfile(r"C:\programData\Jarvis\settings.txt")
            return True
        except FileNotFoundError:
            os.system("cls")
            self.cLog.log("error opening settings file as it was not present" , "e")
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
                self.cLog.log("Previous error may be solved becuase the settings file was generated successfully" , "i")
                
                try:
                    os.startfile(r"C:\programData\Jarvis\settings.txt")
                    print("\nsettings file was opened\n\n")
                    time.sleep(2)
                    os.system("pause")
                    os.system("cls")
                    return True
                except Exception:
                    self.cLog.log("File was regenerated but still cannot be opened" , "e")
                    os.system("cls")
                    print("settings file cannot be opened even after regeneration\n")
                    print("try reinstalling the program with administrative premission\n")
                    print("if the error remains follow instructions : ")
                    print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
                    print("step 2 - {}\n\n".format(self.cLog.getLogFileMessage))
                    os.system("pause")
                    os.system("cls")
                    return False
                
            elif(generateStatus == False):
                print("\nError Occured while generating the settings file\n")
                print("try reinstalling the program with administrative premission\n")
                print("if the error remains follow instructions : ")
                print("step 1 - run command troubleshoot in jarvis , this will generate a log file named as {} on desktop".format(self.cLog.logFileName))
                print("step 2 - {}\n\n".format(self.cLog.getLogFileMessage))
                os.system("pause")
                os.system("cls")
                return False
            
# driver code - only for testing purpose
if __name__ == "__main__":
    obj = Setting()
    print(obj.makeDictionaryFromTxt())
