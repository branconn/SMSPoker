from player import Player
from deck import Deck
from gameGlobals import *
import gameLogic

class Game:
# a hand of poker is defined as a "Game" to prevent confusion with a player's "hand"
    def __init__(self, table, playOrder):
        self.playerDict = table
        self.lineUp = playOrder
        self.status = "This hand has started"
        self.gameDeck = Deck()
        self.pot = 0
        self.currentBet = 0
        for name in self.lineUp:
            self.playerDict[name].hand = []

    def dealHands(self):
    # assigns two cards to each player, removes cards from deck
        for name in self.lineUp:
            self.playerDict[name].hand.append(self.gameDeck.draw())
            self.playerDict[name].hand.append(self.gameDeck.draw())
            print(self.playerDict[name].name)
            print(self.playerDict[name].hand)
        print(len(self.gameDeck.unplayedCards))

    def resetPlayers(self):
    # resets the ability of players to raise
        for name in self.lineUp:
            self.playerDict[name].raisable = True

    def bettingResolved(self):
    # checks if the bets of all active players equals the currentBet
        resolved = True
        for name in self.lineUp:
            if self.currentBet != self.playerDict[name].playerBet:
                resolved = False
        return resolved

# TODO: currentBet and playerBets should carry through the whole Game
    def bettingRound(self, isPreBet):
    # manages one round of betting until all players are either removed from play or have matching bets
        iter = 0
        self.resetPlayers()
        anotherRound = True
        while anotherRound: # Each player gets one chance to raise. Afterwards, the options are call/check & fold 
            for name in self.lineUp:
                if (isPreBet): # in the first round, 1st and 2nd betters post automatic blind bets
                    if name == self.lineUp[0]:
                        if self.playerDict[name].sufficientFunds(SMALL_BLIND): # checks if player can post blind
                            self.playerDict[name].playerBet = SMALL_BLIND
                            self.currentBet = SMALL_BLIND
                            self.pot += SMALL_BLIND
                            self.status = name + " posted small blind of " + str(SMALL_BLIND)
                        else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                    if name == self.lineUp[1]:
                        if self.playerDict[name].sufficientFunds(BIG_BLIND): # checks if player can post blind
                            self.playerDict[name].playerBet = BIG_BLIND
                            self.currentBet = BIG_BLIND
                            self.pot += BIG_BLIND
                            self.status = name + " posted big blind of " + str(BIG_BLIND)
                        else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                else:
                    playerBet = self.playerDict[name].bettingPrompt(self.currentBet, self.status)
                    if not playerBet:
                        self.status = name + " folded."
                        self.lineUp.remove(name)
                    if playerBet == currentBet:
                        if currentBet == 0:
                            self.status = name + " checked."
                        else:
                            self.status = name + " called bet of " + str(self.currentBet)
                            self.pot += playerBet
                    if playerBet > currentBet:
                        currentBet = playerBet
                        self.pot += playerBet
                        self.status = name + " raised bet to " + str(self.currentBet)
                        i = 0
            if self.bettingResolved():
                anotherRound = False
            else:
                anotherRound = True
        print("Betting round is done")

    def getBestHands(self):
        for name in self.lineUp:
            self.playerDict[name]


    def winningHand(self):
        pass

    def distributePot(self):
        for name in self.lineUp:
            self.playerDict[name].playerBet = 0


    def playGame(self):
        self.dealHands()
        self.bettingRound(True)
        self.gameDeck.flip(3) # flop
        self.bettingRound(False)
        self.gameDeck.flip(1) # turn
        self.bettingRound(False)
        self.gameDeck.flip(1) # river
        self.bettingRound(False)
        self.getBestHands(self.gameDeck.communityCards)
        
        return self.playerDict


        

#     gameDealer = players[playerList[gameCount%len(PLAYER_NAMES)]]
#     print(gameDealer.name)
#     gameCount += 1
#     if gameCount >= 10:
#         stillFun = False
# print(gameCount)
