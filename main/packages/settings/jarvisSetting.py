class setting():

    # constructor
    def __init__(self):
        self.myDictionary = {}


    # method for making dictionary by reading the txt file
    def makeDictionaryFromTxt(self):

        # opening the txt file
        with open("settings.txt" , "r+") as fil:

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
                        splitedList = line.split(":")
                        newSplitedList = []

                        for i in splitedList:
                            i = i.strip()
                            newSplitedList.append(i)
                        
                        # adding to dictionary
                        self.myDictionary[newSplitedList[0]] = newSplitedList[1]
                except Exception:
                    pass

    
    # function to return the dictionary
    def getDictionary(self):
        self.makeDictionaryFromTxt()
        return self.myDictionary


    
# driver code - only for testing purpose
if __name__ == "__main__":
    obj = setting()
    obj.makeDictionaryFromTxt()