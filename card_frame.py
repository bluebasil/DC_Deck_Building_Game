import globe
import cardtype
import owners
import arcade

class card:
	name = ""
	vp = 0
	cost = 0
	ctype = cardtype.ANY
	#All cards must manually set these
	defence = False
	attack = False
	owner = None
	owner_type = owners.MAINDECK
	text = ""
	attack_text = ""
	image = "base/images/cards/back.jpeg"
	texture = None


	#stats
	times_played = 0
	bought = False

	def __init__(self,owner = None):
		self.owner = owner
		if owner != None:
			self.owner_type = owners.PLAYER
		self.texture = arcade.load_texture(self.image)
	
	def play_action(self,player):
		return 0

	def later_play(self,player,on_card):
		return 0

	def set_owner(self,player=None):
		self.owner = player
		self.owner_type = owners.PLAYER

	def calculate_vp(self,all_cards):
		return self.vp

	def end_of_turn(self):
		return

	def buy_action(self):
		return

	#defence = True must be set or this will not be an option
	#pop_self will come in handy
	def defend(self):
		return

	#Only used for cards in the supervilalin stack
	def first_apearance(self):
		return

	def attack_action(self,by_player):
		return

	def destroy(self,player_responsible):
		self.pop_self()
		player_responsible.persona.destory_power()
		self.owner = None
		self.owner_type = owners.DESTROYED
		globe.boss.destroyed_stack.add(self)


	def pop_self(self):
		#why am i not checking by ownership type?
		if self in globe.boss.lineup.contents:
			globe.boss.lineup.contents.remove(self)
			if globe.DEBUG:
				print(f"{self.name} pop from lineup")
		elif self in globe.boss.destroyed_stack.contents:
			globe.boss.destroyed_stack.contents.remove(self)
			if globe.DEBUG:
				print(f"{self.name} pop from destroyed")
		elif self in globe.boss.main_deck.contents:
			globe.boss.main_deck.contents.remove(self)
			if globe.DEBUG:
				print(f"{self.name} pop from main_deck")
		elif self.owner_type == owners.PLAYER:
			if self in self.owner.hand.contents:
				self.owner.hand.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from hand")
			elif self in self.owner.discard.contents:
				self.owner.discard.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from discard")
			elif self in self.owner.ongoing.contents:
				self.owner.ongoing.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from ongoing")
			elif self in self.owner.played.contents:
				self.owner.played.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from played")
			elif self in self.owner.deck.contents:
				self.owner.deck.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from deck")
			elif self in self.owner.under_superhero.contents:
				self.owner.under_superhero.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from under_superhero")
		return self
		

class weakness(card):
	name = "Weakness"
	vp = -1
	ctype = cardtype.WEAKNESS
	owner_type = owners.WEAKNESS
	image = "base/images/cards/weakness.jpeg"

class vunerability(card):
	name = "Vunerability"
	vp = 0
	ctype = cardtype.STARTER
	image = "base/images/cards/Vulnerability.jpg"

class punch(card):
	name = "Punch"
	vp = 0
	ctype = cardtype.STARTER
	text = "+1 Power"
	image = "base/images/cards/Punch.jpg"
	
	def play_action(self,player):
		return 1

class kick(card):
	name = "Kick"
	vp = 1
	cost = 3
	ctype = cardtype.SUPERPOWER
	owner_type = owners.KICK
	text = "+2 Power"
	image = "base/images/cards/Kick.jpeg"
	
	def play_action(self,player):
		return 2