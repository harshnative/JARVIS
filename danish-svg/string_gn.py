import random
def string_gnrter():
    lowerCase = ['a','s','d','f','g','h','j','k','l','z','x',
                'c','v','b','n','m','q','w','e','r','t','y','u'
                 ,'i','o','p']

    upperCase = []
    for i in lowerCase:
        upperCase.append(i.upper())

    spChar = ['~','!','@','$','%','^','&','*','(',')','_','-','=',
             '`','/','+','/','<','>','[',']','{','}','.',':',';',
             '|','#']

    nums = ['1','2','3','4','5','6','7','8','9','0']

    rstr = []
    for i in range(3):
        rstr.append(random.choice(upperCase))
    for i in range(4):
        rstr.append(random.choice(lowerCase))
    for i in range(4):
        rstr.append(random.choice(nums))
    rstr.append(random.choice(spChar))
    
    rstr = set(rstr)
    string = ''
    for i in rstr:
        string+=i

    if(len(string) < 12):
        string = string_gnrter()
    
    return string
    

# for testing purpose only
if __name__ == '__main__':
    myList = []
    repeat = 0
    count = 0

    for i in range(100000):
        stringGet = string_gnrter()
        if(stringGet in myList):
            repeat += 1
        myList.append(string_gnrter())
        count += 1
        print(count)

    print(repeat)
