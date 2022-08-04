import message
from deck import Deck
from gameGlobals import *
from gameScoring import HandScore

class Game:
# a hand of poker is defined as a "Game" to prevent confusion with a player's "hand"
    def __init__(self, playerDetails, playOrder):
        self.playerDict = playerDetails
        self.lineUp = playOrder
        self.playStatus = "A hand has started."
        self.gameDeck = Deck()
        self.pot = 0
        self.currentBet = 0
        self.msgCount = 0
        for name in self.lineUp:
            self.playerDict[name].hand = []
            self.playerDict[name].playerBet = 0
            self.playerDict[name].raisable = True

    def dealHands(self):
    # assigns two cards to each player, removes cards from deck
        message.commLine("\n\n")
        for name in self.lineUp:
            self.playerDict[name].hand.append(self.gameDeck.draw())
            self.playerDict[name].hand.append(self.gameDeck.draw())
            message.commLine(self.playerDict[name].name)
            message.commLine(self.playerDict[name].hand[0].name + " " + self.playerDict[name].hand[1].name)

    def informPlayer(self):
        ccStatus = self.gameDeck.present()
        smsTxt = self.playStatus +"\nPot: " + str(self.pot) + " // Current bet: " + str(self.currentBet) + "\n" +  ccStatus + "\n" 
        message.commLine(smsTxt)
        self.msgCount += 1

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

    def bettingRound(self, bettingRound):
    # manages one round of betting until all players are either removed from play or have matching bets
        if len(self.lineUp) > 1:
            message.commLine("\n---------------------")
            message.commLine("Betting round: " + bettingRound + "\n")
            if bettingRound != ROUNDS[0]:
                self.ccStatus = self.gameDeck.present()
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
                            self.playerDict[name].funds -= SMALL_BLIND
                            self.pot += SMALL_BLIND
                            self.playStatus = name + " posted small blind of " + str(SMALL_BLIND)
                            self.informPlayer()
                        else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                    elif (name == self.lineUp[1]) & (bettingRound==ROUNDS[0]) & (not reconcileRaise):
                        if self.playerDict[name].sufficientFunds(BIG_BLIND): # checks if player can post blind
                            self.playerDict[name].playerBet = BIG_BLIND
                            self.currentBet = BIG_BLIND
                            self.playerDict[name].funds -= BIG_BLIND
                            self.pot += BIG_BLIND
                            self.playStatus = name + " posted big blind of " + str(BIG_BLIND)
                        else: self.lineUp.remove(name) # if player cannot post blind, removed from lineUp
                    else:
                        # possibly the most unclear conditional statement ever written?
                        if (not (secondRound and not self.playerDict[name].raisable and (self.playerDict[name].playerBet == self.currentBet))):
                            print("\n\n\n\n\n\n\n\n") # this is only here for command line testing
                            message.commLine("Betting round: " + bettingRound + "\n")
                            self.informPlayer()
                            playerIncrementalBet = self.playerDict[name].bettingPrompt(self.currentBet, 0)
                            if playerIncrementalBet < 0: #player folds (no addition to pot)
                                self.playStatus = name + " folded."
                                quitters.append(name)
                            elif playerIncrementalBet == 0: #player checks (no addition to pot)
                                self.playStatus = name + " checked."      
                            elif playerIncrementalBet > 0: #player calls or raises (addition to pot)
                                if self.playerDict[name].playerBet == self.currentBet:
                                    self.playStatus = name + " called bet of " + str(self.currentBet)
                                    self.pot += playerIncrementalBet 
                                elif self.playerDict[name].playerBet > self.currentBet:
                                    self.currentBet = self.playerDict[name].playerBet
                                    self.pot += playerIncrementalBet
                                    self.playStatus = name + " raised bet to " + str(self.currentBet)
                                else:
                                    message.commLine("Error: playerBet is bigger than currentBet and was not flagged")
                    self.msgCount += self.playerDict[name].plrMsgCount
                    self.playerDict[name].plrMsgCount = 0
                for quitter in quitters:
                    if (quitter in self.lineUp): 
                        self.lineUp.remove(quitter)
                if self.bettingResolved():
                    anotherRound = False
                else:
                    anotherRound = True
                    secondRound = True
                    reconcileRaise = True

            message.commLine("Betting round is done")

    def getBestHands(self):
        gameResults = []
        for name in self.lineUp:
            handScore = HandScore(self.gameDeck.communityCards, self.playerDict[name].hand)
            gameResults.append([name, handScore.bestPlay()])
        gameResults.sort(key = lambda x: x[1], reverse = True)
        return gameResults

    def distributePot(self):
        if len(self.lineUp) == 1:
            message.commLine(self.lineUp[0] + " is awarded " + str(self.pot) + " from the pot.")
            self.playerDict[self.lineUp[0]].funds += self.pot
        else: 
            bestHands = self.getBestHands()
            for playerHand in bestHands:
                message.commLine(playerHand[0] + 
                " has " + 
                KINDS[playerHand[1][1]-2] + 
                " high " + 
                HANDS[playerHand[1][0]])
            print("......")
            message.commLine(bestHands[0][0] + 
                " won with " + 
                KINDS[bestHands[0][1][1]-2] + 
                " high " + 
                HANDS[bestHands[0][1][0]] + 
                " and is awarded " + str(self.pot) + " from the pot.")
            self.playerDict[bestHands[0][0]].funds += self.pot
        self.pot = 0
        self.msgCount += len(self.playerDict)
        print("Message count: " + str(self.msgCount))

    def resetGame(self):
        for player in self.playerDict:
            player.hand = []
            player.playerBet = 0
            player.raisable = True

    def playGame(self):
        self.dealHands()
        self.bettingRound(ROUNDS[0])
        self.gameDeck.flip(3) # flop
        self.bettingRound(ROUNDS[1])
        self.gameDeck.flip(1) # turn
        self.bettingRound(ROUNDS[2])
        self.gameDeck.flip(1) # river
        self.bettingRound(ROUNDS[3])
        self.distributePot()
        
        return self.playerDict

#     gameDealer = players[playerList[gameCount%len(PLAYER_NAMES)]]
#     message.commLine(gameDealer.name)
#     gameCount += 1
#     if gameCount >= 10:
#         stillFun = False
# message.commLine(gameCount)
