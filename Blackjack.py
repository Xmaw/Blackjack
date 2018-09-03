import random

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel
import sys

from PyQt5.uic.properties import QtGui


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def show_value(self):
        return self.value


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.total_money = 0
        self.bet = 0

    def append_card(self, card):
        self.hand.append(card)

    def show_card(self, value):
        return self.hand[value]

    def discard_card(self, index):
        self.hand.pop(index)

    def get_hand(self):
        return self.hand

    def add_money(self, amount):
        self.total_money += amount

    def remove_money(self, amount):
        self.total_money -= amount

    def replay(self):
        self.hand = []

    def place_bet(self, amount):
        self.bet = amount

    def get_money(self):
        return self.total_money


def deal(user, deck):
    if len(deck) > 0:
        user.append_card(deck.pop(random.randint(0, len(deck)-1)))
    else:
        print("Deck is out of cards!")


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # ----Background picture----
        self.picture_label = QLabel(self)
        self.pixmap = QPixmap('blackjack_table.jpg')
        self.picture_label.setPixmap(self.pixmap)

        # ----Buttons----
        self.stand_button = QtWidgets.QPushButton('Stand', self)
        self.hit_button = QtWidgets.QPushButton('Hit', self)
        self.replay_button = QtWidgets.QPushButton('Replay', self)
        self.place_bet_button = QtWidgets.QPushButton('Place bet', self)
        self.start_button = QtWidgets.QPushButton('Start', self)

        # ----Dealer----
        self.dealer_hand = QLabel(self)
        self.dealer_hand.resize(200, 50)
        self.dealer_min = 17

        # ----Player----
        self.player_hand = QLabel(self)
        self.player_hand.resize(200, 50)
        self.player_bet = QtWidgets.QLineEdit(self)
        self.player_bet.resize(50, 50)
        self.player_bet.move(960, 650)
        self.money_label = QtWidgets.QLabel("Total: $0", self)
        self.bet_label = QtWidgets.QLabel("Current bet: $0", self)

        self.player_bet_amount = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack")

        # ---- BUTTONS ----
        self.hit_button.move(850, 750)
        self.stand_button.move(1000, 750)
        self.replay_button.move(200, 400)
        self.place_bet_button.move(850, 750)
        self.start_button.move(1000, 750)
        self.hit_button.clicked.connect(self.deal_button_click)
        self.stand_button.clicked.connect(self.stand_button_clicked)
        self.replay_button.clicked.connect(self.replay_button_click)
        self.place_bet_button.clicked.connect(self.place_bet_button_click)
        self.start_button.clicked.connect(self.start_button_clicked)


        # ---- LABELS ----
        self.player_hand.move(200, 250)
        self.dealer_hand.move(200, 50)
        self.money_label.move(100, 850)
        self.money_label.setFont(QFont("Times", 12, QFont.Bold))
        self.money_label.resize(2500, 50)
        self.bet_label.move(100, 800)
        self.bet_label.setFont(QFont("Times", 12, QFont.Bold))
        self.bet_label.resize(2500, 50)

        # ---- Hides some of the buttons until the round starts ----
        self.start_button.hide()
        self.hit_button.hide()
        self.stand_button.hide()
        self.replay_button.hide()

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

        if sum_player < sum_dealer < 21:
            print("Dealer Won!")
            player.remove_money(self.player_bet_amount)
            self.money_label.setText("Total: $" + str(player.get_money()))

        elif sum_player > 21:
            print("Dealer won!")
            player.remove_money(self.player_bet_amount)
            self.money_label.setText("Total: $" + str(player.get_money()))
        elif sum_dealer < sum_player < 21:
            print("Player won!")
            player.add_money(self.player_bet_amount)
            self.money_label.setText("Total: $" + str(player.get_money()))

        elif sum_player == 21:
            print("Blackjack!!")
            print("Player won: $", self.player_bet_amount * 1.5)
            player.add_money(self.player_bet_amount * 1.5)
            self.money_label.setText("Total: $" + str(player.get_money()) * 1.5)

        elif sum_dealer == 21:
            print("Dealer won!")
            player.remove_money(self.player_bet_amount)
            self.money_label.setText("Total: $" + str(-player.get_money()))

        elif sum_dealer < 21 and sum_player > 21:
            print("Dealer Won!!")

        elif sum_player < 21 and sum_dealer > 21:
            print("Player Won!")

        else:
            print("Draw!")

    def deal_button_click(self):
        # Deal for player

        if self.player_valid_deal(player):
            deal(player, deck)
            string = self.player_hand.text()
            string += ", " + str(player.hand[len(player.hand) - 1].value)
            self.player_hand.setText(string)
            sum1 = 0
            for card in player.hand:
                sum1 += card.value
            if sum1 > 21:
                self.player_hand.setText(self.player_hand.text() + "-" + " You lost")

        else:
            print("TOO MUCHO IDIOTA!")

        if self.computer_valid_deal(dealer):
            deal(dealer, deck)
            str1 = self.dealer_hand.text()
            str1 += ", " + str(dealer.hand[len(dealer.hand) - 1].value)
            self.dealer_hand.setText(str1)
            if self.calculate_total(dealer) > 21:
                self.dealer_hand.setText(self.dealer_hand.text() + "-" "Dealer LOST")
        self.place_cards(player)
        self.place_cards(dealer)

    def stand_button_clicked(self):
        while self.calculate_total(dealer) < 16:
            deal(dealer, deck)
        self.place_cards(dealer)
        self.calculate_winner()

    def replay_button_click(self):
        for p in all_players:
            print(p.name)
            p.replay()

        self.player_hand.setText("")
        self.dealer_hand.setText("")

    def place_bet_button_click(self):
        self.player_bet_amount = int(self.player_bet.text())
        self.bet_label.setText("Current bet: $" + self.player_bet.text())
        self.start_button.show()

    def hide_playfield(self):
        self.stand_button.hide()
        self.hit_button.hide()
        self.replay_button.hide()

    def show_playfield(self):
        self.stand_button.show()
        self.hit_button.show()
        self.replay_button.show()

    def hide_betfield(self):
        self.player_bet.hide()
        self.place_bet_button.hide()

    def show_betfield(self):
        self.player_bet.show()
        self.place_bet_button.show()
        self.welcome_label.show()

    def calculate_total(self, p):
        i = 0
        for card in p.hand:
            temp = card.value
            if temp > 10:
                temp = 10
            i += temp
        return i

    def computer_valid_deal(self, d):
        sum = 0
        for card in d.hand:
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
        for card in p.hand:
            sum += card.value
        print("Player sum: ", sum)
        if sum > 21:
            return False
        else:
            return True

    def show_cards(self):
        s = ""
        for i in range(2):
            s += str(player.hand[i].value)
            if i < 1:
                s += ", "
        self.player_hand.setText(s)
        self.dealer_hand.setText(str(dealer.hand[0].value))

    def start_button_clicked(self):
        self.place_cards(player)
        self.place_cards(dealer)
        self.hide_betfield()

        # ---- Hides start button and displays the command buttons ----
        self.start_button.hide()
        self.stand_button.show()
        self.hit_button.show()

    def place_cards(self, p):
        print(p.name)
        if p.name == 'player':
            delta_y = 450
        else:
            delta_y = 50

        delta_x = 850
        for card in p.hand:
            pic_label = QLabel(self)
            pic_pixmap = QPixmap()
            pixmap_str = 'deck/'

            # Append the value of the card to the cards URL.
            if card.value == 1:
                pixmap_str += 'A'
            elif card.value == 2:
                pixmap_str += '2'
            elif card.value == 3:
                pixmap_str += '3'
            elif card.value == 4:
                pixmap_str += '4'
            elif card.value == 5:
                pixmap_str += '5'
            elif card.value == 6:
                pixmap_str += '6'
            elif card.value == 7:
                pixmap_str += '7'
            elif card.value == 8:
                pixmap_str += '8'
            elif card.value == 9:
                pixmap_str += '9'
            elif card.value == 10:
                pixmap_str += '10'
            elif card.value == 11:
                pixmap_str += 'J'
            elif card.value == 12:
                pixmap_str += 'Q'
            elif card.value == 13:
                pixmap_str += 'K'

            # Append the character representing the suit in the cards URL
            if card.suit == 'Diamonds':
                pixmap_str += 'D'
            elif card.suit == 'Spades':
                pixmap_str += 'S'
            elif card.suit == 'Clubs':
                pixmap_str += 'C'
            else:
                pixmap_str += 'H'

            pic_pixmap.load(pixmap_str)
            pic_pixmap = pic_pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
            pic_label.setPixmap(pic_pixmap)
            pic_label.move(delta_x, delta_y)
            delta_x += 100
            pic_label.show()


suits = ["Diamonds", "Spades", "Heart", "Clubs"]
deck = [Card(value, suit) for value in range(1, 14) for suit in suits]

player = Player("player")
dealer = Player("Dealer")

all_players = [player, dealer]

print("Size of player hand: ", len(player.hand))
print("Cards in Elias' hand: ")
for Card in player.hand:
    print(Card.value, Card.suit)

deal(player, deck)
deal(player, deck)
deal(dealer, deck)

for card in player.hand:
    print(card.value, card.suit)
# ----Setup for Application----
app = QApplication(sys.argv)
w = Window()
w.resize(1920, 1080)
sys.exit(app.exec_())
