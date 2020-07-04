def type_counter(string):
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
    count = [0,0,0,0] #lowercase,uppercase,specialtype,numbers
    for p in string:
        if (p in lowerCase) and (count[0]==0) and len(string)>=8:
            count[0]=1
        if (p in upperCase) and (count[1]==0) and len(string)>=8:
            count[1]=1
        if (p in spChar) and (count[2]==0) and len(string)>=8:
            count[2]=1
        if (p in nums) and (count[3]==0)  and len(string)>=8:
            count[3]=1
    type_num = 0
    for i in count:
        type_num+=i
    return type_num