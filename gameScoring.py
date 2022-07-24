from gameGlobals import *
from deck import Card, Deck
"""
8000000 straightFlush = seq & flush
7000000 fourOfKind = like4
6000000 fullHouse = like3 remove& like2
5000000 flush = flush
4000000 straight = seq
3000000 threeOfKind = like3
2000000 twoPair = like2 remove& like2
1000000 onePair = like2 
N highCard = high

check for:
    sequence of at least 5 "seq"
    same suit of at least 5 "flush"
    same kind of at least 2 "like"
    high card "high"
"""
class HandScore:
    def __init__(self, c_cards, playerHand):
        self.cards = list(c_cards + playerHand)
        self.hands = {}
        # [best hand, high card 1, high card 2, high card 3, buffer]
        self.score = [0,0,0,0]

    def sortCards(self):
        self.cards.sort(key = lambda x: x.suit) # first sort by suit
        self.cards.sort(key = lambda x: x.kind, reverse = True) # second sort by kind (descending)
 
    def checkSeq(self, *args):
        prevCard = Card.dummy()
        highCard = 0
        kicker = 0
        sequence = 1
        straightScore = [0, 0, 0, 0]
        if len(args) == 1:
            copyHand = args[0]
            copyHand.sort(key = lambda x: x.kind, reverse = True)
        else:
            self.sortCards()
            copyHand = self.cards 
        for card in copyHand[:4]:     # if there is an Ace, represent it as high and low
            if card.kind == 14: 
                lowAce = Card(-1,card.suit)
                copyHand.append(lowAce)
        for index, card in enumerate(copyHand):
            if card.kind != prevCard.kind - 1:
                highPos = index
                highCard = card.kind
                sequence = 1
            else:
                sequence += 1
            if sequence == 5:
                break
            prevCard = card
        if sequence == 5:
            kickers = list(copyHand[:highPos] + copyHand[(highPos+5):])
            if copyHand[(highPos+4)].kind == 1:
                kickers = [x for x in kickers if x.name != copyHand[(highPos+4)].name]
            for card in kickers:
                kicker = max(kicker, card.kind)
            straightScore = [4, highCard, kicker, 0]
        return straightScore
    
    def checkLike(self):
        self.sortCards()
        tempDeck = self.cards
        pairs = []
        kicker = 0
        likeScore = [0,0,0,0]

        for index, card in enumerate(tempDeck):
            cardCount = sum(1 for c in tempDeck if c.kind == card.kind)
            if cardCount > 1 and card.kind != tempDeck[index-1].kind:
                pairs.append([cardCount, card.kind])
            elif cardCount == 1:
                kicker = max(kicker, card.kind)
        
        pairs.sort(key = lambda x: x[1], reverse = True) # sort by high card first (descending)
        pairs.sort(key = lambda x: x[0], reverse = True) # then re-sort by number of matches (descending)

        pairCount = len(pairs)
        if pairCount != 0:
            if pairs[0][0] == 4:                        # four of a kind (7)
                if pairCount > 1:                       # edge case: four of kind + additional pair
                    kicker = max(kicker, pairs[1][1])
                likeScore = [7,pairs[0][1],kicker,0]
            elif pairs[0][0] == 3:
                if pairCount > 1:                       # full house (6)
                    if pairs[1][0] > 2:                 # edge case: two three-of-kinds
                        kicker = max(kicker, pairs[1][1])
                    if pairCount > 2:                   # edge case: full house with additional pair
                        kicker = max(kicker, pairs[2][1])
                    likeScore = [6,pairs[0][1],pairs[1][1],kicker]
                else:                                   # three of a kind (3)
                    likeScore = [3,pairs[0][1],kicker,0]
            elif pairs[0][0] == 2:
                if pairCount > 1:                       # two pair (2)
                    if pairCount > 2:                   # edge case: three pairs
                        kicker = max(kicker, pairs[2][1])
                    likeScore = [2,pairs[0][1], pairs[1][1],kicker]
                else:                                   # one pair (1)
                    likeScore = [1,pairs[0][1],kicker,0]
        else:
            likeScore[1] = kicker
        return likeScore

    def checkFlush(self):
        self.cards.sort(key = lambda x: x.kind, reverse = True) # sort by kind initially (descending)
        self.cards.sort(key = lambda x: x.suit) # re-sort by suit
        likeSuitCount = 1
        prevCard = Card.dummy() # a dummy card is created for the intial comparison
        kicker = 0
        flushHigh = 0
        flushSuit = -1
        flushScore = straightFlushScore = [0,0,0,0]
        flushDeck = []
        
        for card in self.cards:
            if card.suit == prevCard.suit:
                likeSuitCount += 1
                flushHigh = max(flushHigh, prevCard.kind)
                if likeSuitCount > 4:                # if there is a flush
                    flushSuit = card.suit       # then note the flush suit
                if likeSuitCount > 5:
                    kicker = max(kicker, card.kind)
            elif likeSuitCount < 5:                  # if current suits don't match and a flush has not been established:
                likeSuitCount = 1                    # reset flush count
                flushHigh = 0                   # reset high card
            else:
                break
            prevCard = card

        if flushSuit != -1:                     # if there is a flush
            for card in self.cards:             # then identify the kicker
                if card.suit != flushSuit:
                    kicker = max(kicker, card.kind)
                else:
                    flushDeck.append(card)
            straightFlushScore = self.checkSeq(flushDeck)
            if straightFlushScore[0] == 4:
                straightFlushScore[0] = 8
                straightFlushScore[2] = max(kicker, straightFlushScore[2])
                flushScore = straightFlushScore
            else:
                flushScore = [5,flushHigh,kicker,0]
        return flushScore

    def bestPlay(self):
        highScore = max(self.checkFlush(), self.checkSeq(), self.checkLike())
        self.score = highScore
        return self.score


    