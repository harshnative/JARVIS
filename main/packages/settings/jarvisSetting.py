import os
import time
from packages.loggerPackage.loggerFile import *



import subprocess as sp

isOnWindows = False
isOnLinux = False

# Checking weather the user is on windows or not
try:
    temp = os.environ
    tempUserName = temp["USERNAME"]
    isOnWindows = True
except Exception:
    isOnLinux = True


# clear screen function 
def customClearScreen():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)


# start file function for diff operating systems
import sys

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        sp.call([opener, filename])


class Setting():
    """
This is the main class of the settings module

methods - 

1.  getDictionary()      ->    this method is used to get the dictionary from the txt file
                               returns False if it cannot generate dictionary

2.  openFile()           ->    used to open the settings file in default txt file viewer

3.  regenerateFile()     ->    used to regenerate the settings file
                               New things must be added into this function to keep it uptodate
    """
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
            customClearScreen()
            print("settings file cannot be found , try restarting or reinstalling the program , or go to website for help")
            return False

        except Exception as e:
            customClearScreen()
            self.cLog.log("error while opening the help file" , "e")
            self.cLog.exception(str(e) , "In jarvisSetting.py/makeDictionaryFromTxt_func")
            if(self.cLog.troubleShoot == False):
                print("\nSomething went wrong, Please Try again, if error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
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

            fil.write("# path to backup for jarvis - ex - F:/myBackup\n")
            fil.write("backUpPathForJarvis = \n\n")

            fil.write("# User Name :\n")
            fil.write("userName = \n\n")

            fil.write("# Greeting :\n")
            fil.write("greeting = Welcome\n\n")

            fil.close()
            return True
            
        except Exception:
            customClearScreen()
            
            if(self.cLog.troubleShoot == False):
                print("It seems like Jarvis do not have write permission in this folder")
                print("try reinstalling the program with administrative premission\n")
                print("\nif error persist, run troubleShoot command")
            else:
                print("\nerror has been logged - continue...")
            input("press enter to continue...")
            customClearScreen()
            return False


    # funnction to open the settings file in default txt viewer
    def openFile(self):
        try:
            open_file(r"C:\programData\Jarvis\settings.txt")
            return True
        except FileNotFoundError:
            customClearScreen()
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
                    open_file(r"C:\programData\Jarvis\settings.txt")
                    print("\nsettings file was opened\n\n")
                    time.sleep(2)
                    input("press enter to continue...")
                    customClearScreen()
                    return True
                except Exception:
                    self.cLog.log("File was regenerated but still cannot be opened" , "e")
                    customClearScreen()
                    if(self.cLog.troubleShoot == False):
                        print("settings file cannot be opened even after regeneration\n")
                        print("try reinstalling the program with administrative premission\n")
                        print("\nif error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
                    input("press enter to continue...")
                    customClearScreen()
                    return False
                
            elif(generateStatus == False):

                if(self.cLog.troubleShoot == False):
                    print("\nError Occured while generating the settings file\n")
                    print("try reinstalling the program with administrative premission\n")
                    print("\n if error persist, run troubleShoot command")
                else:
                    print("\nerror has been logged - continue...")
                input("press enter to continue...")
                customClearScreen()
                return False
            
# driver code - only for testing purpose
if __name__ == "__main__":
    obj = Setting()
    print(obj.makeDictionaryFromTxt())
