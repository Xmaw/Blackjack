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

    def replay(self):
        self.playerCard = []

    def place_bet(self, amount):
        self.bet = amount


def deal(user, deck):
    if len(deck) > 40:
        user.append_card(deck.pop(random.randint(0, len(deck) - 1)))
    else:
        print("Deck is out of cards!")


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # ----Buttons----
        self.fold_button = QtWidgets.QPushButton('Fold', self)
        self.deal_button = QtWidgets.QPushButton('Deal', self)
        self.replay_button = QtWidgets.QPushButton('Replay', self)
        self.place_bet_button = QtWidgets.QPushButton('Place bet', self)

        # ----Dealer----
        self.dealer_hand = QLabel(self)
        self.dealer_hand.resize(200, 50)
        self.dealer_min = 17

        # ----Player----
        self.player_hand = QLabel(self)
        self.player_hand.resize(200, 50)
        self.player_bet = QtWidgets.QLineEdit(self)
        self.player_bet.resize(50, 50)
        self.player_bet.move(150, 250)
        self.money_label = QtWidgets.QLabel("Total: $0", self)
        self.bet_label = QtWidgets.QLabel("Current bet: $0", self)

        # ----Welcome label----
        self.welcome_label = QLabel("Welcome to Blackjack!\nPlease enter your bet below.", self)
        self.welcome_label.setStyleSheet("font: 30px")
        self.welcome_label.setWordWrap(True)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack")

        # ---- BUTTONS ----
        self.deal_button.move(200, 300)
        self.fold_button.move(200, 350)
        self.replay_button.move(200, 400)
        self.place_bet_button.move(150, 300)
        self.deal_button.clicked.connect(self.deal_button_click)
        self.fold_button.clicked.connect(self.fold_button_click)
        self.replay_button.clicked.connect(self.replay_button_click)
        self.place_bet_button.clicked.connect(self.place_bet_button_click)

        # ---- LABELS ----
        self.player_hand.move(200, 250)
        self.dealer_hand.move(200, 50)
        self.money_label.move(50, 350)
        self.bet_label.move(50, 375)
        self.bet_label.resize(200, 25)

        self.hide_playfield()

        self.show()

    def calculate_winner(self):
        sum_dealer = 0
        for card in dealer.get_hand():
            temp = card.value
            print("Computer", card.value)
            if temp > 10:
                temp = 10
            sum_dealer += temp

        sum_player = 0
        for card in player.get_hand():
            temp = card.value
            print("Player", card.value)
            if temp > 10:
                temp = 10
            sum_player += temp

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

        s = ""
        for card in dealer.playerCard:
            print(card.value)
            s += str(card.value)
            s += ", "

        self.dealer_hand.setText(s)

        self.calculate_winner()

    def replay_button_click(self):
        for p in all_players:
            print(p.name)
            p.replay()

        self.player_hand.setText("")
        self.dealer_hand.setText("")
        self.hide_playfield()
        self.show_betfield()

    def place_bet_button_click(self):
        deal(player, deck)
        deal(player, deck)
        deal(dealer, deck)
        print(self.player_bet.text())
        self.bet_label.setText("Current bet: $" + self.player_bet.text())
        self.show_cards()
        self.show_playfield()
        self.hide_betfield()

    def hide_playfield(self):
        self.fold_button.hide()
        self.deal_button.hide()
        self.replay_button.hide()

    def show_playfield(self):
        self.fold_button.show()
        self.deal_button.show()
        self.replay_button.show()

    def hide_betfield(self):
        self.player_bet.hide()
        self.place_bet_button.hide()
        self.welcome_label.hide()

    def show_betfield(self):
        self.player_bet.show()
        self.place_bet_button.show()
        self.welcome_label.show()

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

    def show_cards(self):
        s = ""
        for i in range(2):
            s += str(player.playerCard[i].value)
            if i < 1:
                s += ", "
        self.player_hand.setText(s)
        self.dealer_hand.setText(str(dealer.playerCard[0].value))


suits = ["Diamonds", "Spades", "Heart", "Clubs"]
deck = [Card(value, suit) for value in range(1, 14) for suit in suits]

player = Player("player")
dealer = Player("Dealer")

all_players = [player, dealer]

print("Size of player hand: ", len(player.playerCard))
print("Cards in Elias' hand: ")
for Card in player.playerCard:
    print(Card.value, Card.suit)

# ----Setup for Application----
app = QApplication(sys.argv)
w = Window()
w.resize(500, 500)
sys.exit(app.exec_())
