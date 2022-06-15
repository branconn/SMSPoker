import deck
from gameGlobals import *

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.funds = BUY_IN
        self.playerBet = 0
        self.raisable = True # tracks whether a player can still raise during a betting round

    def sufficientFunds(self, query): # checking if an input is smaller than the (funds + bet) of player
        return (query <= self.funds + self.playerBet)

    def bettingPrompt(self, currentBet, lastMove):
        print(lastMove)
        if not self.sufficientFunds(currentBet):
            # TODO: implement sidepot
            print(self.name + "does not have enough cash to continue")
            return False
        else:
            if self.raisable:
                answer = input("Would you like to fold [f], call/check [c], or raise bet to N [rN]?")
            else:
                answer = input("You can no longer raise. Would you like to fold [f] or call/check [c]?")
            
            # player folds
            if answer == "f":
                return False # returning boolean flag to remove player from betting lineUp
            
            # player calls / checks
            if answer == "c":
                self.raisable = False # a player only gets one chance to raise in a bettin round
                self.funds -= (currentBet - self.playerBet) # subtracting difference from player funds
                self.playerBet = currentBet # updating player bet
                return self.playerBet # returning current bet to client
            
            # player raises
            if answer[0] == "r": 
                try:
                    bet = int(answer[1:]) # checking if raise input is correct format
                except:
                    print("Input format for a raise should be 'r[Amount]', e.g. 'r15'\nRaise amount cannot be lower than current bet + big blind")
                    self.bettingPrompt() # recursive retry
                else:
                    limit = currentBet + BIG_BLIND
                    if bet >= limit:
                        if not self.sufficientFunds(bet):
                            print(self.name + " does not have enough cash to make this raise but can make a lower one")
                            self.bettingPrompt() # recursive retry
                        else:
                            self.raisable = False # a player only gets one chance to raise in a bettin round
                            self.funds -= (bet - self.playerBet) # subtracting difference from player funds
                            self.playerBet, currentBet = bet # updating current bet and player bet
                            return currentBet # returning current bet to client
                    else:
                        print("Your raise must be at least current bet + big blind (" + str(limit)+ ")")
                        self.bettingPrompt() # recursive retry
            else:
                print("invalid input")
                self.bettingPrompt()
