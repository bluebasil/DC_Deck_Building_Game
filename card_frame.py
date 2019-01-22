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
	#List of pid's of who has a frozen token on this card
	frozen = []


	#stats
	times_played = 0
	bought = False

	def __init__(self,owner = None):
		self.owner = owner
		if owner != None:
			self.owner_type = owners.PLAYER
		self.texture = arcade.load_texture(self.image)
		self.frozen = []

	def get_ctype(self):
		return [self.ctype]

	def ctype_eq(self,ctype):
		return self.ctype == ctype
	
	def play_action(self,player):
		return 0

	#def later_play(self,player,on_card):
	#	return 0

	def set_owner(self,player=None):
		if player == owners.WEAKNESS \
				or player == owners.MAINDECK \
				or player == owners.KICK \
				or player == owners.DESTROYED \
				or player == owners.VILLAINDECK \
				or player == owners.LINEUP:
			self.owner = None
			self.owner_type = player
		else:
			self.owner = player
			self.owner_type = owners.PLAYER

	def calculate_vp(self,all_cards):
		return self.vp

	def end_of_turn(self):
		return

	def buy_action(self,player):
		return

	#defence = True must be set or this will not be an option
	#pop_self will come in handy
	def defend(self,attacker = None,defender = None):
		return

	#Only used for cards in the supervilalin stack
	def first_apearance(self):
		return

	def attack_action(self,by_player):
		return

	def destroy(self,player_responsible):
		self.pop_self()
		player_responsible.persona.destory_power()
		self.set_owner(owners.DESTROYED)
		globe.boss.destroyed_stack.add(self)


	def pop_self(self):
		location = self.find_self()
		#print(self.name,location[0].name,location[1])
		location[0].contents.remove(self)
		return self

		"""
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
			#Firestorm.  May interact weirdly, firestorm always puts it back on superhero i think
			elif self in self.owner.over_superhero.contents:
				self.owner.over_superhero.contents.remove(self)
				if globe.DEBUG:
					print(f"{self.name} pop from over_superher")
		return self"""

	def find_self(self):
		#why am i not checking by ownership type?
		if self in globe.boss.lineup.contents:
			return (globe.boss.lineup,globe.boss.lineup.contents.index(self))
		elif self in globe.boss.destroyed_stack.contents:
			return (globe.boss.destroyed_stack,globe.boss.destroyed_stack.contents.index(self))
		elif self in globe.boss.main_deck.contents:
			return (globe.boss.main_deck,globe.boss.main_deck.contents.index(self))
		elif self in globe.boss.kick_stack.contents:
			return (globe.boss.kick_stack,globe.boss.kick_stack.contents.index(self))
		elif self in globe.boss.weakness_stack.contents:
			return (globe.boss.weakness_stack,globe.boss.weakness_stack.contents.index(self))
		elif self in globe.boss.supervillain_stack.contents:
			return (globe.boss.supervillain_stack,globe.boss.supervillain_stack.contents.index(self))
		for p in globe.boss.players:
			if self in p.hand.contents:
				return (p.hand,p.hand.contents.index(self))
			elif self in p.discard.contents:
				return (p.discard,p.discard.contents.index(self))
			elif self in p.ongoing.contents:
				return (p.ongoing,p.ongoing.contents.index(self))
			elif self in p.played.contents:
				return (p.played,p.played.contents.index(self))
			elif self in p.deck.contents:
				return (p.deck,p.deck.contents.index(self))
			elif self in p.under_superhero.contents:
				return (p.under_superhero,p.under_superhero.contents.index(self))
			#Firestorm.  May interact weirdly, firestorm always puts it back on superhero i think
			elif self in p.over_superhero.contents:
				return (p.over_superhero,p.over_superhero.contents.index(self))
		#return self
		

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