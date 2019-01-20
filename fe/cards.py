import cardtype
import owners
import effects
import option
import globe
import ai_hint
import random
import arcade
import actions
import card_frame

#Done
class amanda_waller(card_frame.card):
	name = "Amanda Waller"
	vp = 1
	cost = 4
	ctype = cardtype.HERO
	text = "You may destroy a card in your hand or discard pile.\nIf it's a Villain, +Power equal to it's cost.\nIf you choose not to, +2 Power."
	image = "fe/images/cards/Amanda Waller.jpg"
	
	def play_action(self,player):
		#effects.may_destroy_card_in_hand_or_discard(player)
		collection = player.hand.contents.copy()
		collection.extend(player.discard.contents)
		instruction_text = "You may destroy a card in your hand or discard pile.\nIf it's a Villain, +Power equal to it's cost.\nIf you choose not to, +2 Power."
		card_to_destroy = effects.may_choose_one_of(instruction_text,player,collection,ai_hint.IFBAD)
		if card_to_destroy == None:
			return 2
		else:
			card_to_destroy.destroy(player)
			if card_to_destroy.ctype_eq(cardtype.VILLAIN):
				return card_to_destroy.cost
		return 0

#Done
class atomica(card_frame.card):
	name = "Atomica"
	vp = 1
	cost = 3
	ctype = cardtype.VILLAIN
	text = "You may destroy a non-Villain card in your hand or discard pile. If its cost is 1 or greater, gain 1 VP."
	image = "fe/images/cards/Atomica 3.jpg"
	
	def play_action(self,player):
		#effects.may_destroy_card_in_hand_or_discard(player)
		assemble = []
		for c in player.hand.contents:
			if not c.ctype_eq(cardtype.VILLAIN):
				assemble.append(c)
		for c in player.discard.contents:
			if not c.ctype_eq(cardtype.VILLAIN):
				assemble.append(c)
		instruction_text = "You may destroy a card in your hand or discard pile.\nIf it's a Villain, +Power equal to it's cost.\nIf you choose not to, +2 Power."
		card_to_destroy = effects.may_choose_one_of(instruction_text,player,assemble,ai_hint.IFBAD)
		if card_to_destroy != None:
			card_to_destroy.destroy(player)
			if card_to_destroy.cost >= 1:
				player.gain_vp(1)
		return 0

#Done
class bizarro_power(card_frame.card):
	name = "Bizarro Power"
	vp = -1
	cost = 6
	ctype = cardtype.SUPERPOWER
	text = "+4 Power and gain a Weakness."
	attack = True
	attack_text = "Attack:: Each foe gains a Weakness"
	image = "fe/images/cards/Bizarro Power.jpg"
	
	def play_action(self,player):
		player.gain_a_weakness()
		self.attack_action(player)
		return 4

	def attack_action(self,by_player):
		for p in globe.boss.players:
			if p != by_player and effects.attack(p,self,by_player):
				p.gain_a_weakness()
		return


#Done
class broadsword(card_frame.card):
	name = "Broadsword"
	vp = 2
	cost = 6
	ctype = cardtype.EQUIPMENT
	text = "+2 Power and choose a foe."
	attack = True
	attack_text = "Attack:: Destroy a card with cost 1,2, or 3 in that\nfoe's discard pile."
	image = "fe/images/cards/Broadsword.jpg"
	
	def play_action(self,player):
		self.attack_action(player)
		return 2

	def attack_action(self,by_player):
		#r(instruction_text,player,includes_self = True):
		player = effects.choose_a_player("Choose a player to destroy a cost 1,2, or 3 card from their discard",by_player,False)
		if effects.attack(player,self,by_player):
			assemble = []
			for c in player.discard.contents:
				if c.cost >= 1 and c.cost <= 3:
					assemble.append(c)
			if len(assemble) > 0:
				result = effects.choose_one_of(f"destroy a cost 1,2, or 3 card from {player.persona.name}'s' discard.",by_player,assemble,hint = ai_hint.BEST)
				result.destroy(by_player)
		return

#Done
class catwoman(card_frame.card):
	name = "Catwoman"
	vp = 1
	cost = 3
	ctype = cardtype.HERO
	text = "+1 Power and choose a foe."
	attack = True
	attack_text = "Attack:: Steal 1 VP from that foe"
	image = "fe/images/cards/Catwoman 3 Fe.jpg"
	
	def play_action(self,player):
		self.attack_action(player)
		return 1

	def attack_action(self,by_player):
		#r(instruction_text,player,includes_self = True):
		player = effects.choose_a_player("Choose a player to steal 1 VP from",by_player,includes_self = False)
		if effects.attack(player,self,by_player):
			if player.vp >= 1:
				player.vp -= 1
				by_player.gain_vp(1)
		return

#Done
class cold_gun(card_frame.card):
	name = "Cold Gun"
	vp = 1
	cost = 2
	ctype = cardtype.EQUIPMENT
	text = "+1 Power\nYou may put a Frozen token on a card in the Line-up.\nIf you do, remove it at the start of your next turn."
	image = "fe/images/cards/Cold Gun 2.jpg"
	
	def play_action(self,player):
		instruction_text = "You may put a Frozen token on a card in the Line-up"
		result = effects.may_choose_one_of(instruction_text,player,globe.boss.lineup.contents,ai_hint.RANDOM)
		if result != None:
			result.frozen.append(player.pid)
		return 1

#Done
class commissioner_gordon(card_frame.card):
	name = "Commissioner Gordon"
	vp = 1
	cost = 2
	ctype = cardtype.HERO
	defence = True
	text = "+1 Power.  Defense: You may discard this card to avoid an Attack.  If you do, gain 1 VP."
	image = "fe/images/cards/Commissioner Gordon.jpg"
	
	def play_action(self,player):
		return 1

	def defend(self):
		self.owner.discard_a_card(self)
		self.owner.gain_vp(1)
		return

#Done
class constructs_of_fear(card_frame.card):
	name = "Constructs Of Fear"
	vp = 2
	cost = 7
	ctype = cardtype.SUPERPOWER
	text = "+3 Power"
	attack = True
	attack_text = "Attack:: Each foe discards two cards."
	image = "fe/images/cards/Constructs of Fear.jpg"
	
	def play_action(self,player):
		self.attack_action(player)
		return 3

	def attack_action(self,by_player):
		for p in globe.boss.players:
			if p != by_player and effects.attack(p,self,by_player):
				for i in range(2):
					if len(p.hand.contents) > 0:
						result = effects.choose_one_of(f"Choose a card to discard. ({i}/2)",p,p.hand.contents,ai_hint.WORST)
						p.discard_a_card(result)
		return

class cosmic_staff(card_frame.card):
	name = "Cosmic Staff"
	vp = 1
	cost = 5
	ctype = cardtype.EQUIPMENT
	defence = True
	text = "+2 Power.  Defense: You may discard this card to avoid an Attack.  If you do, gain the bottom of the main deck."
	image = "fe/images/cards/Cosmic Staff.jpg"
	
	def play_action(self,player):
		return 2

	def defend(self):
		self.owner.discard_a_card(self)
		self.owner.gain(globe.boss.main_deck.contents[0])
		return

class deathstorm(card_frame.card):
	name = "Deathstorm"
	vp = '*'
	cost = 4
	ctype = cardtype.VILLAIN
	text = "You may destroy a card in your hand.\nAt the end of the game, this card is worth 10 - 1 fewer VP for each\ncard in excess of 20 in your deck. (Minimum 0)"
	image = "fe/images/cards/Deathstorm.jpg"
	
	def play_action(self,player):
		instruction_text = "You may destroy a card in your hand."
		result = effects.may_choose_one_of(instruction_text,player,player.hand.contents,ai_hint.IFBAD)
		if result != None:
			result.destroy(player)
		return 0

	def calculate_vp(self,all_cards):
		return max(0,10 - max(0,(len(all_cards)-20)))

class despero(card_frame.card):
	name = "Despero"
	vp = 2
	cost = 6
	ctype = cardtype.VILLAIN
	text = "Draw two cards and choose a foe."
	attack = True
	attack_text = "Attack:: That foe discards a card with cost 1 or greater"
	image = "fe/images/cards/Despero.jpg"
	
	def play_action(self,player):
		for i in range(2):
			player.draw_card()
		self.attack_action(player)
		return 0

	def attack_action(self,by_player):
		player = effects.choose_a_player("Choose a player to force to discard a cards costing 1 or greater.",by_player,False)
		if effects.attack(player,self,by_player):
			assemble = []
			for c in player.hand.contents:
				if c.cost >= 1:
					assemble.append(c)
			if len(assemble) > 0:
				result = effects.choose_one_of(f"Choose a card to discard.",player,assemble,ai_hint.WORST)
				player.discard_a_card(result)
		return


class dr_light(card_frame.card):
	name = "Dr. Light"
	vp = 1
	cost = 3
	ctype = cardtype.HERO
	text = "Draw a card and choose a foe."
	attack = True
	attack_text = "Attack:: That foe puts a Location he controls into his discard pile."
	image = "fe/images/cards/Dr Light.jpg"
	
	def play_action(self,player):
		player.draw_card()
		self.attack_action(player)
		return 0

	def attack_action(self,by_player):
		player = effects.choose_a_player("Choose a player to force to discard a location they control",by_player,includes_self = False,hint = ai_hint.RANDOM)
		if effects.attack(player,self,by_player):
			assemble = []
			for c in player.ongoing.contents:
				if c.ctype_eq(cardtype.LOCATION):
					assemble.append(c)
			if len(assemble) > 0:
				result = effects.choose_one_of(f"Choose a location to discard.",player,assemble,ai_hint.WORST)
				player.discard_a_card(result)
		return



class element_woman(card_frame.card):
	name = "Element Woman"
	vp = 1
	cost = 4
	ctype = cardtype.HERO
	text = "+2 Power\nWhile you own or are playing this card, it is also a Super Power, Equipment, and Villain."
	image = "fe/images/cards/Element Woman.jpg"
	
	def play_action(self,player):
		return 2

	def get_ctype(self):
		return [cardtype.HERO,cardtype.SUPERPOWER,cardtype.EQUIPMENT,cardtype.VILLAIN]

	def ctype_eq(self,ctype):
		if ctype == cardtype.SUPERPOWER or ctype == cardtype.EQUIPMENT or ctype == cardtype.VILLAIN or ctype == self.ctype:
			return True
		else:
			return False

#Done
class emperor_penguin(card_frame.card):
	name = "Emperor Penguin"
	vp = 0
	cost = 1
	ctype = cardtype.VILLAIN
	text = "When you destroy this card in any zone, gain 2 VPs."
	image = "fe/images/cards/Emperor Penguin.jpg"
	
	def destroy(self,player_responsible):
		player_responsible.gain_vp(2)
		super().destroy(player_responsible)



class expert_marksman(card_frame.card):
	name = "Expert Marksman"
	vp = 1
	cost = 3
	ctype = cardtype.SUPERPOWER
	text = "You may destroy a non-Super Power card in\nyour hand or discard pile. If its cost is 1 or\n greater, gain 1 VP."
	image = "fe/images/cards/Expert Marksman.jpg"
	
	def play_action(self,player):
		assemble = []
		for c in player.hand.contents:
			if not c.ctype_eq(cardtype.SUPERPOWER):
				assemble.append(c)
		for c in player.discard.contents:
			if not c.ctype_eq(cardtype.SUPERPOWER):
				assemble.append(c)
		if len(assemble) > 0:
			result = effects.may_choose_one_of(self.text,player,assemble,ai_hint.IFBAD)
			if result != None and result.cost >= 1:
				player.gain_vp(1)
		return 0


class firestorm_matrix(card_frame.card):
	name = "Firestorm Matrix"
	vp = 2
	cost = 7
	ctype = cardtype.EQUIPMENT
	text = 'Play the top card of your deck. If its cost is 5 or less, you may\ndestroy this card. If you do, leave the card you played in fromt\nof you for the rest of the game and it has: "Ongoing: You may\nplay this card once during each of your turns.\n(At the end of the game, destroy it.)"'
	image = "fe/images/cards/Firestorm Matrix.jpg"


	
	def play_action(self,player):
		drawn = player.reveal_card()
		player.played.play(drawn.pop_self())
		if drawn.cost <= 5:
			instruction_text = "Would you like to destory the Firestorm Matrix and make this card ongoing?"
			if effects.ok_or_no(instruction_text,player,drawn,hint = ai_hint.IFGOOD):
				self.destroy(player)
				player.ongoing.contents.append(drawn.pop_self())
				#Here comes the scary stuff

				def firestorm_special_action_click(player,actual_self = drawn):
					print("SPECIAL ACTION CLICK",actual_self.name,flush=True)
					if actual_self.action in player.played.special_options:
						player.played.special_options.remove(actual_self.action)
						backup_play_action = actual_self.play_action
						actual_self.play_action = actual_self.original_play_action
						player.played.play(actual_self)
						player.played.contents.remove(actual_self)
						actual_self.play_action = backup_play_action

				def replace_play_action(player,actual_self = drawn):
					print("REPLACE PLAY ACTION",actual_self.name,flush=True)
					actual_self.action = actions.special_action(f"Firestorm-{actual_self.name}",actual_self.firestorm_special_action_click)
					player.played.special_options.append(actual_self.action)
					return 0
				drawn.original_play_action = drawn.play_action
				drawn.firestorm_special_action_click = firestorm_special_action_click
				drawn.play_action = replace_play_action
		return 0

#DOne
class firestorm(card_frame.card):
	name = "Firestorm"
	vp = 2
	cost = 6
	ctype = cardtype.HERO
	text = 'Put the top card of your deck on your Super-Villain.\nThis card has the game text of each card on you\nSuper-Villain this turn.\n(At the end of the game, destroy those cards.)'
	image = "fe/images/cards/Firestorm.jpg"

	def play_action(self,player):
		drawn = player.reveal_card()
		player.over_superhero.append(drawn.pop_self())
		#Should i remove the owner?
		total = 0
		for c in player.over_superhero:
			total += c.play_action(player)
		return total




####LOCATIONS

class belle_reve(card_frame.card):
	name = "Belle Reve"
	vp = 1
	cost = 5
	ctype = cardtype.LOCATION
	text = "Ongoing: +1 Power for each Villain you play."
	image = "fe/images/cards/Belle Reve.jpg"
	ongoing = True

	def location_mod(self,card,player):
		#there is a risk that the card is removed from ongoing from an ealier mod
		if card.ctype_eq(cardtype.VILLAIN) and self.location_mod in player.played.card_mods:
			return 1
		return 0
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		player.played.card_mods.append(self.location_mod)
		return 0

class blackgate_prison(card_frame.card):
	name = "Blackgate Prison"
	vp = 1
	cost = 4
	ctype = cardtype.LOCATION
	text = "Ongoing: Once during each of your turns, reveal the top\ncard of your deck.  If it's a Vulnerability or\nWeakness, destroy it and gain 1 VP."
	image = "fe/images/cards/Blackgate Prison.jpg"
	ongoing = True
	action = None

	def special_action_click(self,player):
		revealed = player.reveal_card()
		effects.reveal(f"This was on top of {player.persona.name}'s deck",player,[revealed])
		if revealed.name == "Vulnerability" or revealed.name == "Weakness":
			revealed.destroy(player)
			player.gain_vp(1)
		player.played.special_options.remove(self.action)
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		#player.played.card_mods.append(self.location_mod)
		self.action = actions.special_action("Blackgate\n  Prison",self.special_action_click)
		player.played.special_options.append(self.action)
		return 0

class central_city(card_frame.card):
	name = "Central City"
	vp = 1
	cost = 5
	ctype = cardtype.LOCATION
	text = "Ongoing: +1 Power for each non-Kick Super Power you play."
	image = "fe/images/cards/Central City.jpg"
	ongoing = True

	def location_mod(self,card,player):
		#there is a risk that the card is removed from ongoing from an ealier mod
		if self.location_mod in player.played.card_mods and card.ctype_eq(cardtype.SUPERPOWER) and card.name != "Kick":
			return 1
		return 0
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		player.played.card_mods.append(self.location_mod)
		return 0

class earth_3(card_frame.card):
	name = "Earth-3"
	vp = 1
	cost = 6
	ctype = cardtype.LOCATION
	text = "Ongoing: Once during each of your turns, reveal the top\ncard of your deck.  If it's a Punch or\nWeakness, destroy it and gain 1 VP."
	image = "fe/images/cards/Earth 3.jpg"
	ongoing = True
	action = None

	def special_action_click(self,player):
		revealed = player.reveal_card()
		effects.reveal(f"This was on top of {player.persona.name}'s deck",player,[revealed])
		if revealed.name == "Punch":
			revealed.destroy(player)
			player.gain_vp(1)
		player.played.special_options.remove(self.action)
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		#player.played.card_mods.append(self.location_mod)
		self.action = actions.special_action("Earth-3",self.special_action_click)
		player.played.special_options.append(self.action)
		return 0

class happy_harbor(card_frame.card):
	name = "Happy Harbor"
	vp = 1
	cost = 5
	ctype = cardtype.LOCATION
	text = "Ongoing: +1 Power for each Hero you play."
	image = "fe/images/cards/Happy Harbor.jpg"
	ongoing = True

	def location_mod(self,card,player):
		#there is a risk that the card is removed from ongoing from an ealier mod
		if self.location_mod in player.played.card_mods and card.ctype_eq(cardtype.HERO):
			return 1
		return 0
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		player.played.card_mods.append(self.location_mod)
		return 0

class star_labs(card_frame.card):
	name = "S.T.A.R. Labs"
	vp = 1
	cost = 5
	ctype = cardtype.LOCATION
	text = "Ongoing: +1 Power for each Equipment you play."
	image = "fe/images/cards/Star Labs.jpg"
	ongoing = True

	def location_mod(self,card,player):
		#there is a risk that the card is removed from ongoing from an ealier mod
		if self.location_mod in player.played.card_mods and card.ctype_eq(cardtype.EQUIPMENT):
			return 1
		return 0
	
	
	def play_action(self,player):
		if self not in player.ongoing.contents:
			player.ongoing.add(self.pop_self())
		player.played.card_mods.append(self.location_mod)
		return 0