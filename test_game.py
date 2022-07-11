import unittest
from unittest import mock
import deck
import game
import player

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
    
    @mock.patch('player.input', create = True)
    def test_auto_fold(self, mocked_input):
        mocked_input.side_effect = ['10','idk','ten']
        result = self.testPlayer.bettingPrompt(30, 0)
        self.assertEqual(result, -1, "Should 'auto-fold' after three attempts")





if __name__ == '__main__':
    unittest.main()
