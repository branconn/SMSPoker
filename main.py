from gameGlobals import *
from player import Player
from game import Game

# creating a dictionary of player objects 
players = {dude: Player(dude) for dude in PLAYER_NAMES} 
playerList = list(players)
playOrder = lineUp = PLAYER_NAMES
wcCost = 0.0089 * (9*len(lineUp)-4) + 0.0058 * (10*len(lineUp)+4)
print("Worst-case cost-per-hand = $" + str(wcCost))    
stillFun = True
gameCount = 0
while stillFun:
    game = Game(players, lineUp)
    players = game.playGame()
    playOrder.append(playOrder.pop(0))
    lineUp = playOrder
    gameCount += 1
    if gameCount >= 2:
        stillFun = False
