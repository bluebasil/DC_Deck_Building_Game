import cardtype
import effects
import ai_hint
import globe
import persona_frame



def get_personas():
	return [hawkman]

"""
#class auquaman(persona_frame.persona):
	name = "Aquaman"
	text = "You may put any cards with cost 5 or less you buy or gain during your turn on top of your deck."

	def aquaman_redirect(self,player,card):
		if globe.boss.whose_turn == self.player.pid and card.cost <= 5 and effects.ok_or_no(f"Would you like to put {card.name} on top of your deck?",player,card,ai_hint.ALWAYS):
			return (True,player.deck)
		return (False,None)

	def ready(self):
		if self.active:
			self.player.gain_redirect.append(self.aquaman_redirect)

#class batman(persona_frame.persona):
	name = "Batman"
	text = "+1 Power for each Equipment you play during your turn."

	def ai_overvalue(self,card):
		if card.ctype == cardtype.EQUIPMENT:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.EQUIPMENT:
			return 1
		return 0

	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

#class cyborg(persona_frame.persona):
	name = "Cyborg"
	text = "+1 power for first super power played, and draw a card for the first equipment played"

	def ai_overvalue(self,card):
		if card.ctype == cardtype.SUPERPOWER or card.ctype == cardtype.EQUIPMENT:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.SUPERPOWER:
			already_played = False
			for c in self.player.played.played_this_turn:
				if c.ctype == cardtype.SUPERPOWER:
					already_played = True
			if not already_played:
				return 1
		elif card.ctype == cardtype.EQUIPMENT:
			already_played = False
			for c in self.player.played.played_this_turn:
				if c.ctype == cardtype.EQUIPMENT:
					already_played = True
			if not already_played:
				
				self.player.draw_card()
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

#class the_flash(persona_frame.persona):
	name = "The Flash"
	text = "You go first.  The first time a card tells you to draw one or more cards during each of your turns, draw an additional card."
	accounted_for = False

	def ai_overvalue(self,card):
		if card.text.lower().count('draw') > 0:
			return persona_frame.overvalue()
		return 0

	def draw_power(self):
		if self.active and not self.accounted_for:
			self.accounted_for = True
			self.player.draw_card()
		return


#class green_lantern(persona_frame.persona):
	name = "Green Lantern"
	text = "If you play three or more cards with different names and cost 1 or more during your turn, +3 Power."
	#accounted_for = False

	def mod(self,card,player):
		#if not self.accounted_for:
		others = [card]
		for c in self.player.played.played_this_turn:
			unique = True
			if c.cost >= 1:
				for o in others:
					if c.name == o.name:
						unique = False
				if unique:
					others.append(c)
		if len(others) >= 3:
			#self.accounted_for = True
			if self.mod in self.player.played.card_mods:
				self.player.played.card_mods.remove(self.mod)
			return 3
		return 0

	def ready(self):
		if self.active:
			#self.accounted_for = False
			self.player.played.card_mods.append(self.mod)
"""


class batgirl(persona_frame.persona):
	name = "Batgirl"
	text = "Once during each of your turns, you may discard a Punch card.  If you do, draw a card."
	accounted_for = False


	def any_time(self):
		if not self.accounted_for:
			for c in self.player.hand.contents:
				if c.name == "Punch":
					self.player.discard.add(c.pop_self())
					self.player.draw_card()
					self.accounted_for = True
					return True
		return False

	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		total_left = 0
		for c in self.player.deck.contents:
			if c.cost > 0:
				total_left += 1
		if total_left/len(self.player.deck.contents) > 0.5:
			return self.any_time()
		return False

	def reset(self):
		self.accounted_for = False

class black_canary(persona_frame.persona):
	name = "Black Canary"
	text = "+1 Power for each different Villain you play during your turn."
	
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

	def ai_overvalue(self,card):
		if card.ctype == cardtype.EQUIPMENT:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype == cardtype.EQUIPMENT:
			number_played = 0:
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
	accounted_for = False

	def get_typecount(self):
		return {cardtype.HERO:self.player.deck.get_count(cardtype.HERO) + self.player.discard.get_count(cardtype.HERO) + 1, \
						cardtype.VILLAIN:self.player.deck.get_count(cardtype.VILLAIN) + self.player.discard.get_count(cardtype.VILLAIN) + 1, \
						cardtype.SUPERPOWER:self.player.deck.get_count(cardtype.SUPERPOWER) + self.player.discard.get_count(cardtype.SUPERPOWER) + 1, \
						cardtype.EQUIPMENT:self.player.deck.get_count(cardtype.EQUIPMENT) + self.player.discard.get_count(cardtype.EQUIPMENT) + 1}

	def ai_overvalue(self,card):
		card_types = self.get_typecount()
		all_relevant = sum(list(card_types.values()))
		if card.ctype in card_types:
			return 0.25/(card_types[card.ctype]/all_relevant) - 1
		return 0
	
	def any_time(self):
		card_types = set()
		if not self.accounted_for:
			for c in self.player.discard.contents:
				card_types.add(c.ctype)
			if len(s) >= 4:
				self.player.played.plus_power(2)
				self.accounted_for = True
				return True
		return False

	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		return self.any_time()

	def reset(self):
		self.accounted_for = False


class shazam(persona_frame.persona):
	name = "Shazam"
	text = "You may pay 4 Power, If you do, gain the top card of the main deck.  You may put it on top of your deck or into your discard pile."

	
	def any_time(self):
		if self.player.played.power >= 4:
			self.player.played.power -= 4
			instruction_text = "Would you like to put this card of top of your deck?"
			card = globe.boss.main_deck.pop()
			card.set_owner(self.player)
			result = effects.ok_or_no(instruction_text,self.player,ai_hint.ALWAYS)
			if result:
				self.player.deck.add(card)
			else:
				self.player.gain(card)
			return True
		return False

	#IDK
	def ai_is_now_a_good_time(self):

		return False



class starfire(persona_frame.persona):
	name = "Starfire"
	text = "Once during each of your turns, if there are no Super Powers in the Line-up, draw a card."
	accounted_for = False

	def ai_overvalue(self,card):
		if card.ctype == cardtype.SUPERPOWER:
			return persona_frame.overvalue()
		return 0

	def any_time(self):
		if not self.accounted_for:
			if globe.boss.lineup.get_count(cardtype.SUPERPOWER) == 0:
				self.player.draw_card()
				self.accounted_for = True
				return True

		return False

	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		return self.any_time()

	def reset(self):
		self.accounted_for = False



"""
class wonder_woman(persona_frame.persona):
	name = "Wonder Woman"
	text = "For each Villain you buy or gain during your turn, draw an extra card at the end of your turn."

	def ai_overvalue(self,card):
		if card.ctype == cardtype.VILLAIN:
			return persona_frame.overvalue()
		return 0

#the reset is specifically timed for this to be possible
	def reset(self):
		if self.active:
			for c in self.player.gained_this_turn:
				if c.ctype == cardtype.VILLAIN:
					self.player.draw_card()

class martian_manhunter(persona_frame.persona):
	name = "Martian Manhunter"
	text = "If you play two or more Villains during your turn, +3 Power.\nIf you play two or more Heros during your turn, +3 Power."

	def ai_overvalue(self,card):
		if card.ctype == cardtype.VILLAIN or card.ctype == cardtype.HERO:
			return persona_frame.overvalue()
		return 0

	def villain_mod(self,card,player):
		if card.ctype == cardtype.VILLAIN:
			#This card is 1
			villain_count = 1
			for c in self.player.played.played_this_turn:
				if c.ctype == cardtype.VILLAIN:
					villain_count += 1
			if villain_count == 2:
				if self.villain_mod in self.player.played.card_mods:
					self.player.played.card_mods.remove(self.villain_mod)
				return 3
		return 0


	def hero_mod(self,card,player):
		if card.ctype == cardtype.HERO:
			#This card is 1
			hero_count = 1
			for c in self.player.played.played_this_turn:
				if c.ctype == cardtype.HERO:
					hero_count += 1
			if hero_count == 2:
				if self.hero_mod in self.player.played.card_mods:
					self.player.played.card_mods.remove(self.hero_mod)
				return 3
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.villain_mod)
			self.player.played.card_mods.append(self.hero_mod)
"""