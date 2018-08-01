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
        self.playerCard = []
        self.total_money = 0
        self.bet = 0

    def append_card(self, card):
        self.playerCard.append(card)

    def show_card(self, value):
        return self.playerCard[value]

    def discard_card(self, index):
        self.playerCard.pop(index)

    def get_hand(self):
        return self.playerCard

    def add_money(self, amount):
        self.total_money += amount

    def get_money(self, amount):
        self.total_money -= amount


def deal(user, deck1):
    user.append_card(deck1.pop(random.randint(0, len(deck1) - 1)))


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.fold_button = QtWidgets.QPushButton('Fold', self)
        self.deal_button = QtWidgets.QPushButton('Deal', self)
        self.replay_button = QtWidgets.QPushButton('Replay', self)

        # ----Dealer----
        self.dealer_hand = QLabel(self)
        self.dealer_hand.setText(str(dealer.playerCard[0].value))
        self.dealer_hand.resize(200, 50)

        # ----Player----
        self.player_hand_string = ""
        for i in range(2):
            self.player_hand_string += str(player.playerCard[i].value)
            if i < 1:
                self.player_hand_string += ", "
        self.player_hand = QLabel(self.player_hand_string, self)
        self.player_hand.resize(200, 50)

        self.dealer_min = 16

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack")

        # ---- BUTTONS ----
        self.deal_button.move(200, 300)
        self.fold_button.move(200, 350)
        self.replay_button.move(200, 400)
        self.deal_button.clicked.connect(self.deal_button_click)
        self.fold_button.clicked.connect(self.fold_button_click)
        self.replay_button.clicked.connect(self.replay_button_click)

        # ---- LABELS ----
        self.player_hand.move(200, 250)
        self.dealer_hand.move(200, 50)

        self.show()

    def calculate_winner(self):
        sum_dealer = 0
        for card in dealer.get_hand():
            sum_dealer += card.value

        sum_player = 0
        for card in player.get_hand():
            sum_player += card.value

        print("Dealer: ", sum_dealer)
        print("Player: ", sum_player)

    def deal_button_click(self):
        # Deal for player
        if self.player_valid_deal(player):
            deal(player, deck)
            string = self.player_hand.text()
            string += ", " + str(player.playerCard[len(player.playerCard) - 1].value)
            self.player_hand.setText(string)

            sum1 = 0
            for card in player.playerCard:
                sum1 += card.value
            if sum1 > 21:
                self.player_hand.setText(self.player_hand.text() + "-" + " You lost")

        else:
            print("TOO MUCHO IDIOTA!")

        if self.computer_valid_deal(dealer):
            deal(dealer, deck)
            str1 = self.dealer_hand.text()
            str1 += ", " + str(dealer.playerCard[len(dealer.playerCard) - 1].value)
            self.dealer_hand.setText(str1)

            if self.calculate_total(dealer) > 21:
                self.dealer_hand.setText(self.dealer_hand.text() + "-" "Dealer LOST")

    def fold_button_click(self):
        while self.calculate_total(dealer) < 16:
            deal(dealer, deck)

        self.calculate_winner()

    def replay_button_click(self):
        print("hej")

    def calculate_total(self, p):
        i = 0
        for card in p.playerCard:
            temp = card.value
            if temp > 10:
                temp = 10
            i += temp
        return i

    def computer_valid_deal(self, d):
        sum = 0
        for card in d.playerCard:
            temp = card.value
            if temp > 10:
                temp = 10
            sum += temp
        print("Computer sum: ", sum)
        if sum > self.dealer_min:
            return False

        else:
            return True

    def player_valid_deal(self, p):
        sum = 0
        for card in p.playerCard:
            sum += card.value
        print("Player sum: ", sum)
        if sum > 21:
            return False
        else:
            return True


player = Player("player")
dealer = Player("Dealer")

deal(player, deck)
deal(player, deck)
deal(dealer, deck)

print("Size of player hand: ", len(player.playerCard))
print("Cards in Elias' hand: ")
for Card in player.playerCard:
    print(Card.value, Card.suit)

# ----Setup for Application----
app = QApplication(sys.argv)
w = Window()
w.resize(500, 500)
sys.exit(app.exec_())
