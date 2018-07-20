import random


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value


suits = ["Diamonds", "Spades", "Heart", "Clubs"]
deck = [Card(value, suit) for value in range(1, 14) for suit in suits]
print(deck.__getitem__(1).suit, deck.__getitem__(1).value)


# for Card in deck:
#   print(Card.suit, "|", Card.value)


class Player:
    def __init__(self, name):
        self.name = name

    playerCard = []

    def appendCard(self, card):
        self.playerCard.append(card)

    def showCard(self, value):
        return self.playerCard[value]

    def discardCard(self, index):
        self.playerCard.pop(index)


def deal(player, deck):
    player.appendCard(deck.pop(random.randint(0, len(deck)-1)))


elias = Player("Elias")
deal(elias, deck)

print(len(elias.playerCard))

for Card in elias.playerCard:
    print(Card.value, Card.suit)

while True:
    request = input()
    if request == "deal":
        deal(elias, deck)
    elif request == "done":
        break
    elif request == "show":
        for Card in elias.playerCard:
            print(Card.suit, Card.value)
    elif request == "discard":
        elias.discardCard(int(input("What chard do you wish to remove?")))
    else:
        print("Invalid request.")
    


