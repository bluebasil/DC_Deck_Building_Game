import cardtype
import owners
import effects
import option

#TODO: Impliment Attacks

class card_class:
	name = ""
	vp = 0
	cost = 0
	ctype = cardtype.ANY
	#All cards must manually set these
	defence = False
	owner = None
	owner_type = owners.MAINDECK
	text = ""

	def __init__(self,owner = None):
		self.owner = owner
		if owner != None:
			self.owner_type = owners.PLAYER

	def play_action(self,player):
		return 0

	def set_owner(self,player=None):

		self.owner = player
		self.owner_type = owners.PLAYER

	def calculate_vp(self):
		return self.vp

	def end_of_turn(self):
		return


#	def check_defence(self):
#		if self.defence == None:
#			return False
#		else:
#			return True

#	def defence_action(self):
#		if self.defence != None:
#			return defence()


class weakness(card_class):
	name = "Weakness"
	vp = -1
	ctype = cardtype.WEAKNESS
	owner_type = owners.WEAKNESS

class vunerability(card_class):
	name = "Vunerability"
	vp = 0
	ctype = cardtype.STARTER

class punch(card_class):
	name = "Punch"
	vp = 0
	ctype = cardtype.STARTER
	text = "+1 Power"

	def play_action(self,player):
		return 1

class kick(card_class):
	name = "Kick"
	vp = 1
	cost = 3
	ctype = cardtype.SUPERPOWER
	owner_type = owners.KICK
	text = "+2 Power"

	def play_action(self,player):
		return 2

#TODO: Trident ability not implimented
class aquamans_trident(card_class):
	name = "Auquaman's Trident"
	vp = 1
	cost = 3
	ctype = cardtype.EQUIPMENT
	text = "+2 Power\nYou may put any one card you buy or gain this turn on top of your deck."

	def play_action(self,player):
		return 2


class bane(card_class):
	name = "Bane"
	vp = 1
	cost = 4
	ctype = cardtype.VILLAIN
	text = "+2 Power\nAttack:: Each foe chooses and discards a card."

	def play_action(self,player):
		return 2
		#attack needed

class fastest_man_alive(card_class):
	name = "The Fastest Man Alive"
	vp = 1
	cost = 5
	ctype = cardtype.HERO
	text = "Draw two cards"

	def play_action(self,player):
		for i in range(2):
			player.draw_card()
		return 0

class green_arrow(card_class):
	name = "Green Arrow"
	vp = '*'
	cost = 5
	ctype = cardtype.HERO
	text = "+2 Power\nAt the end of the game, if you have four or more other Heroes in your deck, this card is worth 5 VPs."

	def play_action(self,player):
		return 2

	def calculate_vp(self):
		count = 0
		if self.owner.deck.get_count(self.owner.pid,cardtype.HERO) > 4:
			return 5
		else:
			return 0

class heat_vision(card_class):
	name = "Heat Vision"
	vp = 2
	cost = 6
	ctype = cardtype.SUPERPOWER
	text = "+3 Power\nYou may destory a card in your hand or discard pile."

	def play_action(self,player):
		effects.may_destroy_card_in_hand_or_discard(player)
		return 3

class high_tech_hero(card_class):
	name = "High-Tech HERO"
	vp = 1
	cost = 3
	ctype = cardtype.HERO
	text = "If you have played a Super Power or Equipment this turn, +3 Power.\nOtherwise, +1 Power."

	def play_action(self,player):
		if player.played.get_count(cardtype.SUPERPOWER) > 0 \
				or player.played.get_count(cardtype.EQUIPMENT) > 0:
			return 3
		else:
			return 1

class king_of_atlantis(card_class):
	name = "King of Atlantis"
	vp = 1
	cost = 5
	ctype = cardtype.HERO
	text = "You may destroy a card in your discard pile.  If you do, +3 Power.  Otherwise, +1 Power"

	def play_action(self,player):
		choice = effects.may_destroy_card_in_discard(player)
		if choice[0] == option.NO:
			return 1
		else:
			return 3

#TODO: Defence
class lasso_of_truth(card_class):
	name = "Lasso of Truth"
	vp = 1
	cost = 2
	ctype = cardtype.EQUIPMENT
	text = "+1 Power\nDefence:: You may discard this card to avoid an Attack.  If you do, draw a card."

	def play_action(self,player):
		return 1

class poison_ivy(card_class):
	name = "Poison Ivy"
	vp = 1
	cost = 3
	ctype = cardtype.VILLAIN
	text = "+1 Power\nAttack:: Each foe discards the top card of his deck.  If its cost is 1 or greater, that player gains a Weakness."

	def play_action(self,player):
		return 1
		#attack needed

class suicide_squad(card_class):
	name = "Suicide Squad"
	vp = '*'
	cost = 4
	ctype = cardtype.VILLAIN
	text = "+2 Power\nIf you already played two other Suicide Squad cards this turn, each foe discards his hand.\nAt the end of the game, this card is worth 1 VP for each Suiside Squad in your deck."

	def play_action(self,player):
		return 2
		# Suidide ability needed

	def calculate_vp(self):
		count = 0
		for c in self.owner.deck:
			if c.name == "Suicide Squad":
				count += 1
		return count

#TODO: allow to place back on top of players deck
class x_ray_vision(card_class):
	name = "X-Ray Vision"
	vp = 1
	cost = 3
	ctype = cardtype.SUPERPOWER
	text = "Each foe reveals the top card of his deck. You may play one of the non-Location cards revealed this eay this turn, then return it to the top of it's owner's deck."

	def play_action(self,player):
		effects.x_ray_vision_reveal(player)
		return 0






#SuperVillains
class ras_al_ghul(card_class):
	name = "Ra's Al Ghul"
	vp = 4
	cost = 8
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+3 Power\nAt the end of your turn, put this card on the bottom of its owners deck before drawing a new hand."

	def play_action(self,player):
		return 3

	def end_of_turn(self):
		return






