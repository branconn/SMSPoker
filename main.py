from gameGlobals import *
from player import Player
from game import Game

# creating a dictionary of player objects 
players = {dude: Player(dude) for dude in PLAYER_NAMES} 
playerList = list(players)
playOrder = lineUp = PLAYER_NAMES  
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
