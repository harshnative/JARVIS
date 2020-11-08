import http.server
from socket import error, setdefaulttimeout
import socketserver
import os
import socket
from os import path
import multiprocessing


class quietServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


# main module class 
class FileShareClass:

	# default constructor 
    def __init__(self):
        self.ipAddress = None
        self.port = 8000
        self.folderToShare = None
        self.logToConsole = False
        self.mulProcess = multiprocessing.Process(target=self.startServerAtFolderSetted)

    # method to set the custom port number
    # raises exception if not a four digit integer
    def setPort(self , port):
        try:
            self.port = int(port)
        except Exception:
            raise Exception("Port number passed is not an integer")

        if(1000 < self.port < 10000):
            pass
        else:
            raise Exception("port number must be a four digit integer")

    # function to get the port number
    def getPort(self):
        return self.port

    # function to set the path to folder to share
    def setSharePath(self , folderPath):
        if(path.exists(str(folderPath)) == True):
            self.folderToShare = str(folderPath)
        else:
            raise Exception("python cannot find passed folder path to share")

    # function to get the path to folder to share
    def getSharePath(self):
        return self.folderToShare

    # function to get the ip address to the network to which computer is currently connected
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    # function to start the python http server
    def startServerAtFolderSetted(self):
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    

        web_dir = os.path.join(self.folderToShare)
        os.chdir(web_dir)
        
        if(not(self.logToConsole)):
            with socketserver.TCPServer(("", self.port), quietServer) as httpd:
                httpd.serve_forever()

        else:
            Handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("", self.port), Handler)

            httpd.serve_forever()


    
    # function ot operate the class methods
    def start_fileShare(self , folderToShare , port = 8000 , logToConsole = False):
        self.setSharePath(folderToShare)
        self.setPort(port)
        self.ipAddress = self.get_ip_address()
        self.logToConsole = logToConsole

        toReturn = []

        toReturn.append("Visit http://{}:{} to browse or download the files".format(self.ipAddress , self.port))
        toReturn.append("Files only available to devices present in the same network connection")

        self.mulProcess.start()

        return toReturn

    # method to stop file share
    def stopFileShare(self):
        self.mulProcess.terminate()
        

# for testing purpose
if __name__ == "__main__":
    pass
    fil = FileShareClass()
    print(fil.start_fileShare("C:/users/harsh/desktop"))

    import time
    time.sleep(60)
    fil.stopFileShare()