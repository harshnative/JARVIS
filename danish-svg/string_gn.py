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
    for i in range(2):
        rstr.append(random.choice(upperCase))
    for i in range(3):
        rstr.append(random.choice(lowerCase))
    for i in range(2):
        rstr.append(random.choice(nums))
    rstr.append(random.choice(spChar))
    
    rstr = set(rstr)
    string = ''
    for i in rstr:
        string+=i
    
    return string
    

