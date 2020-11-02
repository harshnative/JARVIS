import os
import time
from packages.loggerPackage.loggerFile import *
import shutil

import subprocess as sp

class GlobalData_jarvisSetting:

    folderPathWindows = r"C:\programData\Jarvis"
    folderPathLinux = r"~/.config/Jarvis"
    folderPathWindows_simpleSlash = r"C:/programData/Jarvis"

    isOnWindows = False
    isOnLinux = False

import platform
import time
import sys

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_jarvisSetting.isOnLinux = True
elif(osUsing == "Windows"):
    GlobalData_jarvisSetting.isOnWindows = True
else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    sys.exit()


# clear screen function 
def customClearScreen():
    if(GlobalData_jarvisSetting.isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)




def open_file(filename):
    try:
        os.startfile(filename)
    except Exception:
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
    def __init__(self , troubleShootValuePass , makeKeyboardSound):
        self.makeKeyboardSound = makeKeyboardSound
        self.myDictionary = { }
        self.troubleShootValue = troubleShootValuePass
        self.cLog = Clogger()
        self.cLog.setTroubleShoot(self.troubleShootValue)
        if(GlobalData_jarvisSetting.isOnWindows):
            self.pathToSetting = GlobalData_jarvisSetting.folderPathWindows_simpleSlash + r"\settings.txt"
        else:
            self.pathToSetting = GlobalData_jarvisSetting.folderPathLinux + r"/settings.txt"


    # method for making dictionary by reading the txt file
    def makeDictionaryFromTxt(self):

        try:
            # opening the txt file
            with open(self.pathToSetting , "r+") as fil:

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
            self.cLog.log("settings file could not be found , trying to regenerate file" , "w")
            statusOfRegeneration = self.regenerateFile()
            if(statusOfRegeneration):
                self.cLog.log("settings file generated successfully" , "e")
                self.makeDictionaryFromTxt()
            else:
                print("settings file cannot be found , try restarting or reinstalling the program , or go to website for help")
                self.cLog.log("settings file could not be generated" , "e")
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
            shutil.copy2("txtFiles/settings.txt" , self.pathToSetting)
            return True
            
        except Exception as e:
            customClearScreen()
            
            if(self.cLog.troubleShoot == False):
                print("It seems like Jarvis do not have write permission in this folder")
                print("try reinstalling the program with administrative premission\n")
                print("\nif error persist, run troubleShoot command")
                self.cLog.log("error while copying the settins file" , "e")
                self.cLog.exception(str(e) , "In jarvisSetting.py/regenerate file function")
            else:
                print("\nerror has been logged - continue...")
                self.cLog.log("error while copying the settins file" , "e")
                self.cLog.exception(str(e) , "In jarvisSetting.py/regenerate file function")

            input("press enter to continue...")
            customClearScreen()
            return False


    # funnction to open the settings file in default txt viewer
    def openFile(self):
        try:
            open_file(self.pathToSetting)
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
                    open_file(self.pathToSetting)
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
