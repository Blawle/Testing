'''
Simple Black Jack game

No Insurance, Double Down, or Card Splits required (add in future?)
Players get a bank roll = $2000 to start
Players can pick bet level
Only one player and automated dealer

'''

# Setup imports
import random

# Setup Card Deck
suits = (
    'Hearts',
    'Diamonds',
    'Spades',
    'Clubs'
    )
ranks = (
    'Two',
    'Three',
    'Four',
    'Five',
    'Six',
    'Seven',
    'Eight',
    'Nine',
    'Ten',
    'Jack',
    'Queen',
    'King',
    'Ace'
    )
values = {
    'Two':2,
    'Three':3,
    'Four':4,
    'Five':5,
    'Six':6,
    'Seven':7,
    'Eight':8,
    'Nine':9,
    'Ten':10,
    'Jack':10,
    'Queen':10,
    'King':10,
    'Ace':11
    }


# Set Playing = True to enable game to start
playing = True

# CLASS DEFINITIONS:

# Define Card Class
# Contains Suit and Rank, returns suit and rank
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + ' of ' + self.suit

# Define Deck Class
# Contains all 52 cards, can be randomized
class Deck:
    def __init__(self):
        self.deck = [] # Start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = '' # Start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__() # Add each card object's print string
        return 'The deck has: ' + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck) # Randomize the deck

    def deal(self):
        single_card = self.deck.pop() # Remove a card, cannot recieve same card twice
        return single_card

# Define Hand Class
# Hand contains all cards currently in players hand
class Hand:
    def __init__(self):
        self.cards = [] # Start with an empty list
        self.value = 0 # Start with zero value
        self.aces = 0 # Add attribute to keep track of Aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 # Add to self.aces
        
    def adjust_for_aces(self):
        while self.value > 21 and self.aces: # self.aces is an integer which can be treated as a True (>0) and False (=0)
            self.value -= 10
            self.aces -= 1

# Define Chips Class
# Chips contain all money player has
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# FUNCTION DEFINITIONS:

# Define Betting
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry that is an invalid bet.')
        else:
            if chips.bet > chips.total:
                print('Sorry, you cannot complete that bet. Bet cannot exceed ',chips.total)
            else:
                break

# Define Hit
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()

# Define hitting and standing actions
def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's'")
        if x[0].lower() == 'h':
            hit(deck,hand) # hit() function defined above
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again")
            continue
        break

# Define showing some cards (Dealer hand only shows one card at start)
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <Card Hidden>")
    print('',dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand = ",player.value)
    print("\n")

# Define showing all cards
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand = ",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand = ",player.value)
    print("\n")

# Define when a player busts
def player_busts(player, dealer, chips):
    print("Player Busts!")
    print("\n")
    chips.lose_bet()

# Define when a player wins
def player_wins(player, dealer, chips):
    print("Player Wins!")
    print("\n")
    chips.win_bet()

# Define when the dealer busts
def dealer_busts(player, dealer, chips):
    print("Dealer Busts!")
    print("\n")
    chips.win_bet()

# Define when the dealer wins
def dealer_wins(player, dealer, chips):
    print("Dealer Wins!")
    print("\n")
    chips.lose_bet()

# Define when a player pushes
def push(player, dealer):
    print("Player and Dealer Tie. Push.")
    print("\n")

# GAMEPLAY
while True:
    # Print an opening statement
    print("\n\nWelcome to Blackjack!\nThe objective is to get as close to 21 as possible without going over!\nDealer will hit until 17. Aces count as 1 or 11.")

    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    # Player Hand deal
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    # Dealer Hand deal
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Set up the Player's chips
    player_chips = Chips() # Default value is 100

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand) 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
    
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
        
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at: ",player_chips.total)
    if player_chips.total == 0:
        print("\nWe're sorry, you have no chips left.\n\n")
        break
    
    # Ask to play again
    new_game = input("\n\nWould you like to play another hand? y or n: ")
    if new_game[0].lower() == 'y':
        playing=True
        continue
    else:
        print("\n\nThanks for playing!\n")
        break
