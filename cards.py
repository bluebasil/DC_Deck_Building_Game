import cardtype
import owners
import effects
import option
import globe
import ai_hint

#TODO: Impliment Attacks

class card_class:
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
	#should i track this?
	home = None

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

	def buy_action(self):
		return

	#defence = True must be set or this will not be an option
	#pop_self will come in handy
	def defend(self):
		return

	#Only used for cards in the supervilalin stack
	def first_apearance(self):
		return

	def attack_action(self):
		return

	def destroy(self):
		self.pop_self()
		owner = None
		self.owner_type = owners.DESTROYED
		globe.boss.destroyed_stack.add(self)


	def pop_self(self):
		if self in self.owner.hand.contents:
			self.owner.hand.contents.remove(self)
		elif self in self.owner.discard.contents:
			self.owner.discard.contents.remove(self)
		elif self in self.owner.ongoing.contents:
			self.owner.ongoing.contents.remove(self)
		elif self in self.owner.played.contents:
			self.owner.played.contents.remove(self)
		elif self in self.owner.deck.contents:
			self.owner.deck.contents.remove(self)
		elif self in globe.boss.lineup.contents:
			globe.boss.lineup.contents.remove(self)
		elif self in globe.boss.destroyed_stacks.contents:
			globe.boss.destroyed_stacks.contents.remove(self)
		return self
		


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

#TODO: Not Done UI
class aquamans_trident(card_class):
	name = "Auquaman's Trident"
	vp = 1
	cost = 3
	ctype = cardtype.EQUIPMENT
	text = "+2 Power\nYou may put any one card you buy or gain this turn on top of your deck."

	def play_action(self,player):
		player.gain_redirect.append(player.deck)
		return 2

#TODO: Attack
class bane(card_class):
	name = "Bane"
	vp = 1
	cost = 4
	ctype = cardtype.VILLAIN
	text = "+2 Power"
	attack = True
	attack_text = "Attack:: Each foe chooses and discards a card."

	def play_action(self,player):
		return 2

	def attack_action(self):
		return

#done
class the_batmobile(card_class):
	name = "The Batmobile"
	vp = 1
	cost = 2
	ctype = cardtype.EQUIPMENT
	text = "If this is the first card you play this turn, discard your hand and draw 5 cards.  Otherwise, +1 Power"

	def play_action(self,player):
		if self.owner.played.size() == 1:
			self.owner.discard_hand()
			for i in range(5):
				self.owner.draw_card()
			return 0
		else:
			return 1

#done
class the_bat_signal(card_class):
	name = "The Bat-Signal"
	vp = 1
	cost = 5
	ctype = cardtype.EQUIPMENT
	text = "+1 Power.  Put a Hero from your discard pile into your hand."

	def play_action(self,player):
		instruction_text = "Choose a Hero from you discard pile to put into your hand"
		assemble = []
		for c in player.discard.contents:
			if c.ctype == cardtype.HERO:
				assemble.append(c)
		if len(assemble) > 0:
			choosen = effects.choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			#if choosen != None
			player.hand.add(choosen.pop_self())
		return 1

#TODO: test vp
class bizarro(card_class):
	name = "Bizzaro"
	vp = 1
	cost = 7
	ctype = cardtype.VILLAIN
	text = "+3 Power.  At the end of the game, this card is worth 2 VP's for each Weakness in your deck."
	
	def play_action(self,player):
		return 3

	def calculate_vp(self):
		return 2*self.owner.deck.get_count(cardtype.WEAKNESS) + 1

#TODO: Defence
class blue_beetle(card_class):
	name = "Blue Beetle"
	vp = 2
	cost = 6
	ctype = cardtype.HERO
	defence = True
	text = "+3 Power.  Defense: You may reveal this card from your hand to avoid an Attack. (It stays in your hand)"
	
	def play_action(self,player):
		return 3

#TODO: Defence
class bulletproof(card_class):
	name = "Bulletproof"
	vp = 1
	cost = 4
	ctype = cardtype.SUPERPOWER
	defence = True
	text = "+2 Power.  Defense: You may discard this card to avoid an Attack.  If you do, draw a card and you may destroy a card in your discard pile."
	
	def play_action(self,player):
		return 2

#TODO: Defence
class the_cape_and_cowl(card_class):
	name = "The Cape and Cowl"
	vp = 1
	cost = 4
	ctype = cardtype.EQUIPMENT
	defence = True
	text = "+2 Power.  Defense: You may discard this card to avoid an Attack.  If you do, draw two cards."
	
	def play_action(self,player):
		return 2

#done
class catwoman(card_class):
	name = "Catwoman"
	vp = 1
	cost = 2
	ctype = cardtype.HERO
	text = "+2 Power"

	def play_action(self,player):
		return 2

#TODO: Test
class cheetah(card_class):
	name = "Cheetah"
	vp = 1
	cost = 2
	ctype = cardtype.VILLAIN
	text = "Gain any card with cost 4 or less from the Line-Up."

	def play_action(self,player):
		instruction_text = "Choose a one of these to gain from the Line-Up"
		assemble = []
		for c in globe.boss.lineup.contents:
			if c.cost <= 4:
				assemble.append(c)
		if len(assemble) > 0:
			choosen = effects.choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			#if choosen != None
			player.gain(choosen.pop_self())
		return 0

#TODO: Test
class clayface(card_class):
	name = "Clayface"
	vp = 1
	cost = 4
	ctype = cardtype.VILLAIN
	text = "Choose a card you played this turn.  Play it again this turn.  (Effects and Power generated the first time you played it remain.)"

	def play_action(self,player):
		instruction_text = "Choose a card that you have already played to play again"
		assemble = []
		for c in player.played.contents:
			assemble.append(c)
		if len(assemble) > 0:
			choosen = effects.choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			player.played.play(choosen)
			#To avoid it being in the played list twise
			#This is suposed to only remove 1 instance of the element
			player.played.contents.remove(choosen)
		return 0

#Test, especially catwoman special, but its not done its UI
class the_dark_knight(card_class):
	name = "The Dark Knight"
	vp = 1
	cost = 5
	ctype = cardtype.HERO
	text = "+2 Power.  Gain all Equipment in the Line-Up.  Then, if you play or have gained Catwoman this turn, you may put a card you bought or gained this turn into your hand."

	def play_action(self,player):
		assemble = []
		for c in globe.boss.lineup.contents:
			if c.ctype == cardtype.EQUIPMENT:
				assemble.append(c)
		for c in assemble:
			player.gain(c.pop_self())
		for c in player.played.contents:
			if c.name == "Catwoman":
				player.gain_redirect.append(player.hand)
				for c in player.gained_this_turn:
					if player.controler.may_put_on_top(f"Would you like to put {c.name} into your hand?",self):
						player.gain_redirect.remove(player.hand)
						player.hand.add(c.pop_self())
		return 2

#Done
class doomsday(card_class):
	name = "Doomsday"
	vp = 2
	cost = 6
	ctype = cardtype.VILLAIN
	text = "+4 Power"

	def play_action(self,player):
		return 4

#Test
class the_emerald_knight(card_class):
	name = "The Emerald Knight"
	vp = 1
	cost = 5
	ctype = cardtype.HERO
	text = "Remove an Equipment, Hero, or Super Power from the Line-Up.  Play it, then return it to the Line-Up at the end of your turn."
	played_card = None

	def play_action(self,player):
		instruction_text = "Choose one of these from the line up, play it, then return it at the end of the turn"
		assemble = []
		for c in globe.boss.lineup:
			if c.ctype == cardtype.EQUIPMENT or c.ctype == cardtype.HERO or c.ctype == cardtype.SUPERPOWER:
				assemble.append(c)
		if len(assemble) > 0:
			choosen = effects.choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			self.played_card = choosen
			player.played.play(choosen)
		return 0

	def end_of_turn(self):
		globe.boss.lineup.add(self.played_card.pop_self())
		return

#Done
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

#Done
class gorilla_grodd(card_class):
	name = "Grorilla Grodd"
	vp = 2
	cost = 5
	ctype = cardtype.HERO
	text = "+3 Power"

	def play_action(self,player):
		return 3

#TODO: need testing calculating vp
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
		if self.owner.deck.get_count(cardtype.HERO) > 4:
			return 5
		else:
			return 0

#Test
class green_arrows_bow(card_class):
	name = "Green Arrow's Bow"
	vp = 1
	cost = 4
	ctype = cardtype.EQUIPMENT
	text = "+2 Power.  Super-Villains cost you 2 less to defeat this turn."

	def play_action(self,player):
		player.discount_on_sv += 2
		return 2

#ATTACk
class harley_quinn(card_class):
	name = "Harley Quinn"
	vp = 1
	cost = 2 
	ctype = cardtype.VILLAIN
	text = "+1 Power"
	attack = True
	attack_text = "Attack: Each foe puts a Punch or Vulnerability from his discard pile on top of his deck."

	def play_action(self,player):
		return 1

	def attack_action(self):
		return

#done
class heat_vision(card_class):
	name = "Heat Vision"
	vp = 2
	cost = 6
	ctype = cardtype.SUPERPOWER
	text = "+3 Power\nYou may destory a card in your hand or discard pile."

	def play_action(self,player):
		effects.may_destroy_card_in_hand_or_discard(player)
		return 3

#Done
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

#Test
class jonn_jonzz(card_class):
	name = "J'onn J'onzz"
	vp = 2
	cost = 6
	ctype = cardtype.HERO
	text = "Play the top card of the Super-Villain stack, then return it to the stack.  (The First Appearance - Attack does not happen.)"

	def play_action(self,player):
		top_of_sv = globe.boss.supervillain_stack.contents.pop()
		player.played.play(top_of_sv)
		player.played.contents.remove(top_of_sv)
		globe.boss.supervillain_stack.add(top_of_sv)
		return 0

#Done
class kid_flash(card_class):
	name = "Kid Flash"
	vp = 1
	cost = 2
	ctype = cardtype.HERO
	text = "Draw a card"

	def play_action(self,player):
		player.draw_card()
		return 0

#done
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

#Test
class lobo(card_class):
	name = "Lobo"
	vp = 2
	cost = 7
	ctype = cardtype.VILLAIN
	text = "+3 Power.  You may destroy up to two cards in your hand and/or discard pile."

	def play_action(self,player):
		for i in range(2):
			effects.may_destroy_card_in_hand_or_discard(player)
		return 3

#Test
class the_man_of_steel(card_class):
	name = "The Man of Steel"
	vp = 3
	cost = 8
	ctype = cardtype.HERO
	text = "+3 Power.  Put all Super Powers from your discard pile into your hand."

	def play_action(self,player):
		assemble = []
		for c in player.discard.contents:
			if c.ctype == cardtype.SUPERPOWER:
				assemble.append(c)
		for c in assemble:
			player.hand.add(c.pop_self())
		return 

#Test
class mera(card_class):
	name = "Mera"
	vp = 1
	cost = 3
	ctype = cardtype.HERO
	text = "If your discard pile is empty, +4 Power.  Otherwise, +2 Power."

	def play_action(self,player):
		if player.discard.size() == 0:
			return 4
		return 2

#test
class nth_metal(card_class):
	name = "Nth Metal"
	vp = 1
	cost = 3
	ctype = cardtype.EQUIPMENT
	text = "+1 Power.  Look at the top of your deck.  You may destroy it."

	def play_action(self,player):
		top_card = player.deck.contents[-1]
		if effects.ok_or_no(f"This card is on top of your deck, would you like to destroy it? (ok/no)",player,top_card,ai_hint.IFBAD):
			top_card.destroy()
		return 

# Test
class the_penguin(card_class):
	name = "The Penguin"
	vp = 1
	cost = 3
	ctype = cardtype.VILLAIN
	text = "Draw two cards, then choose and discard two cards from your hand."

	def play_action(self,player):
		for i in range(2):
			player.draw_card()
		for i in range(2):
			effects.discard_a_card(player)
		return 0

#TODO: attack
class poison_ivy(card_class):
	name = "Poison Ivy"
	vp = 1
	cost = 3
	ctype = cardtype.VILLAIN
	text = "+1 Power"
	attack = True
	attack_text = "Attack:: Each foe discards the top card of his deck.  If its cost is 1 or greater, that player gains a Weakness."

	def play_action(self,player):
		return 1
		#attack needed


#TODO: TEST, i dont think UI will work properly
class power_ring(card_class):
	name = "Power Ring"
	vp = 1
	cost = 3
	ctype = cardtype.EQUIPMENT
	text = "Reveal the top card of your deck.  If its cost is 1 or greater, +3 Power.  Otherwise, +2 Power."

	def play_action(self,player):
		top_card = player.deck.contents[-1]
		effects.reveal("Top card of your deck:",player,[top_card])
		if top_card.cost >= 1:
			return 3
		return 2

#Test
class princess_diana_of_themyscira(card_class):
	name = "Princess Diana of Themyscira"
	vp = 2
	cost = 7
	ctype = cardtype.HERO
	text = "Gain all Villains with cost 7 or less in the Line-Up."

	def play_action(self,player):
		assemble = []
		for c in globe.boss.lineup.contents:
			if c.ctype == cardtype.VILLAIN and c.cost <= 7:
				assemble.append(c)
		for c in assemble:
			player.gain(c.pop_self())
		return 0

#test
class the_riddler(card_class):
	name = "The Riddler"
	vp = 1
	cost = 3
	ctype = cardtype.VILLAIN
	text = "You may pay 3 Power.  If you do, gain the top card of the main deck.  Use this ability any number of times this turn.  If you choose not to, +1 Power instead"

	def play_action(self,player):
		player.played_riddler = True
		return 1

#test
class robin(card_class):
	name = "Robin"
	vp = 1
	cost = 3
	ctype = cardtype.HERO
	text = "+1 Power.  Put an Equipment from your discard pile into your hand."

	def play_action(self,player):
		instruction_text = "Choose an Equipment from you discard pile to put into your hand"
		assemble = []
		for c in player.discard.contents:
			if c.ctype == cardtype.EQUIPMENT:
				assemble.append(c)
		if len(assemble) > 0:
			choosen = effects.choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			#if choosen != None
			player.hand.add(choosen.pop_self())
		return 1

#Attack
class scarecrow(card_class):
	name = "Scarecrow"
	vp = 1
	cost = 5
	ctype = cardtype.VILLAIN
	text = "+2 Power."
	attack = True
	attack_text = "Attack: Each foe gains a Weakness."

	def play_action(self,player):
		return 2

	def attack_action(self):
		return

#TEst
class solomon_grundy(card_class):
	name = "Solomon Grundy"
	vp = 2
	cost = 6
	ctype = cardtype.VILLAIN
	text = "When you buy or gain this Villain, you may put him on top of your deck.  +3 Power."

	def play_action(self,player):
		return 3

	def buy_action(self):
		self.owner.gain_redirect.append(self.owner.deck)

Starro

#TEst
class starro(card_class):
	name = "Starro"
	vp = 2
	cost = 7
	ctype = cardtype.VILLAIN
	text = ""
	attack = True
	attack_text = "Attack: Each foe discards the top card of his deck.  You may play each non-Location discarded this way this turn."

	def play_action(self,player):
		return 0

	def attack_action(self):
		return

#TODO: Suiside ability
class suicide_squad(card_class):
	name = "Suicide Squad"
	vp = '*'
	cost = 4
	ctype = cardtype.VILLAIN
	text = "+2 Power\nIf you already played two other Suicide Squad cards this turn, each foe discards his hand.\nAt the end of the game, this card is worth 1 VP for each Suiside Squad in your deck."

	def play_action(self,player):
		count = 0
		for c in player.played.contents:
			if c.name == "Suicide Squad":
				count += 1
		#This card has been played
		if count >= 3:
			for p in globe.boss.players:
				if p != player:
					p.discard_hand()
		return 2
		# Suidide ability needed

	def calculate_vp(self):
		count = 0
		for c in self.owner.deck:
			if c.name == "Suicide Squad":
				count += 1
		return count

#TODO: Defence
class super_speed(card_class):
	name = "Super Speed"
	vp = 1
	cost = 3
	ctype = cardtype.SUPERPOWER
	defence = True
	text = "Draw a card.  Defense: You may discard this card to avoid an Attack.  If you do, draw two cards."

	def play_action(self,player):
		player.draw_card()
		return 0

	def defend(self):
		return

#Done
class super_strength(card_class):
	name = "Super Strength"
	vp = 2
	cost = 7
	ctype = cardtype.SUPERPOWER
	text = "+5 Power"

	def play_action(self,player):
		return 5

##############################

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
		self.pop_self()
		self.owner.deck.insert(0,self)
		return

class the_anti_monitor(card_class):
	name = "The Anti-Monitor"
	vp = 6
	cost = 12
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+2 Power.\n Destroy any number of cards in the Line-Up, then replace them."
	attack_text = "First Appearance - Attack:: Each player reveals his hand, chooses a card with cost 1 or greater from it, and adds that card to the Line-Up."

	def play_action(self,player):
		effects.replace_cards_in_lineup(player)
		return 2

	def first_apearance(self):
		for p in globe.players:
			effects.fa_add_card_to_lineup(self,p)
		return

class atrocitus(card_class):
	name = "Atrocitus"
	vp = 5
	cost = 10
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+2 Power.\n Destroy up to two cards in your discard pile.\n First Appearance - Attack:: Each player puts a random card from his hand under his Super Hero.  When this Villain is defeated, put each of those cards on top of it's owner's deck."

	def play_action(self,player):
		for i in range(2):
			effects.may_destroy_card_in_discard(player)
		return 2

	def first_apearance(self):
		for p in globe.players:
			effects.fa_hide_card_under_superhero(self,p)
		return

	def buy_action(self):
		for p in globe.players:
			affects.return_hidden_cards()
		return


class black_manta(card_class):
	name = "Black Manta"
	vp = 4
	cost = 8
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+3 Power and draw a card."
	attack_text = "First Appearance - Attack:: Each player discards the top card of his deck.  If you discarded a card with cost 1 or more, choose one: Destroy it, or discard your hand."

	def play_action(self,player):
		player.draw_card()
		return 3

	def first_apearance(self):
		for p in globe.boss.players:
			card = effects.discard_top_of_deck(p)
			if card != None:
				effects.fa_destroy_or_discard_hand(self,p,card)
		return

class brainiac(card_class):
	name = "Brainiac"
	vp = 6
	cost = 11
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "Each player reveals a random card from his hand."
	attack_text = "Play each revealed non-Location.\n First Appearance - Attack:: Each player chooses two cards from his hand and puts them on the table face down.  Shuffle all of the chosen cards face down, then deal two back to each player at random."

	def play_action(self,player):
		effects.play_random_card_from_opponents_hands(player)
		return 0

	def first_apearance(self):
		cards_to_shuffle = []
		participating_players = []
		for p in globe.boss.players:
			cards_to_add = effects.fa_random_shuffle_two_cards(self,p)
			if len(cards_to_add) > 0:
				participating_players.append(p)	
				cards_to_shuffle.extend(cards_to_add)
		random.Shuffle(cards_to_shuffle)
		for i in range(2):
			for p in participating_players:
				if len(cards_to_shuffle) > 0:
					p.hand.add(cards_to_shuffle.pop())
		return

class captain_cold(card_class):
	name = "Captain Cold"
	vp = 5
	cost = 9
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+2 Power, and an additional +1 Power for each foe with a Hero in his discard pile."
	attack_text = "First Appearance - Attack:: Each player flips his Super Hero face down until this Villain is defeated."

	def play_action(self,player):
		power = 2
		for p in globe.boss.players:
			if p != player:
				if p.discard.get_count(cardtype.HERO) > 0:
					power += 1
		return power

	def first_apearance(self):
		for p in globe.boss.players:
			affects.fa_disable_superhero(self,p)
		return

	def buy_action(self):
		for p in globe.boss.players:
			affects.enable_superhero(p)
		return

class darkseid(card_class):
	name = "Darkseid"
	vp = 6
	cost = 11
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "You may destroy two cards in your hand.\n If you do, +5 Power.  Otherwise, +3 Power."
	attack_text = "First Appearance - Attack:: Each player discards two cards unless he reveals a Villain from his hand."

	def play_action(self,player):
		power = 3
		if len(effects.may_destroy_two_cards(player)):
			power = 5
		return power

	def first_apearance(self):
		for p in globe.boss.players:
			effects.fa_reveal_villain_or_discard_two(self,player)
		return

class deathstroke(card_class):
	name = "Deathstroke"
	vp = 5
	cost = 9
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "You may gain a Hero or Villain from the Line-Up.\n If you choose not to, +3 Power."
	attack_text = "First Appearance - Attack:: Each player reveals his hand and destroys a Hero, Super Power or Equipment in his hand or discard pile."

	def play_action(self,player):
		if effects.gain_card_from_lineup() == None:
			return 3
		return 0

	def first_apearance(self):
		for p in globe.boss.players:
			effects.fa_destroy_hero_villain_superpower_in_hand_discard(self,p)
		return
		
class the_joker(card_class):
	name = "The Joker"
	vp = 5
	cost = 10
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "+2 Power and each foe chooses: He discards a random card, or you draw a card."
	attack_text = "First Appearance - Attack:: Each player puts a card from his hand into the discard pile of the player on his left.  If the card you received has a cost of 1 or greater, gain a Weakness"

	def play_action(self,player):
		for p in globe.boss.players:
			if effects.may_discard_a_card() == None:
				player.draw()
		return 2

	def first_apearance(self):
		cards_to_shuffle = []
		participating_players = []
		for p in globe.boss.players:
			card_to_give = effects.fa_card_in_discard_to_left(self,p)
			if card_to_give != None:
				participating_players.append(p)
				cards_to_shuffle.append(card_to_give)
		for i,p in enumerate(participating_players):
			card_recived = cards_to_shuffle[i-1]
			p.discard.add(card_recived)
			if card_recived.cost > 0:
				p.gain_a_weakness()
		return

class lex_luther(card_class):
	name = "Lex Luther"
	vp = 5
	cost = 10
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "Draw three cards."
	attack_text = "First Appearance - Attack:: Each player gains a Weakness for each Villain in the Line-Up."

	def play_action(self,player):
		for i in range(3):
			player.draw_card()
		return 0

	def first_apearance(self):
		for p in globe.boss.players:
			effects.fa_gain_weakness_villains_lineup(self,p)
		return

class parallax(card_class):
	name = "Parallax"
	vp = 6
	cost = 12
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "Double your Power this turn."
	attack_text = "First Appearance - Attack:: Each player reveals his hand and discards all cards with cost 2 or less."

	def play_action(self,player):
		player.played.parallax_double()
		return 0

	def first_apearance(self):
		for p in globe.boss.players:
			effects.fa_discard_two_or_less(self,p)
		return

class sinestro(card_class):
	name = "Sinestro"
	vp = 5
	cost = 10
	ctype = cardtype.VILLAIN
	owner_type = owners.VILLAINDECK
	text = "Reveal the top card of the main deck.  If it's a Hero, +3 Power and then destroy it.  Otherwise, put it in your hand."
	attack_text = "First Appearance - Attack: Each player reveals his hand and discards a card for each Hero revealed this way."

	def play_action(self,player):
		if len(globe.boss.main_deck.contents) > 0 and globe.boss.main_deck.contents[-1].ctype == cardtype.HERO:
			globe.boss.main_deck.contents.pop().destroy()
			return 3
		else:
			new_card = globe.boss.main_deck.contents.pop()
			#ownership change
			new_card.owner = player
			new_card.owner_type = owners.PLAYER
			player.hand.add(new_card)
			return 0

	def first_apearance(self):
		for p in globe.boss.players:
			effects.fa_discard_based_on_heros(self,p)
		return




