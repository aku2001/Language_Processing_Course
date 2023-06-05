import re 


digRegex = re.compile(r'(\d)')
eqRegex = re.compile(r'=')
onRegex = re.compile(r'(on|On|ON)')
offRegex = re.compile(r'(of|Of|OFF)')
on = True

while True:
    msg = input(": ")
    sumRes = 0

    onRes = onRegex.search(msg)
    offRes = offRegex.search(msg)

    if(onRes != None):
        on = True
    elif(offRes != None):
        on = False

    if(on):
        res = digRegex.findall(msg)
        eqRes = eqRegex.search(msg)

        
        if(len(res)> 0):
            for num in res:
                sumRes += int(num)
            
            print("= ",sumRes)
        





