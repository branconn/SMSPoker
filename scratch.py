from gameGlobals import *
from player import Player
from gameLogic import Logic
from game import Game
# a = [[1,3],[2,4],[3,3],[7,1],[1,1]]

# print(a)
# a.sort(key = lambda x: x[1])
# print(a)
# a.sort(key = lambda x: x[0])
# print(a)

hand = [14,1],[5,2]
c_cards = [5,1],[3,1],[2,1],[12,1],[4,4]
# c = c_cards + hand
# print(c)
# creating a dictionary of player objects 

# players = {dude: Player(dude) for dude in PLAYER_NAMES} 
# playerList = list(players)
# lineUp = PLAYER_NAMES
# testGame = Game(players, lineUp)
# testGame.dealHands()

testLogic = Logic(c_cards, hand)
pairs = testLogic.checkLike()
print("pairs: " + str(pairs))
flush = testLogic.checkFlush()
print("flush: " + str(flush))
straight = testLogic.checkSeq()
print("straight: " + str(straight))