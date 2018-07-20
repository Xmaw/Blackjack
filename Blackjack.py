import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
import sys


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value


suits = ["Diamonds", "Spades", "Heart", "Clubs"]
deck = [Card(value, suit) for value in range(1, 14) for suit in suits]


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
    player.appendCard(deck.pop(random.randint(0, len(deck) - 1)))


elias = Player("Elias")
deal(elias, deck)

print("size of deck", len(elias.playerCard))

print("Cards in Elias' hand: ")
for Card in elias.playerCard:
    print(Card.value, Card.suit)

# ----Setup for Application----
app = QApplication(sys.argv)
w = QWidget()
w.show()
w.setWindowTitle("Blackjack")
# ---- BUTTONS ----
deal_button = QtWidgets.QPushButton('Deal')
fold_button = QtWidgets.QPushButton('Fold')

button_box = QtWidgets.QHBoxLayout()

# ---- Add widgets to the Hbox ----
button_box.addWidget(deal_button)
button_box.addWidget(fold_button)

w.setLayout(button_box)  # Add widgets to the window

sys.exit(app.exec_())
