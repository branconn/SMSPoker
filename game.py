from player import Player
from deck import Deck
from gameGlobals import *
from gameScoring import HandScore

class Game:
# a hand of poker is defined as a "Game" to prevent confusion with a player's "hand"
    def __init__(self, playerDetails, playOrder):
        self.playerDict = playerDetails
        self.lineUp = playOrder
        self.status = "This hand has started"
        self.gameDeck = Deck()
        self.pot = 0
        self.currentBet = 0
        for name in self.lineUp:
            self.playerDict[name].hand = []

    def dealHands(self):
    # assigns two cards to each player, removes cards from deck
        print("\n\n")
        for name in self.lineUp:
            self.playerDict[name].hand.append(self.gameDeck.draw())
            self.playerDict[name].hand.append(self.gameDeck.draw())
            print(self.playerDict[name].name)
            print(self.playerDict[name].hand)

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

    # def playerSettled(self, playerName):
    # # returns whether a player should be called upon to f/c/r
    #     if self.currentBet != self.playerDict[playerName].playerBet:
    #         return False
    #     elif 

# TODO: bug: if all checks in first round, game still does second round.. ReconcileRaise should be handed per player instance
    def bettingRound(self, bettingRound):
    # manages one round of betting until all players are either removed from play or have matching bets
        print("\n---------------------")
        print("Betting round: " + bettingRound + "\n")
        if bettingRound != ROUNDS[0]:
            print(self.gameDeck.communityCards)
        self.resetPlayers()
        anotherRound = True
        secondRound = False
        reconcileRaise = False
        quitters = []
        while anotherRound: # Each player gets one chance to raise. Afterwards, the options are call/check & fold 
            for name in self.lineUp:
# in the first round, 1st and 2nd betters post automatic blind bets
                if (name == self.lineUp[0]) & (bettingRound==ROUNDS[0]) & (not reconcileRaise):
                    if self.playerDict[name].sufficientFunds(SMALL_BLIND): # checks if player can post blind
                        self.playerDict[name].playerBet = SMALL_BLIND
                        self.currentBet = SMALL_BLIND
                        self.pot += SMALL_BLIND
                        self.status = name + " posted small blind of " + str(SMALL_BLIND)
                        print(self.status)
                    else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                elif (name == self.lineUp[1]) & (bettingRound==ROUNDS[0]) & (not reconcileRaise):
                    if self.playerDict[name].sufficientFunds(BIG_BLIND): # checks if player can post blind
                        self.playerDict[name].playerBet = BIG_BLIND
                        self.currentBet = BIG_BLIND
                        self.pot += BIG_BLIND
                        self.status = name + " posted big blind of " + str(BIG_BLIND)
                    else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                else:
                    # possibly the most unclear conditional statement ever written?
                    if (not (secondRound and not self.playerDict[name].raisable and (self.playerDict[name].playerBet == self.currentBet))):
                        print(self.status)
                        playerIncrementalBet = self.playerDict[name].bettingPrompt(self.currentBet, 0)
                        if playerIncrementalBet < 0: #player folds (no addition to pot)
                            self.status = name + " folded."
                            quitters.append(name)
                        elif playerIncrementalBet == 0: #player checks (no addition to pot)
                            self.status = name + " checked."      
                        elif playerIncrementalBet > 0: #player calls or raises (addition to pot)
                            if self.playerDict[name].playerBet == self.currentBet:
                                self.status = name + " called bet of " + str(self.currentBet)
                                self.pot += playerIncrementalBet 
                            elif self.playerDict[name].playerBet > self.currentBet:
                                self.currentBet = self.playerDict[name].playerBet
                                self.pot += playerIncrementalBet
                                self.status = name + " raised bet to " + str(self.currentBet)
                            else:
                                print("Error: playerBet is bigger than currentBet and was not flagged")
            for quitter in quitters:
                if (quitter in self.lineUp): 
                    self.lineUp.remove(quitter)
            if self.bettingResolved():
                anotherRound = False
            else:
                anotherRound = True
                secondRound = True
                reconcileRaise = True

        print("Betting round is done")

    def getBestHands(self):
        gameResults = {name: HandScore(self.gameDeck.communityCards, self.playerDict[name].hand) for name in self.lineUp}

    def winningHand(self):
        pass

    def distributePot(self):
        for name in self.lineUp:
            self.playerDict[name].playerBet = 0


    def playGame(self):
        self.dealHands()
        self.bettingRound(ROUNDS[0])
        self.gameDeck.flip(3) # flop
        self.bettingRound(ROUNDS[1])
        self.gameDeck.flip(1) # turn
        self.bettingRound(ROUNDS[2])
        self.gameDeck.flip(1) # river
        self.bettingRound(ROUNDS[3])
        self.getBestHands(self.gameDeck.communityCards)
        
        return self.playerDict

#     gameDealer = players[playerList[gameCount%len(PLAYER_NAMES)]]
#     print(gameDealer.name)
#     gameCount += 1
#     if gameCount >= 10:
#         stillFun = False
# print(gameCount)
