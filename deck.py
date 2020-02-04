from random import randint

class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	def __str__(self):
		return f"Value:\t{self.value}\tSuit:\t{self.suit}\n"

	def __repr__(self):
		return f"Value:\t{self.value}\tSuit:\t{self.suit}\n"

class Deck:
	suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

	def __init__(self,empty=True):
		self.deck = []

		if empty == False:
			self.populate()

	def __str__(self):
		s = "Your deck:\n"
		for card in self.deck:
			s += str(card)
		return s#"\n" + str(self.deck)

	def insert_card(self, card):
		self.deck.append(card)

	def populate(self):
		for i in [2,3,4,5,6,7,8,9,10,10,10,10,11]:
			for suit in Deck.suits:
				self.deck.append(Card(i, suit))

	def deal(self):
		if len(self.deck) == 0:
			self.populate()
		
		pop_index = randint(0, len(self.deck)-1)
		card = self.deck.pop(pop_index)

		return card

	def get_value(self):
		return sum([card.value for card in self.deck])

	def did_bust(self):
		value = self.get_value()
		if value > 21:
			#check to see if there's an ace:
			for card in self.deck:
				if card.value == 11:

					card.value = 1
					print(f"\t\t[!] Swapped ace from 11 to 1. New value: {self.get_value()}")
					if self.get_value() <= 21:
						return False
					else:
						continue

			return True
		else:
			return False

class Player:
	def __init__(self, num=0):
		self.deck = Deck()
		self.bet = 0
		self.score = 0
		self.busted = False
		self.name = f"Player {num+1}"

	def reset():
		self.deck = Deck()
		self.bet = 0
		self.busted = False

	def play(self) -> bool:
		user_input = input("\tType 'hit' if you would like to hit. > ")
		if user_input == "hit" or user_input == "h":
			return True
		else:
			return False

	def add_card(self, card) -> int:
		self.deck.insert_card(card)
		self.score += card.value
		return self.deck.get_value()

	def did_bust(self) -> bool:
		return self.deck.did_bust()

	def show_hand(self):
		return(self.deck)

	def get_value(self):
		if self.did_bust():
			return 0
		return self.score



class Dealer(Player):
	hit_until_inclusive = 16
	def __init__(self):
		super().__init__()
		self.name = "Dealer"

	def play(self):
		if self.deck.get_value() <= Dealer.hit_until_inclusive:
			return True
		else:
			return False

class Round:
	def __init__(self, num_players=1):
		self.main_deck = Deck(empty=False)
		self.dealer = Dealer()
		self.players = [Player(num=player) for player in range(num_players)]

		for player in self.players:
			c1 = self.main_deck.deal()
			c2 = self.main_deck.deal()
			player.add_card(c1)
			player.add_card(c2)

	def turn(self, player):
		print(f"*****\n{player.name}'s turn:")
		print(f"{player.show_hand()}*****\n")
		print(f"\t\tYour value is: {player.get_value()}\n")
		while player.play() == True: #If player decides to hit
			dealt_card = self.main_deck.deal()
			player.add_card(dealt_card)

			

			if player.did_bust():
				player.score = 0
				print(f"\n\t[!] Busted! Better luck next time.")
				print(f"\t\tYour value is: {player.get_value()}\n")
				break

			print(f"\t\tYour value is: {player.get_value()}\n")

		print(f"\n{player.show_hand()}*****\n")

		return player.get_value()


class Game:
	def __init__(self, num_players=1):
		self.round = Round(num_players=num_players)
		
	def play_game(self):
		for player in self.round.players:
			player.score = self.round.turn(player)
		self.round.turn(self.round.dealer)

		print("\n$$$$$\nTallying Results...\n")
		print(f"{self.round.dealer.name}'s score is: {self.round.dealer.score}")
		for player in self.round.players:
			print(f"{player.name}'s score is: {player.score}")

		winning_players = [player for player in self.round.players if (player.score > self.round.dealer.score) or (player.did_bust == False and self.round.dealer.did_bust == True)]
		if winning_players == []:
			print("Dealer wipes everyone out!")
		else:
			for player in winning_players:
				print(f"{player.name} wins!")





if __name__ == '__main__':
	n = input("Please input the number of players.")
	g = Game(int(n))
	g.play_game()
