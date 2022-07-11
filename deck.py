from gameGlobals import *
import random
# terms: community cards, flop, turn, river

class Card:
    ### The Card class defines the attributes of a card, namely the <int>kind, <int>suit, and <String>name used for player readability
    def __init__(self, kindInt, kindStr, suitInt, suitStr):
        self.suit = suitInt
        self.kind = kindInt
        self.id = suitInt * NUM_KINDS + kindInt
        self.name = kindStr + suitStr
class Deck:
    def __init__(self):
        self.unplayedCards = []
        self.communityCards = []
        # for k in range(NUM_KINDS): # creating the deck as a nested list
        #     for s in range(NUM_SUITS):
        #         card = [k, s] # cards are defined as a list of kind and suit
        #         newCard = Card(k, s)
        #         self.unplayedCards.append(newCard)
        for kIndex , kTxt in enumerate(KINDS):
            for sIndex , sTxt in enumerate(SUITS):
                newCard = Card(kIndex, kTxt, sIndex, sTxt)
                self.unplayedCards.append(newCard)
        self.shuffle() # the deck is shuffled on initialization
        
    def shuffle(self):
        random.shuffle(self.unplayedCards)

    def draw(self):
        return (self.unplayedCards.pop(0))

    def flip(self, times):
        for i in range(times):
            self.communityCards.append(self.draw())

    def present(self):
        for card in self.unplayedCards:
            print(card.id)


# deck_1 = Deck()
# deck_1.present()
# print(deck_1.deal())
# print(len(deck_1.unplayed_cards))

