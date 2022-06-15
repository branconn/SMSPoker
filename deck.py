from gameGlobals import *
import random
# terms: community cards, flop, turn, river

class Deck:
    def __init__(self):
        self.unplayedCards = []
        self.communityCards = []
        for k in range(2, NUM_KINDS+2): # creating the deck as a nested list
            for s in range(NUM_SUITS):
                card = [k, s] # cards are defined as a list of kind and suit
                self.unplayedCards.append(card)
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
            print(card)


# deck_1 = Deck()
# deck_1.present()
# print(deck_1.deal())
# print(len(deck_1.unplayed_cards))

