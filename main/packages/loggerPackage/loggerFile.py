import logging

# custom logger class
class Clogger:

    """
This class is a custom implementation of the looger module available in python

methods included - setTroubleShoot()    ->    used to set the the log level - 
                                              if True then the debug and info level logs will also be logged
                                              default troubleShoot value is False

                 - setLoggerConfig()    ->    set the logger module configration according to the troubleshoot value
                 
                 - log()                ->    used to log the stuff
                                              to use create a obj of Clogger class and call this function
                                              you need to pass on 2 arguments , 1st will be the log message as string
                                              2nd will the level the log - 
                                              "d" for debug ,
                                              "i" for info ,
                                              "w" for warning , 
                                              "e" for error ,
                                              "c" for critical
                
                - exception()           ->    used to log an exception
                                              accepts to arguments - 1st is the exception as string
                                              and 2nd is the message

                                              ex - except Exception as e:
                                                       objClogger.exception(str(e) , "Exception occured in fileName.py/funcName - ")
    """

    # constructing important variables
    def __init__(self):
        self.troubleShoot = False
        self.logFileName = r"C:\programData\Jarvis\jarvisLogs.log"
        self.getLogFileMessage = "Email us this file at myjarvispa@gmail.com and we will fix the error as soon as possible"
        self.setLoggerConfig()

    def setTroubleShoot(self , boolValuePass):
        self.troubleShoot = bool(boolValuePass)
        self.setLoggerConfig()

    # function to define basic config of logging module
    def setLoggerConfig(self):
        
        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # setting up logging configration
        if(self.troubleShoot == True):
            logging.basicConfig(level=logging.DEBUG , filename = self.logFileName , format='%(asctime)s - %(levelname)s : %(message)s' , datefmt='%d-%b-%y %H:%M:%S')
        else:
            logging.basicConfig(level=logging.WARNING , filename = self.logFileName , format='%(asctime)s - %(levelname)s : %(message)s' , datefmt='%d-%b-%y %H:%M:%S')

    # creating a logger function for easy logging
    # levels can be debug , info , warning , error , critical or shortly d , i , w , e , c
    def log(self, message , level):
        """ levels can be debug , info , warning , error , critical or shortly d , i , w , e , c """
        if((level == "debug") or (level == "d")):
            logging.debug(str(message))
        elif((level == "info") or (level == "i")):
            logging.info(str(message))
        elif((level == "warning") or (level == "w")):
            logging.warning(str(message))
        elif((level == "error") or (level == "e")):
            logging.error(str(message))
        elif((level == "critical") or (level == "c")):
            logging.critical(str(message))
        else:
            logging.error("log parameter incorrectly passed")

    def exception(self , exceptionPass , PlaceOfException):
        stringPass = "In : " + PlaceOfException + " Exception Occured - " + exceptionPass
        logging.error(str(stringPass))

if __name__ == "__main__":
    objClogger = Clogger()
    print(objClogger.__doc__)