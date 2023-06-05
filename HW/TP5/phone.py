import re

class State:
    def __init__(self,stateName):
        self.stateName = stateName
        self.nextStates = []

    def addNextStates(self,nextStates):
        if(isinstance(nextStates,list)):
            for state in nextStates:
                self.nextStates.append(state)
        
        self.nextStates = list(set(self.nextStates))
    
    def addNextState(self,newState):
        self.nextStates.append(newState)
        self.nextStates = list(set(self.nextStates))
        


class StateMachine:
    
    def __init__(self,states,currentState):
        self.states = states
        self.currentState = currentState
        self.prevState = None
    

    def changeState(self,newState):
        
        stateFound = False
        for state in self.currentState.nextStates:
            if(state.stateName == newState.stateName):
                stateFound = True
                break
        
        if(stateFound):
            self.prevState = self.currentState 
            self.currentState = newState
            return True
        else:
            print("The Command Is Not Valid In This State")
            return False

    def changeStateWithName(self,newStateName):
        # print("New State Name: ",newStateName)
        for state in self.states:
            if(state.stateName.lower() == newStateName.lower()):
                return self.changeState(state) 
        
        print("The Command Is Not Valid")
        return False

    def returnToPrevState(self):
        self.currentState = self.prevState


class Machine:

    def __init__(self) :
        
        self.IDLE = State("I")
        self.LIFT = State("LIFT")
        self.LAND = State("LAND")
        self.CURRENCY = State("CURRENCY")
        self.TELEPHONE = State("T")
        self.ABORT = State("ABORT")

        self.validCurrencies = ["5c","10c","20c","50c","1e","2e"]
        self.balanceCent = 0
        self.balanceEuro = 0
        
        # In cents
        self.intMinPrice = 150
        self.natMinPrice = 25
        self.blueMinPrice = 10

        states = [self.LIFT,self.LAND,self.CURRENCY,self.TELEPHONE,self.ABORT]

        self.IDLE.addNextStates([self.LIFT])
        self.LIFT.addNextStates([self.LAND,self.CURRENCY,self.ABORT])
        self.LAND.addNextStates([self.LIFT])
        self.CURRENCY.addNextStates([self.ABORT,self.LAND,self.TELEPHONE])
        self.TELEPHONE.addNextStates([self.LAND,self.ABORT])
        self.ABORT.addNextStates([self.LIFT])

        self.stateMachine = StateMachine(states,self.IDLE)

    def startInterraction(self):
        
        cmdRegex = re.compile(r'\A[a-zA-Z]+')
        currencyRegex = re.compile(r'(\d+)(c|e)')
        telephoneRegex = re.compile(r'(00|\d{3})(\d){6}')

        while True:
            msg = input(": ")
            res = cmdRegex.search(msg)

            # No Commands
            if(res == None):
                print("Wrong Command Type")
                continue
            
            # Change State if not wrong
            if(not self.stateMachine.changeStateWithName(res.group())):
                print("The Valid Commands: ")
                for state in self.stateMachine.currentState.nextStates:
                    print(state.stateName)
                continue

            # Execute The State
            # Lift State
            if(self.stateMachine.currentState == self.LIFT):
                print("maq: Please insert coin")

            # Currency State
            elif(self.stateMachine.currentState == self.CURRENCY):
                res = currencyRegex.finditer(msg)
                
                for money in res:
                    if(money.group().lower() not in self.validCurrencies):
                        print("maq: {} - invalid currency".format(money.group()))
                    else:
                        if(money.group(2).lower() == "c"):
                            self.balanceCent += int(money.group(1))
                            if(self.balanceCent >= 100):
                                self.balanceCent %= 100
                                self.balanceEuro += 1
                        elif(money.group(2).lower() == "e"):
                            self.balanceEuro += int(money.group(1))
                
                print("balance = {}e{}c".format(self.balanceEuro,self.balanceCent))

            # Telephone Balance
            elif(self.stateMachine.currentState == self.TELEPHONE):
                res = telephoneRegex.search(msg)

                if(res == None):
                    # Invalid Number 
                    self.stateMachine.returnToPrevState()
                    print("maq: Wrong Number")

                elif(res.group(1) == "601" or res.group(1) == "641"):
                    # Restricted Numbers
                    self.stateMachine.returnToPrevState()
                    print("maq: This number is not allowed on this phone. Please dial new number!")

                elif(res.group(1) == "00"):
                    # International Calls
                    if( (self.balanceEuro * 100) + self.balanceCent <= self.intMinPrice ):
                        self.stateMachine.returnToPrevState()
                        print("maq: The Balance Is Not Enough For International Calls")
                    else:
                        # Make the call
                        cents = self.balanceEuro * 100 + self.balanceCent
                        cents -= self.intMinPrice
                        self.balanceEuro = cents // 100
                        self.balanceCent = cents % 100
                        print("maq: balance = {}e{}c".format(self.balanceEuro,self.balanceCent))
                
                elif(res.group(1)[0] == "2"):
                    # National Calls Starting With 2

                    if( (self.balanceEuro * 100) + self.balanceCent <= self.natMinPrice ):
                        self.stateMachine.returnToPrevState()
                        print("maq: The Balance Is Not Enough For National Calls")
                    else:
                        cents = self.balanceEuro * 100 + self.balanceCent
                        cents -= self.natMinPrice
                        self.balanceEuro = cents // 100
                        self.balanceCent = cents % 100
                        print("maq: balance = {}e{}c".format(self.balanceEuro,self.balanceCent))

                elif(res.group(1) == "800"):
                    # Green Calls No Price
                    print("maq: balance = {}e{}c".format(self.balanceEuro,self.balanceCent))

                elif(res.group(1) == "808"):
                    # Blue Calls Starting With 808
                    if( (self.balanceEuro * 100) + self.balanceCent <= self.blueMinPrice ):
                        self.stateMachine.returnToPrevState()
                        print("maq: The Balance Is Not Enough For Blue Calls")
                    else:
                        cents = self.balanceEuro * 100 + self.balanceCent
                        cents -= self.blueMinPrice
                        self.balanceEuro = cents // 100
                        self.balanceCent = cents % 100
                        print("maq: balance = {}e{}c".format(self.balanceEuro,self.balanceCent))

                else:
                    self.stateMachine.returnToPrevState()
                    print("maq: Wrong Number")      

            # Abort
            elif(self.stateMachine.currentState == self.ABORT):
                print("maq: Aborted change: {}e{}c ".format(self.balanceEuro,self.balanceCent))
            
            # Land
            elif(self.stateMachine.currentState == self.LAND):
                print("maq: change: {}e{}c; Come back often! ".format(self.balanceEuro,self.balanceCent))
            


                    
if __name__ == "__main__":
    
    phone = Machine()
    phone.startInterraction()
            
    


        
