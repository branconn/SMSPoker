from gameGlobals import *

"""
800 straightFlush = seq & flush
700 fourOfKind = like4
600 fullHouse = like3 remove& like2
500 flush = flush
400 straight = seq
300 threeOfKind = like3
200 twoPair = like2 remove& like2
100 onePair = like2 
N highCard = high

check for:
    sequence of at least 5 "seq"
    same suit of at least 5 "flush"
    same kind of at least 2 "like"
    high card "high"
"""
class Logic:
    def __init__(self, c_cards, playerHand):
        self.cards = list(c_cards + playerHand)
        self.hands = {}
        print(self.cards)

    def sortCards(self):
        self.cards.sort(key = lambda x: x[1]) # first sort by suit
        self.cards.sort(key = lambda x: x[0], reverse = True) # second sort by kind (descending)

    def checkSeq(self):
        self.sortCards()
        if self.cards[0][0] == 14: # if there is an Ace, represent it as high and low
            lowAce = ([1, self.cards[0][1]])
            # self.cards = list(self.cards + lowAce)
            self.cards.append(lowAce)
        cardVal = -1
        highCard = -1
        sequence = 1
        for card in self.cards:
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
        print(self.cards)
        cardVal = -1
        like = [[1,-1],[1,-1]]
        likeInd = 0 # switches to second pair/kind after first
        for card in self.cards:
            if card[0] == cardVal:
                like[likeInd][0] += 1
                like[likeInd][1] = card[0]
            elif like[0][0] > 1:
                likeInd = 1

            cardVal = card[0]
        like.sort(key = lambda x: x[0])
        return like

    def checkFlush(self):
        self.cards.sort(key = lambda x: x[1]) # sort by suit
        likeSuit = 1
        prevCard = [-1, -1]
        highCard = -1
        for card in self.cards:
            if card[1] == prevCard[1]:
                likeSuit += 1
                highCard = max(highCard, prevCard[0])
            elif likeSuit < 5: # if current suits don't match and a flush has not been established:
                likeSuit = 1 # reset flush count
                highCard = -1 # reset high card
            prevCard = card
        if likeSuit >= 5:
            return highCard
        else:
            return -1
    
    def checkHigh(self):
        self.cards.sort(key = lambda x: x[0])
        return self.cards[0][0]

    def bestPlay(self):
        ofKind = self.checkLike()
        high = self.checkHigh()

        if ofKind[0][0] == 4:
            score = 700 + ofKind[0][1]
            desc = "4 of kind, " + KINDS[ofKind[0][1]] + "s"
            self.hands[score] = desc
        elif ofKind[0][0] == 3 & ofKind[1][0] == 2:
            score = 600 + ofKind[0][1]
            desc = "full house, " + KINDS[ofKind[0][1]] + "s and " + KINDS[ofKind[1][1]] + "s"
            self.hands[score] = desc
        elif ofKind[0][0] == 3:
            score = 300 + ofKind[0][1]
            desc = "3 of kind, " + KINDS[0][1] + "s"
        elif ofKind[0][0] == 2 & ofKind[1][0] == 2:
            ofKind.sort(key = lambda x: x[1])
            # if highest pair matches, win is decided by other pair, if both match, win is decided by high card
            score = 200 + 3 * ofKind[0][1] + 0.1 * ofKind[1][1] + 0.01 * high
            desc = "two pair, " + KINDS[ofKind[0][1]] + "s and " + KINDS[ofKind[1][1]] + "s"
        elif ofKind[0][0] == 2:
            score = 100 + ofKind[0][1] + 0.1 * high

    #strike this from this class
    def winningHand(self, playerHands):
        pass