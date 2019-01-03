#Constants
import random
import cardtype
import visibilities
import owners
import controlers
import effects
import deck_builder
import globe


class pile:
	#List of cards
	contents = None
	visibility = visibilities.PUBLIC
	owner = None

	#I'll start the deck empty
	def __init__(self,owner = None,visibility = visibilities.PUBLIC):
		self.owner = owner
		self.visibility = visibility
		self.contents = []

	def shuffle(self):
		random.shuffle(self.contents)

	def size(self):
		return len(self.contents) 

	def can_draw(self):
		if self.size() > 0:
			return True
		else:
			return False

	def draw(self):
		return self.contents.pop()

	def add(self,card):
		self.contents.append(card)

	def add_bottom(self,card):
		self.contents.insert(0,card)

	def get_count(self,find_type = cardtype.ANY):
		if find_type == cardtype.ANY:
			return self.size()
		else:
			#if self.visibility == visibilities.PUBLIC \
			#	or (self.visibility == visibilities.PRIVATE and self.owner.pid = pid)
			count = 0
			for c in self.contents:
				if c.ctype == find_type:
					count += 1
			return count

class playing(pile):
	power = 0
	card_mods = []
	double_modifier = 0

	def no_mod(self,card):
		return card.play_action(self.owner)

	def __init__(self,owner = None,visibility = visibilities.PUBLIC):
		self.owner = owner
		self.visibility = visibility
		self.contents = []
		self.card_mods = [self.no_mod]


	def turn_end(self):
		print("ENDEDPLAYING")
		self.power = 0
		self.card_mods = [self.no_mod]
		self.double_modifier = 0
		while self.size() > 0:
			c = self.contents.pop()
			print(c.name,self.size(), c.owner)
			if c.owner_type == owners.PLAYER:
				c.owner.discard.add(c)
				print("!!!",c.owner.discard.size())
			elif c.owner_type == owners.MAINDECK:
				globe.boss.globe.boss.main_deck.add(c)
			elif c.owner_type == owners.LINEUP:
				globe.boss.lineup.add(c)
			elif c.owner_type == owners.VILLAINDECK:
				globe.boss.supervillain_stack.add(c)

	def add(self,card):
		self.play(card)


	def play(self,card):
		self.contents.append(card)
		modifier = 0
		#print("ABIOUT TO PLAY")
		for mod in self.card_mods:
			modifier += mod(card)
		#modifier = card.play_action(self.owner)
		#modifier = post_power()

		for i in range(self.double_modifier):
			modifier *= 2

		#print("MOD WAS",modifier)
		self.power += modifier
		#print("PLAYED!", self.power, self)

	def parallax_double():
		power *= 2
		double_modifier += 1



class player:
	pid = -1
	deck = None
	hand = None
	discard = None
	ongoing = None
	played = None
	controler = None

	gain_redirect = []
	gained_this_turn = []
	discount_on_sv = 0
	played_riddler = False

	def __init__(self,pid, controler):
		self.controler = controler
		self.pid = pid
		self.deck = pile(self, visibilities.SECRET)
		self.hand = pile(self, visibilities.PRIVATE)
		self.discard = pile(self)
		self.ongoing = pile(self)
		self.played = playing(self)

		#These should be reinitialized or they share values with all insatnces
		gain_redirect = []
		gained_this_turn = []

		self.deck.contents = deck_builder.get_starting_deck(self)
		#self.deck.shuffle()

		for i in range(5):
			self.hand.add(self.deck.draw())

	def draw_card(self):
		if not self.manage_reveal():
			return None
		drawn_card = self.deck.draw()
		self.hand.add(drawn_card)
		return drawn_card

	def reveal_card(self):
		if not self.manage_reveal():
			return None
		print("HSHHDHD",self.deck.size())
		return self.deck.contents[-1]

	def manage_reveal(self):
		if not self.deck.can_draw():
			self.deck.contents = self.discard.contents
			self.discard.contents = []
			self.deck.shuffle()
			print("IM HERE")
			if self.deck.size() == 0:
				return False
			return True
		else:
			return True

	def play(self, cardnum):
		print("Tried to play")
		self.played.play(self.hand.contents.pop(cardnum))

	def play_and_return(self, card, pile):
		self.played.play(card)
		self.played.contents.remove(card)
		pile.add(card)

	def buy_supervillain(self):
		if self.played.power >= globe.boss.supervillain_stack.contents[-1].cost - discount_on_sv:
			self.played.power -= globe.boss.supervillain_stack.contents[-1].cost -discount_on_sv
			self.gain(globe.boss.supervillain_stack.contents.pop())
			return True
		return False

	def buy_kick(self):
		if globe.boss.kick_stack.size() > 0 and self.played.power >= globe.boss.kick_stack.contents[-1].cost:
			self.played.power -= globe.boss.kick_stack.contents[-1].cost
			self.gain(globe.boss.kick_stack.contents.pop())
			return True
		return False

	def riddle(self):
		if self.played_riddler and globe.boss.main_deck.size() > 0 and self.played.power >= 3:
			self.played.power -= 3
			self.gain(globe.boss.main_deck.contents.pop())
			return True
		return False

	def gain_a_weakness(self):
		if globe.boss.weakness_stack.size() > 0:
			self.gain(globe.boss.weakness_stack.contents.pop())
			return True
		return False

	def buy(self,cardnum):
		if cardnum < 0 or cardnum >= len(globe.boss.lineup.contents):
			return False
		elif self.played.power >= globe.boss.lineup.contents[cardnum].cost:
			self.played.power -= globe.boss.lineup.contents[cardnum].cost
			self.gain(globe.boss.lineup.contents.pop(cardnum))
			return True
		return False

	def gain(self, card):
		card.set_owner(player=self)
		gained_this_turn.append(card)
		card.buy_action()

		if len(self.gain_redirect) > 0:
			assemble = []
			for re in self.gain_redirect:
				assemble.append(re)
			for re in assemble:
				if re == self.hand and controler.may_put_on_top("of hand",card):
					self.gain_redirect.remove(re)
					self.hand.add(card)
					return
				elif re == self.deck:
					if controler.may_put_on_top("of deck",card):
						self.gain_redirect.remove(re)
						self.deck.add(card)
						return
					# If theres a better way to do solomun grudy with the architecture avalable...
					elif card.name == "Solomon Grundy":
						self.gain_redirect.remove(re)

		self.discard.add(card)
		return
			

	def discard_hand(self):
		self.discard.contents.extend(self.hand.contents)
		self.hand.contents = []

	def end_turn(self):
		gain_redirect = []
		gained_this_turn = []
		discount_on_sv = 0
		played_riddler = False
		for c in self.played.contents:
			c.end_of_turn()
		self.played.turn_end()
		print("HAND DISCARDED")
		self.discard_hand()
		for i in range(5):
			self.draw_card()

	def calculate_vp(self):
		self.deck.contents.extend(self.discard.contents)
		self.deck.contents.extend(self.hand.contents)
		self.deck.contents.extend(self.played.contents)
		self.deck.contents.extend(self.ongoing.contents)
		vp = 0
		for c in self.deck.contents:
			vp += c.calculate_vp()
		return vp





class model:

	DEBUG = True
	main_deck = None
	weakness_stack = None
	kick_stack = None
	supervillain_stack = None
	lineup = None
	players = []
	player_score = []
	destroyed_stack = None
	notify = None
	whose_turn = 0

	#initialize Game
	def __init__(self,number_of_players=2):
		self.main_deck = pile()
		self.main_deck.contents = deck_builder.initialize_deck()
		self.weakness_stack = pile()
		self.weakness_stack.contents = deck_builder.initialize_weaknesses()
		self.kick_stack = pile()
		self.kick_stack.contents = deck_builder.initialize_kicks()
		self.supervillain_stack = pile()
		self.supervillain_stack.contents = deck_builder.initialize_supervillains()
		self.lineup = pile()
		self.destroyed_stack = pile()

		for c in range(5):
			self.lineup.add(self.main_deck.draw())

		#2 human players for initialization
		for player_id in range(number_of_players):
			new_player = player(player_id,None)
			new_controler = controlers.human(new_player)
			new_player.controler = new_controler
			self.players.append(new_player)

	def start_game(self):
		while self.supervillain_stack.get_count() > 0:
			if self.notify != None:
				self.notify()
			self.players[self.whose_turn].controler.turn()

			for i in range(5 - self.lineup.size()):
				self.lineup.add(self.main_deck.draw())

			self.whose_turn += 1
			if self.whose_turn >= len(self.players):
				self.whose_turn = 0

		for p in self.players:
			self.player_score.append(p.calculate_vp())



	def register(self,func):
		self.notify = func

