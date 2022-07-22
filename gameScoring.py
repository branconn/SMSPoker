from gameGlobals import *
from deck import Card
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
 
    # TODO: update methods to handle Card objects
    def checkSeq(self):
        self.sortCards()
        for card in self.cards:
            if card.kind == 12: # if there is an Ace, represent it as high and low
                lowAce = Card(-1,card.suit)
                self.cards.append(lowAce)
        cardVal = -1
        highCard = -1
        sequence = 1
        shortHand = self.cards
        discard = []
        for i in range(shortHand - 1):
            if shortHand[i] == shortHand[i+1]-1:
                sequence += 1
                highCard = max(shortHand[i], highCard)
            elif sequence >= 5:
                discard.append(shortHand.pop(i))
        for card in shortHand:
            if card[0] == cardVal - 1:
                sequence += 1
                highCard = max(cardVal, highCard)
            elif sequence < 5: # if the current card doesn't match the previous, and a straight is not made, reset sequence value
                sequence = 1
                highCard = -1
            cardVal = card[0]
        if sequence >= 5:
            return highCard
        else:
            return -1
    
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
        self.cards.sort(key = lambda x: x.suit) # re-sort by suit
        likeSuit = 1
        prevCard = Card.dummy() # a dummy card is created for the intial comparison
        kicker = 0
        flushHigh = 0
        flushSuit = -1
        flushScore = [0,0,0,0]
        for card in self.cards:
            if card.suit == prevCard.suit:
                likeSuit += 1
                flushHigh = max(flushHigh, prevCard.kind)
                if likeSuit > 4:                # if there is a flush
                    flushSuit = card.suit       # then note the flush suit
                if likeSuit > 5:
                    kicker = max(kicker, card.kind)
            elif likeSuit < 5:                  # if current suits don't match and a flush has not been established:
                likeSuit = 1                    # reset flush count
                flushHigh = 0                   # reset high card
            prevCard = card

        if flushSuit != -1:                     # if there is a flush
            for card in self.cards:             # then identify the kicker
                if card.suit != flushSuit:
                    kicker = max(kicker, card.kind)
            flushScore = [5,flushHigh,kicker,0]
        return flushScore

    # TODO: update methods to handle Card objects
    def checkHigh(self):
        self.cards.sort(key = lambda x: x[0])
        return self.cards[0][0]
    
    def highCard(cardArray):
        cardArray.sort(key = lambda x: x.kind, reverse = True)
        return cardArray[0]

    def bestPlay(self):
        
        high = self.checkHigh()
        
        ofKind = self.checkLike()
        if ofKind[0][0] == 4:
            score = 7000000 + 10000 * ofKind[0][1]
            desc = "4 of kind, " + KINDS[ofKind[0][1]] + "s"
            self.hands[score] = desc
        elif ofKind[0][0] == 3 & ofKind[1][0] == 2:
            score = 6000000 + 10000 * ofKind[0][1]
            desc = "full house, " + KINDS[ofKind[0][1]] + "s and " + KINDS[ofKind[1][1]] + "s"
            self.hands[score] = desc
        elif ofKind[0][0] == 3:
            score = 3000000 + 10000 * ofKind[0][1]
            desc = "3 of kind, " + KINDS[0][1] + "s"
        elif ofKind[0][0] == 2 & ofKind[1][0] == 2:
            ofKind.sort(key = lambda x: x[1])
            # if highest pair matches, win is decided by other pair, if both match, win is decided by high card
            score = 2000000 + 10000 * ofKind[0][1] + 100 * ofKind[1][1] + 1 * high
            desc = "two pair, " + KINDS[ofKind[0][1]] + "s and " + KINDS[ofKind[1][1]] + "s"
        elif ofKind[0][0] == 2:
            score = 1000000 + ofKind[0][1] + 10000 * high

        flush = self.checkFlush()


        for score in self.hands:
            maxScore = max(score, maxScore)
        return {maxScore : self.hands[maxScore]}

    #strike this from this class
    def winningHand(self, playerHands):
        pass

    