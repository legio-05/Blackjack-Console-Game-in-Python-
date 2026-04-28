import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def image(self):
        top = "┌───┐"
        mid = f"|{self.rank:<2} |" if len(self.rank) == 1 else f"|{self.rank:<2}|"
        suit = f"| {self.suit} |"
        bot = "└───┘"
        return [top, mid, suit, bot]

class Deck:
    suits = ['♥', '♦', '♠', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.rank in ['J', 'Q', 'K']:
            self.value += 10
        elif card.rank == 'A':
            self.value += 11
            self.aces += 1
        else:
            self.value += int(card.rank)
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def get_value(self):
        return self.value

    def display(self, show_dealer=False):
        if self.dealer and not show_dealer:
            print("DEALER HAND:")
            hidden = ["┌───┐", "|## |", "|###|", "└───┘"]
            card2 = self.cards[1].image()
            for h, c in zip(hidden, card2):
                print(h, c)
        else:
            owner = "DEALER" if self.dealer else "PLAYER"
            print(f"{owner} HAND (Value: {self.get_value()})")
            images = [card.image() for card in self.cards]
            for i in range(4):
                print(" ".join(img[i] for img in images))

class Money:
    def __init__(self, amount):
        self.amount = amount

    def add_money(self, amount):
        self.amount += amount

    def sub_money(self, amount):
        self.amount -= amount

    def get_bet(self, max_bet):
        while True:
            try:
                bet = int(input(f"How much do you bet? (max -> {max_bet}, or 0 to quit): "))
                if bet == 0:
                    return 0
                if 0 < bet <= min(self.amount, max_bet):
                    return bet
                else:
                    print("Invalid bet. Try again.")
            except ValueError:
                print("Please enter a valid number.")

class Game:
    def __init__(self):
        print("Welcome to Blackjack!")
        money = int(input("How much money are you willing to play with? "))
        self.money = Money(money)

    def get_move(self):
        while True:
                move = input("Do you want to (H)it, (S)tand, or (D)ouble Down? ").lower()
                if move in ['h', 's', 'd']:
                    return move
                else:
                    print("Invalid choice. Try again.")

    def play(self):
        while self.money.amount > 0:
            deck = Deck()
            deck.shuffle()

            bet = self.money.get_bet(500)
            if bet == 0:
                print("You quit the game.")
                break

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

            dealer_hand.display(show_dealer=False)
            player_hand.display()

            hands = [player_hand]

            for hand in hands:
                while hand.get_value() < 21:
                    move = self.get_move()
                    if move == 'h':
                        hand.add_card(deck.deal())
                        hand.display()
                    elif move == 'd':
                        bet *= 2
                        hand.add_card(deck.deal())
                        hand.display()
                        break
                    else:
                        break

                if hand.get_value() > 21:
                    print("Bust! You lose.")
                    self.money.sub_money(bet)
                    continue

                while dealer_hand.get_value() < 17:
                    dealer_hand.add_card(deck.deal())
                dealer_hand.display(show_dealer=True)

                if dealer_hand.get_value() > 21 or dealer_hand.get_value() < hand.get_value():
                    print("You win!")
                    self.money.add_money(bet)
                elif dealer_hand.get_value() == hand.get_value():
                    print("It's a tie")
                else:
                    print("Dealer wins!")
                    self.money.sub_money(bet)

            print("Money left:", self.money.amount)
            if self.money.amount <= 0:
                print("You are out of money. Game over.")
                break

if __name__ == "__main__":
    game = Game()
    game.play()