import cardtype
import effects
import ai_hint
import globe
import persona_frame

def get_personas():
	return [auquaman,batman,cyborg,the_flash,green_lantern,hawkman,superman,wonder_woman,martian_manhunter]


class auquaman(persona_frame.persona):
	name = "Aquaman"
	text = "You may put any cards with cost 5 or less you buy or gain during your turn on top of your deck."
	#image = "base/images/personas/Aquaman MC.jpg"

	def aquaman_redirect(self,player,card):
		if globe.boss.whose_turn == self.player.pid and card.cost <= 5 and effects.ok_or_no(f"Would you like to put {card.name} on top of your deck?",player,card,ai_hint.ALWAYS):
			return (True,player.deck)
		return (False,None)

	def ready(self):
		if self.active:
			self.player.gain_redirect.append(self.aquaman_redirect)

class batman(persona_frame.persona):
	name = "Batman"
	text = "+1 Power for each Equipment you play during your turn."
	#image = "base/images/personas/Aquaman MC.jpg"

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

class cyborg(persona_frame.persona):
	name = "Cyborg"
	text = "+1 power for first super power played, and draw a card for the first equipment played"
	#image = "base/images/personas/Aquaman MC.jpg"

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

class the_flash(persona_frame.persona):
	name = "The Flash"
	text = "You go first.  The first time a card tells you to draw one or more cards during each of your turns, draw an additional card."
	#image = "base/images/personas/Aquaman MC.jpg"
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

	def reset(self):
		self.accounted_for = False


class green_lantern(persona_frame.persona):
	name = "Green Lantern"
	text = "If you play three or more cards with different names and cost 1 or more during your turn, +3 Power."
	#image = "base/images/personas/Aquaman MC.jpg"
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

class hawkman(persona_frame.persona):
	name = "Hawkman"
	text = "+1 Power for each Hero you play during your turn."
	#image = "base/images/personas/Aquaman MC.jpg"

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

class superman(persona_frame.persona):
	name = "Superman"
	text = "+1 Power for each different Super Power you play during your turn."
	#image = "base/images/personas/Aquaman MC.jpg"
	
	def ai_overvalue(self,card):
		if card.ctype == cardtype.SUPERPOWER:
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

class wonder_woman(persona_frame.persona):
	name = "Wonder Woman"
	text = "For each Villain you buy or gain during your turn, draw an extra card at the end of your turn."
	#image = "base/images/personas/Aquaman MC.jpg"

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
	#image = "base/images/personas/Aquaman MC.jpg"

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