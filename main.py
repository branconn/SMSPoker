from gameGlobals import *
from player import Player
from game import Game

# creating a dictionary of player objects 
players = {dude: Player(dude) for dude in PLAYER_NAMES} 
playerList = list(players)
lineUp = PLAYER_NAMES
    
stillFun = True
gameCount = 0
while stillFun:
    # gameDealer = players[playerList[gameCount%len(PLAYER_NAMES)]]
    game = Game(players, lineUp)
    players = game.playGame()
    # game.dealHands()
    lineUp.append(lineUp.pop(0))
    # print(gameDealer.name)
    gameCount += 1
    if gameCount >= 2:
        stillFun = False


# for person in players:
#     print(players[person].funds)
