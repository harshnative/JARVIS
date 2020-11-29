import http.server
from socket import error, setdefaulttimeout
import socketserver
import os
import socket
from os import path
import multiprocessing

import logging
from pyftpdlib.log import config_logging


from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer


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
        self.mulProcess1 = multiprocessing.Process(target=self.startServerAtFolderSettedHTTP)
        self.mulProcess2 = multiprocessing.Process(target=self.startServerAtFolderSettedFTP)
        self.http = False
        self.logToConsole = False

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
    def startServerAtFolderSettedHTTP(self):
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


    # function to start the python http server
    def startServerAtFolderSettedFTP(self):
        if(self.ipAddress == None):
            raise Exception("Could not get system IP Address")
        if(self.folderToShare == None):
            raise Exception("path to folder to share is not setted")    


        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user('user', '225588', self.folderToShare , perm='elradfmwMT')
        authorizer.add_anonymous(homedir=self.folderToShare)

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        if(not(self.logToConsole)):
            config_logging(level=logging.ERROR)

        # Define a customized banner (string returned when client connects)
        handler.banner = "pyftpdlib based ftpd ready."
        address = (self.ipAddress, self.port)  # listen on every IP on my machine on port 21
        server = servers.FTPServer(address, handler)
        server.serve_forever()
 
    
    # function to operate the class methods
    def start_fileShare(self , folderToShare , port = 8000 , http = False , logToConsole = False):
        self.setSharePath(folderToShare)
        self.setPort(port)
        self.ipAddress = self.get_ip_address()
        self.http = http
        self.logToConsole = logToConsole

        toReturn = []

        if(self.http):
            toReturn.append("Visit http://{}:{} in browse to download files".format(self.ipAddress , self.port))
            toReturn.append("Files only available to devices connected to the same network")

            self.mulProcess1.start()

        else:
            toReturn.append("Visit ftp://{}:{} in file explorer or FTP browse to download files".format(self.ipAddress , self.port))
            toReturn.append("For Uploading as well Visit ftp://user:225588@{}:{} in same".format(self.ipAddress , self.port))
            toReturn.append("Files only available to devices connected to the same network")
            self.mulProcess2.start()

        return toReturn

    # method to stop file share
    def stopFileShare(self):
        if(self.http):
            self.mulProcess1.terminate()
        else:
            self.mulProcess2.terminate()
        

# # for testing purpose
# if __name__ == "__main__":
#     pass
#     fil = FileShareClass()
#     print(fil.start_fileShare("C:/users/harsh/desktop" , http = False))

#     import time
#     time.sleep(60)
#     fil.stopFileShare()