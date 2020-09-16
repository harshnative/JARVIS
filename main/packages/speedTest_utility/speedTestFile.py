import speedtest   
import os
from packages.loggerPackage.loggerFile import *


import subprocess as sp

class GlobalData:
    isOnWindows = False
    isOnLinux = False

import platform
import time

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData.isOnLinux = True
elif(osUsing == "Windows"):
    GlobalData.isOnWindows = True
else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    exit()


# clear screen function 
def customClearScreen():
    if(GlobalData.isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)




class SpeedTestClass:
    """
This is the main class of speed test file

methods - 
1.  runSpeedTestUtility    ->    this the only method that you need to use this class functions as
                                 this methods automatically calls other methods of the class

                                 this method accepts two arguments -
                                                                                
                                 1st inBytes - if the result shown need to be in MegaBytes instead of Megabits
                                               default value of this is False
                                                                                
                                 2nd numberOfTimesToDo - How many times you need to average the result out
                                                         default value is two
    """

    # contructor for the class
    def __init__(self , troubleShootValuePass):
        self.st = None
        self.cLog = Clogger()
        self.troubleShootValue = troubleShootValuePass
        self.cLog.setTroubleShoot(self.troubleShootValue)
    

    # function to set things up - mainly creating obj of speedtest module and setting up server
    # this function returns false if it cannot find a serve - mainly due to lack of internet connection
    def setThingsUp(self):
        try:
            # creating object
            self.st = speedtest.Speedtest()

            # getting best server
            self.st.get_best_server()

            self.cLog.log("set things up function runned successfully for speed test file" , "i")
            return True     # returned True as server setted up successfully

        except Exception as e:
            self.cLog.log("set things up function failed to execute properly becuase exception occured", "e")
            self.cLog.exception(str(e) , "in speedTest.py/setThingsUP_function")
            return False


    # function to convert bits into mega bits
    def convToMb(self , bitsPass):
        self.cLog.log("convToMb function runned successfully for speed test file" , "i")
        return (bitsPass / (1024 * 1024))


    # function to convert mega bits to mega bytes
    def convToMB(self , megaBitsPass):
        self.cLog.log("convToMB function runned successfully for speed test file" , "i")
        return (megaBitsPass / 8)


    # function to get the download speed
    def getDownloadSpeed(self):
        try:
            toReturn = self.st.download()
            self.cLog.log("getDownloadSpeed function runned successfully for speed test file" , "i")
            return toReturn
        except Exception as e:
            self.cLog.log("get download speed function failed to execute properly becuase exception occured" , "e")
            self.cLog.exception(str(e) , "in speedTest.py/get download speed_function")
            return False


    # function to get the upload speed
    def getUploadSpeed(self):
        try:
            toReturn = self.st.upload()
            self.cLog.log("getUploadSpeed function runned successfully for speed test file" , "i")
            return toReturn
        except Exception as e:
            self.cLog.log("get upload speed function failed to execute properly becuase exception occured" , "e")
            self.cLog.exception(str(e) , "in speedTest.py/get upload speed_function")
            return False


    # function to get the upload speed
    def getPing(self):
        try:
            toReturn = self.st.results.ping
            self.cLog.log("getPing function runned successfully for speed test file" , "i")
            return toReturn
        except Exception as e:
            self.cLog.log("get ping function failed to execute properly becuase exception occured" , "e")
            self.cLog.exception(str(e) , "in speedTest.py/get ping_function")
            return False


    # main function of the class to handle all the internal process and output result
    def runSpeedTestUtility(self , inBytes = False , numberOfTimesToDo = 2):
        customClearScreen()
        print("running speed test - this may take some time")
        
        # checking internet connection status
        status = self.setThingsUp()
        
        if(status == False):
            # if the internet is not present
            print("Could not run speed test , make sure you are online ...")
            self.cLog.log("status comed false in run speed test utility function" , "i")
            return False
        
        else:
            # setting up some variables to avoid garbage value allocation
            avgDownloadSpeed = 0
            avgUploadSpeed = 0
            avgPing = 0
            value = 0

            # running loop for doing number of test as pass or by default 2 times
            for i in range(numberOfTimesToDo):
                customClearScreen()

                # printing message
                print("running speed test - this may take some time")
                print("\nProcessing pass {} out of {}".format(i+1 , numberOfTimesToDo))

                # checking download speed
                print("\nchecking Download Speed...")
                value = self.getDownloadSpeed()
                if(value == False):
                    customClearScreen()
                    if(self.cLog.troubleShoot == False):
                        print("\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
                    self.cLog.log("download speed test failed in run speed test utility", "i")
                    return False
                avgDownloadSpeed = avgDownloadSpeed + value

                # checking upload speed
                print("checking Upload Speed...")
                value = self.getUploadSpeed()
                if(value == False):
                    customClearScreen()
                    if(self.cLog.troubleShoot == False):
                        print("\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
                    self.cLog.log("upload speed test failed in run speed test utility", "i")
                    return False
                avgUploadSpeed = avgUploadSpeed + value

                # checking ping 
                print("checking Ping...")
                value = self.getPing()
                if(value == False):
                    customClearScreen()
                    if(self.cLog.troubleShoot == False):
                        print("\nSpeed test failed, Something went wrong, Please Try again, if error persist, run troubleShoot command")
                    else:
                        print("\nerror has been logged - continue...")
                    self.cLog.log("ping test failed in run speed test utility", "i")
                    return False
                avgPing = avgPing + value


            avgDownloadSpeed = avgDownloadSpeed / (numberOfTimesToDo) 
            avgUploadSpeed = avgUploadSpeed / (numberOfTimesToDo)
            avgPing = avgPing / (numberOfTimesToDo)

            avgDownloadSpeed = self.convToMb(avgDownloadSpeed)
            avgUploadSpeed = self.convToMb(avgUploadSpeed)

            customClearScreen()
            if(inBytes == False):
                print("Download speed    =    {} Mb/s".format(avgDownloadSpeed))
                print("upload speed      =    {} Mb/s".format(avgUploadSpeed))
                print("ping              =    {} ms".format(avgPing))
            else:
                print("Download speed    =    {} MB/s".format(self.convToMB(avgDownloadSpeed)))
                print("upload speed      =    {} MB/s".format(self.convToMB(avgUploadSpeed)))
                print("ping              =    {} ms".format(avgPing))

            self.cLog.log("speed test main function - run speed test utility executed successfully", "i")

            return True



   
if __name__ == "__main__":
    obj = SpeedTestClass()
    obj.runSpeedTestUtility(True)

