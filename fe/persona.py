import cardtype
import effects
import ai_hint
import globe
import persona_frame
import actions
import owners



def get_personas():
	return []



class bane(persona_frame.persona):
	name = "Bane"
	text = "If the first card you play during each of your turns has a cost 1\nor greater, you may destroy it. If you do, +2 Power."
	image = "fe/images/personas/Bane MC.jpg"
	action = None

	def special_action_click(self,player):
		self.player.played.played_this_turn[0].destroy(player)
		self.player.played.plus_power(2)
		self.player.played.special_options.remove(self.action)
		return True

	def mod(self,card,player):
		if len(player.played.played_this_turn) > 0 and player.played.played_this_turn[0].cost >= 1:
			self.action = actions.special_action("Bane",self.special_action_click)
			self.player.played.special_options.append(self.action)
			self.player.played.card_mods.remove(self.mod)
		return 0

	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

	def ai_is_now_a_good_time(self):
		return False


class bizarro(persona_frame.persona):
	name = "Bizarro"
	text = "When you destroy a card, gain a Weakness.\nDuring your turn, you may put two Weakness cards from your\ndiscard pile on top of the Weakness stack.  If you do, draw a card."
	image = "fe/images/personas/Bizarro MC.jpg"
	action = None

	def special_action_click(self,player):
		to_remove = []
		for c in self.player.discard.contents:
			if c.ctype == cardtype.WEAKNESS:
				to_remove.append(c)
				if len(to_remove) == 2:
					for w in to_remove:
						w.pop_self()
						w.set_owner(owners.WEAKNESS)
						globe.boss.weakness_stack.add(w)
					self.player.draw_card()
					self.player.played.special_options.remove(self.action)
					return True
		return False

	def ready(self):
		if self.active:
			self.action = actions.special_action("Bizarro",self.special_action_click)
			self.player.played.special_options.append(self.action)

	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)

	def destory_power(self):
		if self.active:
			self.player.gain_a_weakness()
		return


class black_adam(persona_frame.persona):
	name = "Black Adam"
	text = "The first time you play a super power during each of your turns, you may destroy it.  If you do, draw a card and gain 1 VP."
	image = "fe/images/personas/Black Adam MC.jpg"

	def mod(self,card,player):
		if card.ctype == SUPERPOWER: # and len(player.played.played_this_turn) == 0:
			instruction_text = "Would you like to destory it? If you do, draw a card and gain 1 VP."
			result = effects.ok_or_no(instruction_text,player,card,ai_hint.IFBAD)
			if result:
				card.destory(player)
				player.draw_card()
				player.vp += 1
			self.player.played.card_mods.remove(self.mod)
		return 0

	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

class black_manta(persona_frame.persona):
	name = "Black Manta"
	text = "You may put any cards you buy or gain from the lineup on the bottom of your deck."
	image = "base/images/personas/Black Manta MC.jpg"

	def aquaman_redirect(self,player,card):
		if globe.boss.whose_turn == self.player.pid and effects.ok_or_no(f"Would you like to put {card.name} on the bottom of your deck?",player,card,ai_hint.ALWAYS):
			return [True,player.deck,"bottom"]
		return (False,None)

	def ready(self):
		if self.active:
			self.player.gain_redirect.append(self.aquaman_redirect)

class deathstroke(persona_frame.persona):
	name = "Deathstroke"
	text = "+1 Power for each card you destroy during your turn."
	image = "fe/images/personas/Deathstroke MC.jpg"


	def destory_power(self):
		if self.active and globe.boss.whose_turn == self.player.pid:
			self.player.played.plus_power(1)
		return



"""
class black_canary(persona_frame.persona):
	name = "Black Canary"
	text = "+1 Power for each different Villain you play during your turn."
	image = "hu/images/personas/Black Canary HU MC.jpg"
	
	def ai_overvalue(self,card):
		if card.ctype == cardtype.VILLAIN:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.SUPERPOWER:
			already_played = False
			for c in self.player.played.played_this_turn:
				if card.name == c.name:
					already_played = True
			if not already_played:
				return 1
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)


class booster_gold(persona_frame.persona):
	name = "Booster Gold"
	text = "+1 Power for each Defense card you play during your turn.  When you avoid an attack, draw a card."
	image = "hu/images/personas/Booster Gold MC.jpg"
	
	def ai_overvalue(self,card):
		if card.defence:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.defence:
			return 1
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

	def avoided_attack(self):
		self.player.draw_card()
		return

class hawkman(persona_frame.persona):
	name = "Hawkman"
	text = "+1 Power for each Hero you play during your turn."
	image = "hu/images/personas/Hawkman MC.jpg"

	def ai_overvalue(self,card):
		if card.ctype == cardtype.HERO:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.HERO:
			return 1
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

class nightwing(persona_frame.persona):
	name = "Nightwing"
	text = "The first time you play an Equipment during your turn, +1 Power.\n The second time you play an Equipment during your turn, draw a card."
	image = "hu/images/personas/Nightwing MC.jpg"

	def ai_overvalue(self,card):
		if card.ctype == cardtype.EQUIPMENT:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.EQUIPMENT:
			number_played = 0
			for c in self.player.played.played_this_turn:
				if c.ctype == cardtype.EQUIPMENT:
					number_played += 1
			if number_played == 0:
				return 1
			elif number_played == 1:
				self.player.draw_card()
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)



class red_tornado(persona_frame.persona):
	name = "Red Tornado"
	text = "Once during each of your turns, if there are four or more different card types in your discard pile, +2 Power."
	image = "hu/images/personas/Red Tornado MC.jpg"
	accounted_for = False
	action = None

	def get_typecount(self):
		return {cardtype.HERO:self.player.deck.get_count(cardtype.HERO) + self.player.discard.get_count(cardtype.HERO) + 1, \
						cardtype.VILLAIN:self.player.deck.get_count(cardtype.VILLAIN) + self.player.discard.get_count(cardtype.VILLAIN) + 1, \
						cardtype.SUPERPOWER:self.player.deck.get_count(cardtype.SUPERPOWER) + self.player.discard.get_count(cardtype.SUPERPOWER) + 1, \
						cardtype.EQUIPMENT:self.player.deck.get_count(cardtype.EQUIPMENT) + self.player.discard.get_count(cardtype.EQUIPMENT) + 1}

	def ai_overvalue(self,card):
		card_types = self.get_typecount()
		all_relevant = sum(list(card_types.values()))
		print("MAKE SURE NONE OF THESE ARE 0",card.ctype,all_relevant,flush=True)
		if card.ctype in card_types:
			return 0.25/(card_types[card.ctype]/all_relevant) - 1
		return 0


	def special_action_click(self,player):
		#We must ensure that we are doing this on our turn
		if player.pid == globe.boss.whose_turn:
			card_types = set()
			for c in player.discard.contents:
				card_types.add(c.ctype)
			if len(card_types) >= 4:
				player.played.plus_power(2)
				player.played.special_options.remove(self.action)
				return True
		return False


	def ready(self):
		if self.active:
			self.action = actions.special_action("Red Tornado",self.special_action_click)
			self.player.played.special_options.append(self.action)


	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)


class shazam(persona_frame.persona):
	name = "Shazam"
	text = "You may pay 4 Power, If you do, gain the top card of the main deck.  You may put it on top of your deck or into your discard pile."
	image = "hu/images/personas/Shazam MC.jpg"
	action = None


	def special_action_click(self,player):
		#We must ensure that we are doing this on our turn
		if player.pid == globe.boss.whose_turn:
			if self.player.played.power >= 4:
				self.player.played.power -= 4
				card = globe.boss.main_deck.contents[-1]
				instruction_text = f"Would you like to put {card.name} on top of your deck?"
				result = effects.ok_or_no(instruction_text,self.player,card,ai_hint.ALWAYS)
				card = globe.boss.main_deck.contents.pop()
				card.set_owner(self.player)
				if result:
					self.player.deck.add(card)
				else:
					self.player.gain(card)
				return True
		return False


	def ready(self):
		if self.active:
			self.action = actions.special_action("Shazam",self.special_action_click)
			self.player.played.special_options.append(self.action)

	#IDK
	def ai_is_now_a_good_time(self):

		return False



class starfire(persona_frame.persona):
	name = "Starfire"
	text = "Once during each of your turns, if there are no Super Powers in the Line-up, draw a card."
	image = "hu/images/personas/Starfire HU MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype == cardtype.SUPERPOWER:
			return persona_frame.overvalue()
		return 0


	def special_action_click(self,player):
		#We must ensure that we are doing this on our turn
		if player.pid == globe.boss.whose_turn:
			if globe.boss.lineup.get_count(cardtype.SUPERPOWER) == 0:
				self.player.draw_card()
				player.played.special_options.remove(self.action)
				return True
		return False


	def ready(self):
		if self.active:
			self.action = actions.special_action("Starfire",self.special_action_click)
			self.player.played.special_options.append(self.action)


	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)

"""