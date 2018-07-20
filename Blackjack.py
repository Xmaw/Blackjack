import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
import sys


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def show_value(self):
        return self.value


suits = ["Diamonds", "Spades", "Heart", "Clubs"]
deck = [Card(value, suit) for value in range(1, 14) for suit in suits]


class Player:
    def __init__(self, name):
        self.name = name

    playerCard = []

    def append_card(self, card):
        self.playerCard.append(card)

    def show_card(self, value):
        return self.playerCard[value]

    def discard_card(self, index):
        self.playerCard.pop(index)


def deal(player, deck1):
    player.append_card(deck1.pop(random.randint(0, len(deck1) - 1)))


player = Player("player")
dealer = Player("Dealer")
deal(player, deck)
deal(dealer, deck)

print("size of deck", len(player.playerCard))

print("Cards in Elias' hand: ")
for Card in player.playerCard:
    print(Card.value, Card.suit)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.fold_button = QtWidgets.QPushButton('Fold', self)
        self.deal_button = QtWidgets.QPushButton('Deal', self)

        # ---- Card representations as Lables ----
        self.dealer_hand_string = str(dealer.show_card(0).show_value())
        self.player_hand = QLabel(str(player.show_card(0).show_value()), self)
        self.dealer_hand = QLabel(self.dealer_hand_string, self)
        self.player_hand.resize(200, 50)
        self.dealer_hand.resize(200, 50)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack")

        # ---- BUTTONS ----
        self.deal_button.move(200, 300)
        self.fold_button.move(200, 350)
        self.deal_button.clicked.connect(self.deal_button_click)
        self.fold_button.clicked.connect(self.fold_button_click)

        # ---- LABELS ----
        self.player_hand.move(200, 250)
        self.dealer_hand.move(200, 50)

        self.show()

    def deal_button_click(self):
        if self.valid_deal():
            deal(player, deck)
            string = self.player_hand.text()
            string += ", " + str(player.show_card(len(player.playerCard)-1).value)
            print(string)
            self.player_hand.setText(string)

    def fold_button_click(self):
        self.player_hand.setText("New Text")

    def valid_deal(self):
        return True


# ----Setup for Application----
app = QApplication(sys.argv)
w = Window()
w.resize(500, 500)
sys.exit(app.exec_())
