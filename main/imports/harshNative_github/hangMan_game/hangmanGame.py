import os
import random

isOnWindows = False
isOnLinux = False

# Checking weather the user is on windows or not
try:
    temp = os.environ
    tempUserName = temp["USERNAME"]
    isOnWindows = True
except Exception:
    isOnLinux = True
    
import subprocess as sp

def customClearScreen():
    if(isOnWindows == True):
        os.system("cls")
    else:
        sp.call('clear',shell=True)

#class for handling the tasks when a user guess a wrong letter
class failure:
    
    def __init__(self):
        self.failureCount = 0
        self.string = "dumbAss"
        self.gameOver = False 

    def increaseFunc(self):
        self.failureCount += 1 

    def showFunc(self):
        if(self.failureCount >= 7):
            self.gameOver = True 
            return "DumbAss"
            
        else:
            return self.string[:(self.failureCount)]

    def isGameOver(self):
        return self.gameOver

    def isGameContinue(self):
        return not(self.gameOver)


    def resetValues(self):
        self.failureCount = 0
        self.gameOver = False


# class for handling the main game events
class game:

    def __init__(self , wordToBeGuessed):
        self.word = str(wordToBeGuessed).strip()
        self.wordCopy = ""
        for i in range(len(self.word)):
            self.wordCopy = self.wordCopy + "*"
        self.wordCopy = str(self.wordCopy)
    
    def changeWordCopy(self , letterPassed):
        for i,j in enumerate(self.word):
            if(j == letterPassed):
                self.wordCopy = self.wordCopy[:i] + letterPassed + self.wordCopy[i+1:]


    def showWordCopy(self):
        return self.wordCopy

    def isLetterInWord(self , letterPassed):
        for i in self.word:
            if(i == letterPassed):
                return True
        return False

    def isWordGuessed(self):
        for i in self.wordCopy:
            if(i == "*"):
                return False
        return True


# func for returning a random word from the file
def returnEasyWord():
    myList = []
    try:
        with open("txtFiles/easyWordsCat.txt" , "r") as fil:
            myList = fil.readlines()
    except FileNotFoundError:
        print("catalogue file is missing")
        print("\n\ngame will quit now :(")
        input()
        return False
    
    lowerLimit = 0
    upperLimit = len(myList) - 1

    randomNumber = random.randint(lowerLimit , upperLimit)

    return myList[randomNumber]


# func for returning a random word from the file
def returnCityCountryWord():
    myList = []
    try:
        with open("txtFiles/cityCountryWord.txt" , "r") as fil:
            myList = fil.readlines()
    except FileNotFoundError:
        print("catalogue file is missing")
        print("\n\ngame will quit now :(")
        input()
        return False
    
    lowerLimit = 0
    upperLimit = len(myList) - 1

    randomNumber = random.randint(lowerLimit , upperLimit)

    return myList[randomNumber]




# func for returning a random word from the file
def returnWord(): 
    myList = []
    try:
        with open("txtFiles/wordsCat.txt" , "r") as fil:
            myList = fil.readlines()
    except FileNotFoundError:
        print("catalogue file is missing")
        print("\n\ngame will quit now :(")
        input()
        return False
    
    lowerLimit = 0
    upperLimit = len(myList) - 1

    randomNumber = random.randint(lowerLimit , upperLimit)

    return myList[randomNumber]


# main function - the driver code
def subMainForHangmanGame(word):
    
    objGame = game(word)

    objFailure = failure()


    while(objFailure.isGameContinue):
        print("this is the word you have to guess the letter for now - {}".format(objGame.showWordCopy()))
        x = input("enter the letter - ")
        while( len(x) != 1 ):
            print("\n\nwrong input try again......")
            x = input("enter the letter - ")

        customClearScreen()
        if(objGame.isLetterInWord(x)):
            print("\n\nyoo the letter is in the word")
            objGame.changeWordCopy(x)
        else:
            objFailure.increaseFunc()
            print("\n\noops wrong guess , you have become {} out of {}".format(objFailure.showFunc() , objFailure.string))
        
        print("updated word is {}".format(objGame.showWordCopy()))
        print("\n\npress enter to continue")
        input()
        customClearScreen()
        if(objGame.isWordGuessed()):
            print("yoo you guessed the word the word was {}".format(objGame.word))
            return 0
        if(objFailure.isGameOver()):
            print("Game over , you loose.... , the word was {}".format(objGame.word))
            return 0
            
# function that will be called from the jarvis
def mainForHangmanGame():
    while(1):
        customClearScreen()
        print("which level do you want to play - ")
        print("1. easy")
        print("2. medium")
        print("3. City / Country names")

        try:    
            level = int(input("enter your preference here : "))
        except ValueError:
            customClearScreen()
            print("oops wrong input try again")
            input()
            continue
            

        if(1 < level < 4):
            pass
        else:
            customClearScreen()
            print("oops wrong input try again")
            input()
            continue
        
        word = ""

        if(level == 1):
            word = returnEasyWord()
        if(level == 2):
            word = returnWord()
        if(level == 3):
            word == returnCityCountryWord()

        # if the txt files for words is not found
        if(word == False):
            return False

        customClearScreen()
        subMainForHangmanGame(word)

        print("\n\nenter zero below to play again ...")
        x = input()
        if(x == "0"):
            pass
        else:
            return True
    

# below code is for testing purpose only
# if main for repeadely playing the game and major inputs 
# if __name__ == "__main__":
#     while(1):
#         os.system("cls")
#         print("which level do you want to play - ")
#         print("1. easy")
#         print("2. medium")

#         try:    
#             level = int(input("enter your preference here : "))
#         except ValueError:
#             os.system("cls")
#             print("oops wrong input try again")
#             input()
#             continue
            

#         if(level == 1):
#             pass 
#         elif(level == 2):
#             pass
#         else:
#             os.system("cls")
#             print("oops wrong input try again")
#             input()
#             continue


#         if(level == 1):
#             word = returnEasyWord()
#         else:
#             word = returnWord()

#         os.system("cls")
#         main(word)

#         print("\n\nenter zero below to play again ...")
#         x = input()
#         if(x == "0"):
#             pass
#         else:
#             exit()