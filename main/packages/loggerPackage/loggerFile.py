import logging

# custom logger class
class Clogger:

    # constructing important variables
    def __init__(self):
        self.troubleShoot = False
        self.logFileName = "jarvis.log"
        self.getLogFileMessage = "Email us this file at jarvismail@gmail.com and we will fix the error as soon as possible"

    def setTroubleShoot(self , boolValuePass):
        self.troubleShoot = bool(boolValuePass)

    # function to define basic config of logging module
    def setLoggerConfig(self):
        """ Must be called """
        # setting up logging configration
        if(self.troubleShoot == True):
            logging.basicConfig(level=logging.DEBUG , filename = logFileName , format='%(asctime)s - %(message)s' , datefmt='%d-%b-%y %H:%M:%S')
        else:
            logging.basicConfig(level=logging.WARNING , filename = logFileName , format='%(asctime)s - %(message)s' , datefmt='%d-%b-%y %H:%M:%S')

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
