# PLAYER_NAMES = ["gusto", "camelot", "e-man", "bcon", "kareem abdul-jabbar"]
PLAYER_NAMES = input("Who is playing?").split(" ")
BUY_IN = 100
SMALL_BLIND = 5
BIG_BLIND = 2 * SMALL_BLIND
KINDS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
NUM_KINDS = len(KINDS)
SUITS = ["C", "H", "S", "D"]
NUM_SUITS = len(SUITS)
ROUNDS = ["Pre-flop", "Flop", "Turn", "River"]
HANDS = [
    "", 
    "pair", 
    "two pair",
    "three of kind",
    "straight",
    "flush",
    "full house",
    "four of kind",
    "straight flush"
    ]