from gameGlobals import *
from player import Player
from gameScoring import Logic
from game import Game
# a = [[1,3],[2,4],[3,3],[7,1],[1,1]]

# print(a)
# a.sort(key = lambda x: x[1])
# print(a)
# a.sort(key = lambda x: x[0])
# print(a)

hand = [14,1],[7,2]
c_cards = [5,1],[3,1],[6,1],[12,1],[4,4]
# c = c_cards + hand
# print(c)
# creating a dictionary of player objects 

# players = {dude: Player(dude) for dude in PLAYER_NAMES} 
# playerList = list(players)
# lineUp = PLAYER_NAMES
# testGame = Game(players, lineUp)
# testGame.dealHands()

shortHand = list(hand + c_cards)
shortHand.sort(key = lambda x: x[1]) # first sort by suit
shortHand.sort(key = lambda x: x[0], reverse = True) # second sort by kind (descending)

if shortHand[0][0] == 14: # if there is an Ace, represent it as high and low
    lowAce = ([1, shortHand[0][1]])
    # self.cards = list(self.cards + lowAce)
    shortHand.append(lowAce)
cardVal = -1
highCard = -1
sequence = 1
discard = []
for i in range(len(shortHand) - 1):
    if shortHand[i][0] == (shortHand[i+1][0]+1):
        sequence += 1
        highCard = max(shortHand[i][0], highCard)
    else:
        discard.append(shortHand[i])

print("sequence: " + str(sequence))
print(shortHand)
print(discard)

# testLogic = Logic(c_cards, hand)
# pairs = testLogic.checkLike()
# print("pairs: " + str(pairs))
# flush = testLogic.checkFlush()
# print("flush: " + str(flush))
# straight = testLogic.checkSeq()
# print("straight: " + str(straight))