import message
from gameGlobals import *

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.funds = BUY_IN # total amount that the player has not allocated to the pot
        self.playerBet = 0 # total amount that the player has contributed to the pot
        self.raisable = True # tracks whether a player can still raise during a betting round
        self.plrMsgCount = 0

    def sufficientFunds(self, query): # checking if an input is smaller than the (funds + bet) of player
        return (query <= self.funds + self.playerBet)

    def bettingPrompt(self, currentBet, attempts):
        handPrint = " ".join(c.name for c in self.hand)
        details = self.name + "..\n" + handPrint + "\nYour bet: " + str(self.playerBet) + " // Your funds: " + str(self.funds)
        if not self.sufficientFunds(currentBet):
            # TODO: implement sidepot
            message.commLine(self.name + " does not have enough cash to continue")
            self.plrMsgCount += 1
            return False
        elif attempts >= 2:
            message.commLine("Too many incorrect entries. Automatic fold.")
            self.plrMsgCount += 1
            return -1
        else:
            if self.raisable:
                
                answer = message.inputCL(details + "\nFold [f], call/check " + str(currentBet-self.playerBet) + " [c], or raise bet to N [rN]?")
            else:
                answer = message.inputCL(details + "\nYou can no longer raise. Fold [f] or call/check " + str(currentBet-self.playerBet) + " [c]?")
            self.plrMsgCount += 1
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
                    message.commLine("Input format for a raise should be 'r[Amount]', e.g. 'r15'\nRaise amount cannot be lower than current bet + big blind")
                    self.plrMsgCount += 1
                    incremental = self.bettingPrompt(currentBet,attempts+1) # recursive retry
                    return incremental
                else:
                    limit = currentBet + BIG_BLIND
                    if bet >= limit:
                        if not self.sufficientFunds(bet):
                            message.commLine(self.name + " does not have enough cash to make this raise but can make a lower one")
                            self.plrMsgCount += 1
                            incremental = self.bettingPrompt(currentBet, attempts+1) # recursive retry
                            return incremental
                        else:
                            self.raisable = False # a player only gets one chance to raise in a bettin round
                            incremental = bet - self.playerBet
                            self.playerBet = bet # setting player's bet to their raise amount
                            self.funds -= incremental # subtracting difference from player funds
                            return incremental # returning incremental addition to the pot
                    else:
                        message.commLine("Your raise must be at least current bet + big blind (" + str(limit)+ ")")
                        self.plrMsgCount += 1
                        incremental = self.bettingPrompt(currentBet, attempts+1) # recursive retry
                        return incremental
            else:
                message.commLine("invalid input")
                self.plrMsgCount += 1
                incremental = self.bettingPrompt(currentBet, attempts+1)
                return incremental
