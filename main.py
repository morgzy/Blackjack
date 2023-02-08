"""
A simple blackjack game, interacting with the deck of cards API at www.deckofcardsapi.com
By Morgan Hopkins
2022

Planned updates:
GUI
Improved game loop
"""

import json
import requests

# Declare globals
playerHand = []
aiHand = []
sitting = False
aiSitting = False
round = 0

# using responses to get a new deck of cards
url = "https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
resp = requests.get(url)
print(resp) # Should return Response 200
newDeck = resp.content
newDeck = json.loads(newDeck)

# Get deck ID
deckID = newDeck["deck_id"]
print("Deck ID: ", deckID)

# Declaring the constant for the deck URL
DECK_URL = "https://www.deckofcardsapi.com/api/deck/"+deckID

# Methods
def draw(x, hand):
    """ Draw x cards"""
    draw = DECK_URL+"/draw/?count="+str(x)
    resp = requests.get(draw)
    cards = resp.content
    cards = json.loads(cards)
    for card in cards["cards"]:
        hand.append(card)

def count():
    """ Count remaining cards in deck """
    count = requests.get(DECK_URL)
    count = count.content
    count = json.loads(count)
    print("COUNTING")
    print(count["remaining"])

def shuffle():
    """ Shuffle the deck """
    shuffle = DECK_URL + "/shuffle/"
    requests.get(shuffle)

def getValue(val):
    """ Get the value of a card """
    if val == "KING" or val == "JACK" or val == "QUEEN":
        value = 10
    elif val == "ACE":
        value = 11
    else:
        value = val
    return int(value)

def scoreHand(hand):
    """ Score the hand"""
    score = 0
    aces = 0

    for card in hand:
        if card["value"] == "ACE":
            aces += 1
        else:
            value = getValue(card["value"])
            score += value

    # Scoring aces
    score += aces
    for i in range(aces):
        if score + 10 <= 21:
            score += 10
    return score

def showHand(hand):
    """ Show a hand """
    for card in hand:
        print(getCard(card))

def getCard(card):
    """ Get rank and value of a card """
    card = card["value"].title() + " of " + card["suit"].title()
    return card

def gameStart():
    """  Initialise the game """
    global playerHand
    global aiHand
    global sitting
    global aiSitting

    playerHand = []
    aiHand = []
    sitting = False
    aiSitting = False
    draw(1, playerHand)
    draw(1, aiHand)
    draw(1, playerHand)
    draw(1, aiHand)

def printScores():
    """ Print player and AI scores """
    global sitting
    print("-"*33)
    print("Player hand:")
    showHand(playerHand)
    print("Score: ", scoreHand(playerHand))
    print()
    print("AI hand:")
    if not sitting:
        print("??")
        showHand(aiHand[1:])
        aiScore = scoreHand(aiHand[1:])
    else:
        showHand(aiHand)
        aiScore = scoreHand(aiHand)
    print("Score: ", aiScore)
    print()

def playerTurn():
    """ Player turn """
    global sitting
    if not sitting:
        hit = input("Would you like to hit? y/n\n")
        if hit == "y":
            draw(1, playerHand)
            print("You drew:",getCard(playerHand[-1]))
        else:
            sitting = True

def aiTurn():
    """ AI Logic """
    global aiSitting
    curScore = scoreHand(aiHand)
    if curScore > 16:
        aiSitting = True
        return
    else:
        draw(1, aiHand)
        print("AI Drew:", getCard(aiHand[-1]))

def conditionCheck():
    """ Check player and AI conditions """
    global sitting
    global aiSitting
    print("-"*33)
    pScore = scoreHand(playerHand)
    aiScore = scoreHand(aiHand)

    if pScore == 21:
        sitting = True
    if aiScore == 21:
        sitting = True

    printScores()
    if sitting and aiSitting:
        pScore = scoreHand(playerHand)
        aiScore = scoreHand(aiHand)
        if pScore > aiScore:
            # printScores()
            print("You win!")
            return True
        elif pScore == aiScore:
            # printScores()
            print("Draw!")
            return True
        else:
            # printScores()
            print("You lose!")
            return True

    if pScore > 21:
        # printScores()
        print("Player bust!")
        return True
    elif aiScore > 21:
        # printScores()
        print("AI bust!")
        return True
    elif pScore == 21:
        # printScores()
        print("Player wins!")
        return True
    elif aiScore == 21:
        # printScores()
        print("AI wins!")
        return True
    else:
        # printScores()
        return False

def playAgain():
    """ Prompt user to play again """
    prompt = input("Would you like to play again? y/n\n")
    if prompt == "y":
        print("\n"*50)
        return 0
    return -1

if __name__ == '__main__':
    """ Main game loop """
    while True:
        if round == -1:
            print("Thanks for playing!")
            break
        if round == 0:
            round += 1
            gameStart()
        if conditionCheck():
            round = playAgain()
            continue
        playerTurn()
        if sitting:
            aiTurn()
