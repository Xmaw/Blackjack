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


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack")
        # ---- BUTTONS ----
        deal_button = QtWidgets.QPushButton('Deal')
        fold_button = QtWidgets.QPushButton('Fold')

        deal_button.move(55, 70)

        # ---- Game Field BUTTONBOX ----
        game_area = QtWidgets.QVBoxLayout()
        game_area.addWidget(deal_button)
        game_area.addWidget(fold_button)

        # ----- Game Field GAMEAREA ----

        self.setLayout(game_area)  # Add widgets to the window

        self.show()

# ----Setup for Application----
app = QApplication(sys.argv)
w = Window()
w.resize(500,500)
sys.exit(app.exec_())
