import model
import time
import cardtype
import controlers
import globe


class view_controler():
	window = None
	colour = {cardtype.STARTER: '\033[93m', \
			cardtype.WEAKNESS: '\033[92m', \
			cardtype.HERO: '\033[94m', \
			cardtype.VILLAIN: '\033[91m', \
			cardtype.SUPERPOWER: '\033[96m', \
			cardtype.EQUIPMENT: '\033[89m', \
			cardtype.LOCATION: '\033[95m', \
			cardtype.ANY: '\033[0m'}

	def __init__(self,window = None):
		self.window = window
		controlers.set_view(self)

	def updated(self):
		print_board(globe.boss)

	def print_card(self,card, num = 0):
		print("\033[;7m" + self.colour[card.ctype] + f"{num:<2} {card.name:<20}vp:{card.vp:>2} cost:{card.cost:>2}  {card}" + self.colour[cardtype.ANY] + \
			f"\n{card.text}\n{card.attack_text}", flush = True)
		print("------------------------------------", flush = True)

	def print_board(self,turn = -1):
		if self.window != None:
			self.window.render()
		if turn == -1:
			turn = globe.boss.whose_turn
		player = globe.boss.players[turn]
		print("------------------------------------------------")
		print("------------------------------------------------")
		print("------------------------------------------------")
		print("------------------------------------------------")
		print(f"-{turn}--{player.persona.name}--------------------------------------------")
		if player.persona.active:
			print(f"----{player.persona.text}")
		else:
			print(f"----FLIPPED UPSIDE DOWN")
		print("------------------------------------------------")
		if player.ongoing.size() > 0:
			print(f"Ongoing:  ")
			print("------------------------------------------------")
			for num, card in enumerate(player.ongoing.contents):
				self.print_card(card,num)
			print("------------------------------------------------")



		print(f"#Weaknesses:{globe.boss.weakness_stack.size()}, #Kicks:{globe.boss.kick_stack.size()}")
		print(f"#Supervillains:{globe.boss.supervillain_stack.size()}, #Deck:{globe.boss.main_deck.size()}")
		if globe.boss.supervillain_stack.current_sv == globe.boss.supervillain_stack.contents[-1]:
			self.print_card(globe.boss.supervillain_stack.current_sv)
		else:
			print("\033[;7m" + f"Unkown" + self.colour[cardtype.ANY] + \
			f"\n\n", flush = True)
		print("------------------------------------", flush = True)
		print("------------------------------------------------")
		print("Lineup:")
		print("------------------------------------------------")
		for num, card in enumerate(globe.boss.lineup.contents):
			self.print_card(card,num)
		print("------------------------------------------------")
		print(f"#Deck:{player.deck.size()}, #Discard:{player.discard.size()}")
		if player.hand.size() > 0:
			print(f"Hand:  ")
			print("------------------------------------------------")
			for num, card in enumerate(player.hand.contents):
				self.print_card(card,num)
		print("------------------------------------------------")
		print("Played:  ")
		print("------------------------------------------------")
		for num, card in enumerate(player.played.contents):
			self.print_card(card,num)

		if player.played.power > 0:
			print(f"-- {player.played.power} power --")

	def print_power(self):
		player = globe.boss.players[globe.boss.whose_turn]
		print(f"-- {player.played.power} power --")

	def print_discard(self,turn = -1):
		if turn == -1:
			turn = globe.boss.whose_turn
		player = globe.boss.players[turn]
		print("------------------------------------------------")
		print("Discard:  ")
		print("------------------------------------------------")
		for num, card in enumerate(player.discard.contents):
			self.print_card(card,num)
		print("-------")

	def print_destroyed(self):
		print("------------------------------------------------")
		print(f" DESTRYOED ")
		print("------------------------------------------------")
		for num, card in enumerate(globe.boss.destroyed_stack.contents):
			self.print_card(card,num)

	def print_hand(self,player_id):
		player = globe.boss.players[player_id]
		print("------------------------------------------------")
		print(f" {player_id}'s HAND")
		print("------------------------------------------------")
		for num, card in enumerate(player.hand.contents):
			self.print_card(card,num)

	def print_played(self,player_id):
		player = globe.boss.players[player_id]
		print("------------------------------------------------")
		print(f" {player_id}'s played cards")
		print("------------------------------------------------")
		for num, card in enumerate(player.played.contents):
			self.print_card(card,num)

	def print_under(self,player_id):
		player = globe.boss.players[player_id]
		print("------------------------------------------------")


		
		print(f" Under {player_id}'s superhero")
		print("------------------------------------------------")
		for num, card in enumerate(player.under_superhero.contents):
			self.print_card(card,num)


	def print_deck(self, player_id = -1):
		player = None
		if player_id != -1:
			player = globe.boss.players[player_id]
		print("------------------------------------------------")
		if player == None:
			print(f" DECK ")
		else:
			print(f" {player_id}'s DECK ")
		print("------------------------------------------------")
		if player == None:
			for num, card in enumerate(globe.boss.main_deck.contents):
				self.print_card(card,num)
		else:
			for num, card in enumerate(player.deck.contents):
				self.print_card(card,num)

	def print_custom(self,cards):
		print("------------------------------------------------", flush = True)
		print("------------------------------------------------", flush = True)
		print("------------------------------------------------", flush = True)
		for i,c in enumerate(cards):
			self.print_card(c,i)
		
	

	def add_played_card(self):
		player = globe.boss.players[globe.boss.whose_turn]
		self.print_card(globe.boss.players[globe.boss.whose_turn].played.contents[-1],globe.boss.players[globe.boss.whose_turn].played.size()-1)
		print(f"-- {player.played.power} power --")

