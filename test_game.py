import unittest
from unittest import mock
import deck
import game
import player
import gameScoring

class DeckTestCase(unittest.TestCase):
    def setUp(self):
        self.testDeck = deck.Deck()

    def tearDown(self):
       pass

    def checkDuplicates(self):
        setOfDeck = set()
        for cardObj in self.testDeck.unplayedCards:
            if cardObj in setOfDeck:
                return True
            else:
                setOfDeck.add(cardObj)
        return False

    def test_deck_duplicates(self):
        self.assertFalse(self.checkDuplicates(),"Should contain no duplicates")

    def test_deck_length(self):
        self.assertEqual(len(self.testDeck.unplayedCards), 52, "Should be 52")

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.testPlayer = player.Player("Johnathan Cromwell")

    def test_insufficient_funds(self):
        self.testPlayer.funds = 10
        self.assertFalse(self.testPlayer.bettingPrompt(self.testPlayer.funds + 1, 0))
    
    @mock.patch('player.message.inputCL', create = True)
    def test_auto_fold(self, mocked_input):
        mocked_input.side_effect = ['10','idk','ten']
        result = self.testPlayer.bettingPrompt(30, 0)
        self.assertEqual(result, -1, "Should 'auto-fold' after three attempts")

class ScoringTestCase(unittest.TestCase):
    def setUp(self):
        self.testDeck = deck.Deck.ordered() # instantiate an ordered deck
        self.testCases = {
            "straightFlushType0" : [["3D","7C","8C","9C","AH","10C","JC"],[8,11,14,0]],
            "straightFlushType1" : [["3D","7C","8C","9C","AC","10C","JC"],[8,11,14,0]],
            "straightFlushType2" : [["3D","7C","8C","9C","6C","10C","JC"],[8,11,6,0]],
            "fourOfKindType0" : [["3D","9H","9D","9C","9S","4H","8S"],[7,9,8,0]],
            "fourOfKindType1" : [["3D","9H","9D","9C","9S","AH","AS"],[7,9,14,0]], # with additional pair
            "fourOfKindType2" : [["AD","9H","9D","9C","9S","AH","AS"],[7,9,14,0]], # with additional ToK
            "fullHouseType0" : [["3D","3H","3C","9C","9S","4H","8S"],[6,3,9,8]], 
            "fullHouseType1" : [["3D","3H","3C","9C","9S","9H","8S"],[6,9,3,8]], # as two ToKs
            "fullHouseType2" : [["3D","3H","3C","9C","9S","9H","2S"],[6,9,3,3]], # as two ToKs w/ affected kicker
            "fullHouseType3" : [["3D","3H","3C","9C","9S","10H","10S"],[6,3,10,9]], # with additional pair
            "flushType0" : [["3D","4C","3C","9C","9S","10C","JC"],[5,11,9,0]],
            "flushType1" : [["3D","7C","KC","9C","AC","10C","JC"],[5,14,7,0]], # with a sixth like suit affecting kicker
            "flushType2" : [["3D","7D","KC","9C","AC","10C","JC"],[5,14,7,0]], 
            "straightType0" : [["QD","7D","KH","5C","AC","10C","JD"],[4,14,7,0]],
            "straightType1" : [["2D","7D","4H","3C","AC","10C","5D"],[4,5,10,0]], # with ace used as low card
            "straightType2" : [["2D","AD","4H","3C","AC","10C","5D"],[4,5,14,0]], # with ace used as low card and additonal ace
            "straightType3" : [["6D","7D","4H","9C","8C","5C","2D"],[4,9,4,0]], # with run of > 5 affecting kicker
            "straightType4" : [["AD","KD","4H","6C","8C","5C","7D"],[4,8,14,0]], # with a false run affecting kicker
            "threeOfKindType0" : [["3D","3H","3C","10C","9S","4H","8S"],[3,3,10,0]], 
            "twoPairType0" : [["3D","3H","4C","10C","9S","4H","8S"],[2,4,3,10]],
            "twoPairType1" : [["3D","3H","4C","10C","10S","4H","8S"],[2,10,4,8]], # with additional pair
            "twoPairType2" : [["3D","3H","4C","10C","10S","4H","2S"],[2,10,4,3]], # with additional pair w/ affected kicker
            "pairType0" : [["3D","KS","KH","6C","2C","JC","7D"],[1,13,11,0]],
            "pairType1" : [["3D","KS","KH","6C","2C","AC","7D"],[1,13,14,0]],
            "highCardType0" : [["3D","KS","4H","6C","2C","JC","7D"],[0,13,0,0]],
        }

    def test_like_scoring(self):    
        for case in self.testCases:
            hand = self.testDeck.testHand(self.testCases[case][0])
            scoring = gameScoring.HandScore(hand[:5],hand[5:])
            self.assertEqual(scoring.bestPlay(),self.testCases[case][1], "Check testCases")





if __name__ == '__main__':
    unittest.main()
