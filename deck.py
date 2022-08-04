from gameGlobals import *
import random
import message
# terms: community cards, flop, turn, river

class Card:
    ### The Card class defines the attributes of a card, namely the <int>kind, <int>suit, and <String>name used for player readability
    def __init__(self, kindInt, suitInt, fae=0):
        self.suit = suitInt - fae
        self.kind = kindInt + 2 - fae * 3
        self.id = suitInt * NUM_KINDS + kindInt
        self.name = KINDS[kindInt] + SUITS[suitInt]
    @classmethod
    def dummy(cls):
        return cls(0,0,1)
class Deck:
    def __init__(self, shuffled=True):
        self.unplayedCards = []
        self.communityCards = []
        self.cardDict = {}
        for kIndex in range(NUM_KINDS):
            for sIndex in range(NUM_SUITS):
                newCard = Card(kIndex, sIndex)
                self.unplayedCards.append(newCard)
        if shuffled:
            self.shuffle() # the deck is shuffled on initialization
        for ind, card in enumerate(self.unplayedCards):
            self.cardDict[card.name] = ind

    @classmethod
    def ordered(cls):
        return cls(False)

    def shuffle(self):
        random.shuffle(self.unplayedCards)

    def draw(self):
        return (self.unplayedCards.pop(0))

    def flip(self, times):
        for i in range(times):
            self.communityCards.append(self.draw())

    def present(self):
        cardsStr = " ".join(o.name for o in self.communityCards)
        unflippedStr = " ".join(["[]"] * (5-len(self.communityCards)))
        cardsStr = cardsStr + " " + unflippedStr
        return cardsStr

    def testHand(self, cardList):
        hand = []
        for cardStr in cardList:
            index = self.cardDict[cardStr]
            hand.append(self.unplayedCards[index])
        return hand

# deck_1 = Deck()
# deck_1.present()
# print(deck_1.deal())
# print(len(deck_1.unplayed_cards))

