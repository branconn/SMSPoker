import deck
from gameGlobals import *

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.funds = BUY_IN # total amount that the player has not allocated to the pot
        self.playerBet = 0 # total amount that the player has contributed to the pot
        self.raisable = True # tracks whether a player can still raise during a betting round

    def sufficientFunds(self, query): # checking if an input is smaller than the (funds + bet) of player
        return (query <= self.funds + self.playerBet)

    def bettingPrompt(self, currentBet, attempts):
        if not self.sufficientFunds(currentBet):
            # TODO: implement sidepot
            print(self.name + " does not have enough cash to continue")
            return False
        elif attempts >= 2:
            print("Too many incorrect entries. Automatic fold.")
            return -1
        else:
            if self.raisable:
                answer = input(self.name + ", would you like to fold [f], call/check [c], or raise bet to N [rN]?")
            else:
                answer = input(self.name + ", you can no longer raise. Would you like to fold [f] or call/check [c]?")
            
            # player folds
            if answer == "f":
                return -1 # returning boolean flag to remove player from betting lineUp
            
            # player calls / checks
            elif answer == "c":
                self.raisable = False # a player only gets one chance to raise in a bettin round
                incremental = currentBet - self.playerBet
                self.funds -= incremental # subtracting incremental difference from player funds
                self.playerBet = currentBet # updating player bet to current bet
                return incremental # returning incremental addition to pot to client
            
            # player raises
            elif (answer[0] == "r") & (self.raisable): 
                try:
                    bet = int(answer[1:]) # checking if raise input is correct format
                except:
                    print("Input format for a raise should be 'r[Amount]', e.g. 'r15'\nRaise amount cannot be lower than current bet + big blind")
                    incremental = self.bettingPrompt(currentBet,attempts+1) # recursive retry
                    return incremental
                else:
                    limit = currentBet + BIG_BLIND
                    if bet >= limit:
                        if not self.sufficientFunds(bet):
                            print(self.name + " does not have enough cash to make this raise but can make a lower one")
                            incremental = self.bettingPrompt(currentBet, attempts+1) # recursive retry
                            return incremental
                        else:
                            self.raisable = False # a player only gets one chance to raise in a bettin round
                            incremental = bet - self.playerBet
                            self.playerBet = bet # setting player's bet to their raise amount
                            self.funds -= incremental # subtracting difference from player funds
                            return incremental # returning incremental addition to the pot
                    else:
                        print("Your raise must be at least current bet + big blind (" + str(limit)+ ")")
                        incremental = self.bettingPrompt(currentBet, attempts+1) # recursive retry
                        return incremental
            else:
                print("invalid input")
                incremental = self.bettingPrompt(currentBet, attempts+1)
                return incremental
