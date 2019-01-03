import cardtype
import effects
import ai_hint

def get_personas():
	return [auquaman,batman,cyborg,the_flash,green_lantern,hawkman,superman,wonder_woman]

class persona:
	player = None
	name = ""
	text = ""

	def __init__(self,player):
		self.player = player

	def set_modifiers(self):
		return


	def gain_power(self,card):
		return

	def draw_power(self):
		return

	def reset(self):
		return

class auquaman(persona):
	name = "Auqaman"
	text = "You may put any cards with cost 5 or less you buy or gain during your turn on top of your deck."

	def aquaman_redirect(self,player,card):
		if card.cost <= 5 and effects.ok_or_no(f"Would you like to put {card.name} on top of your deck?",player,card,ai_hint.ALWAYS):
			return (True,player.deck)
		return (False,None)

	def reset(self):
		self.player.gain_redirect.append(self.aquaman_redirect)

class batman(persona):
	name = "Batman"
	text = "+1 Power for each Equipment you play during your turn."

	def mod(self,card,player):
		if card.ctype == cardtype.EQUIPMENT:
			return 1
		return 0

	def reset(self):
		self.player.played.card_mods.append(self.mod)

class cyborg(persona):
	name = "Cyborg"
	text = "+1 power for first super power played, and draw a card for the first equipment played"

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


	def reset(self):
		self.player.played.card_mods.append(self.mod)

class the_flash(persona):
	name = "The Flash"
	text = "You go first.  The first time a card tells you to draw one or more cards during each of your turns, draw an additional card."
	accounted_for = False

	def draw_power(self):
		if not self.accounted_for:
			self.accounted_for = True
			self.player.draw_card()
		return


class green_lantern(persona):
	name = "Green Lantern"
	text = "If you play three or more cards with different names and cost 1 or more during your turn, +3 Power."
	accounted_for = False

	def mod(self,card,player):
		if not self.accounted_for:
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
				self.accounted_for = True
				return 3
		return 0

	def reset(self):
		self.accounted_for = False
		self.player.played.card_mods.append(self.mod)

class hawkman(persona):
	name = "Hawkman"
	text = "+1 Power for each Hero you play during your turn."

	def mod(self,card,player):
		if card.ctype == cardtype.HERO:
			return 1
		return 0


	def set_modifiers(self):
		self.player.played.card_mods.append(self.mod)
		return

class superman(persona):
	name = "Superman"
	text = "+1 Power for each different Super Power you play during your turn."

	def mod(self,card,player):
		if card.ctype == cardtype.SUPERPOWER:
			already_played = False
			for c in self.player.played.played_this_turn:
				if card.name == c.name:
					already_played = True
			if not already_played:
				return 1
		return 0


	def reset(self):
		self.player.played.card_mods.append(self.mod)
		return

class wonder_woman(persona):
	name = "Wonder Woman"
	text = "For each Villain you buy or gain during your turn, draw an extra card at the end of your turn."

#the reset is specifically timed for this to be possible
	def reset(self):
		for c in self.player.gained_this_turn:
			if c.ctype == cardtype.VILLAIN:
				self.player.draw_card()
