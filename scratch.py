# from gameGlobals import *
# from player import Player
# from gameScoring import Logic
# from game import Game
# a = [[1,3],[2,4],[3,3],[7,1],[1,1]]
import deck
import player
import gameScoring
#-----------------------
#initializing test player and deck for scoring
# test_deck = deck.Deck()
# test_deck.flip(5)
# test_player = player.Player("Test Case")
# test_player.hand.append(test_deck.draw())
# test_player.hand.append(test_deck.draw())
#-----------------------
#intializing test hands
testDeck = deck.Deck()
testCases = {
            "fourOfKindType0" : [["3D","9H","9D","9C","9S","4H","8S"],[7,9,8,0]],
            "fourOfKindType1" : [["3D","9H","9D","9C","9S","AH","AS"],[7,9,14,0]],
            "fourOfKindType2" : [["AD","9H","9D","9C","9S","AH","AS"],[7,9,14,0]],
            "fullHouseType0" : [["3D","3H","3C","9C","9S","4H","8S"],[6,3,9,8]],
            "fullHouseType1" : [["3D","3H","3C","9C","9S","9H","8S"],[6,9,3,8]],
            "fullHouseType2" : [["3D","3H","3C","9C","9S","9H","2S"],[6,9,3,3]],
            "fullHouseType3" : [["3D","3H","3C","9C","9S","10H","10S"],[6,3,10,9]],
            "flushType0" : [["3D","4C","3C","9C","9S","10C","JC"],[5,11,9,0]],
            "flushType1" : [["3D","7C","KC","9C","AC","10C","JC"],[5,14,7,0]],
            "flushType2" : [["3D","7D","KC","9C","AC","10C","JC"],[5,14,7,0]],
        }
testHand = testDeck.testHand(testCases["flushType2"][0])
testDeck.present(testHand)
scoring = gameScoring.HandScore(testHand[:5],testHand[5:])
print(scoring.checkLike())
print(scoring.checkFlush())


#-----------------------
# print(test_player.name)
# print(test_player.hand[0].name+" "+test_player.hand[1].name)
# print(str(test_player.hand[0].id)+" "+str(test_player.hand[1].id))
# print("K: "+str(test_player.hand[0].kind)+" "+str(test_player.hand[1].kind))
# print("S: "+str(test_player.hand[0].suit)+" "+str(test_player.hand[1].suit))
#-----------------------
#initializing test scoring object, passing in test player and deck
# test_score = gameScoring.HandScore(test_deck.communityCards, test_player.hand)
# test_score.sortCards()
# test_deck.present(test_score.cards)
# print("-------")
# test_score.checkLike()

# hand = [14,1],[7,2]
# c_cards = [5,1],[3,1],[6,1],[12,1],[4,4]
# # c = c_cards + hand
# # print(c)
# # creating a dictionary of player objects 

# # players = {dude: Player(dude) for dude in PLAYER_NAMES} 
# # playerList = list(players)
# # lineUp = PLAYER_NAMES
# # testGame = Game(players, lineUp)
# # testGame.dealHands()

# shortHand = list(hand + c_cards)
# shortHand.sort(key = lambda x: x[1]) # first sort by suit
# shortHand.sort(key = lambda x: x[0], reverse = True) # second sort by kind (descending)

# if shortHand[0][0] == 14: # if there is an Ace, represent it as high and low
#     lowAce = ([1, shortHand[0][1]])
#     # self.cards = list(self.cards + lowAce)
#     shortHand.append(lowAce)
# cardVal = -1
# highCard = -1
# sequence = 1
# discard = []
# for i in range(len(shortHand) - 1):
#     if shortHand[i][0] == (shortHand[i+1][0]+1):
#         sequence += 1
#         highCard = max(shortHand[i][0], highCard)
#     else:
#         discard.append(shortHand[i])

# print("sequence: " + str(sequence))
# print(shortHand)
# print(discard)

# testLogic = Logic(c_cards, hand)
# pairs = testLogic.checkLike()
# print("pairs: " + str(pairs))
# flush = testLogic.checkFlush()
# print("flush: " + str(flush))
# straight = testLogic.checkSeq()
# print("straight: " + str(straight))

num_levels = 6
