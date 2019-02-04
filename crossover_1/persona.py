from constants import cardtype
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from frames import actions

def get_personas():
	#return [auquaman(),batman(),the_flash()]
	return [alan_scott(),doctor_fate(),jay_garrick()]
	#return [alan_scott(),doctor_fate(),jay_garrick(),mister_terricic(),power_girl(),stargirl(),wildcat()]


class alan_scott(persona_frame.persona):
	name = "Alan Scott"
	text = "Each time you play a different Super Power during your\nturn, reveal the top card of your deck. If the revealed card\ncosts 0, draw it."
	image = "crossover_1/images/personas/Alan Scott MC.jpg"

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.SUPERPOWER):
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype_eq(cardtype.SUPERPOWER):
			already_played = False
			for c in self.player.played.played_this_turn:
				if c != card and card.name == c.name:
					already_played = True
			if not already_played:
				top_card = player.reveal_card(public = True)
				if top_card.cost == 0:
					player.draw_card()
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)


class doctor_fate(persona_frame.persona):
	name = "Doctor Fate"
	text = "When you play two cards with consecutive costs during your turn,\n+1 Power.\nWhen you play three cards with consecutive costs during your turn,\ndraw a card."
	image = "crossover_1/images/personas/Doctor Fate MC.jpg"
	cards_registered = []

	def get_costcount(self):
		distribution = {}
		for i in range(25):
			distribution[i] = 1
		assemble = []
		assemble.extend(self.player.deck.contents)
		assemble.extend(self.player.discard.contents)
		for c in assemble:
			distribution[c.cost] += 1
		return distribution

	def ai_overvalue(self,card):
		card_costs = self.get_costcount()
		all_relevant = sum(list(card_types.values()))
		return 0.25/(card_costs[card.cost]/all_relevant) - 1
		#print("MAKE SURE NONE OF THESE ARE 0",card.ctype,all_relevant,flush=True)
		#if card.ctype in card_types:
		#	return 0.25/(card_types[card.ctype]/all_relevant) - 1
		#return 0

	#This is a complicated ability.  
	#I kind of disagree how its being interpreted on forms, but i am implimenting it thqt way anyways
	#There should be decition mkainging, like what pairs, but i may just base that on order of cards played
	#Idealy, if finds the optimum, but that is hard.  nealy impossible with drawing
	def mod(self,card,player):
		self.cards_registered.append(card)
		card.df_power = False
		card.df_draw = False
		#initialize all cards that have been played, if they have not been inititalized yet
		for c in self.player.played.played_this_turn:
			if not hasattr(c, 'df_power'):
				self.cards_registered.append(c)
				c.df_power = False
				c.df_draw = False
		for c in self.player.played.played_this_turn:
			#starts by finding 2 consecutive
			if c != card and abs(c.cost-card.cost) == 1:
				#power portion
				if c.df_power == False and card.df_power == False:
					c.df_power = True
					card.df_power = True
					player.played.plus_power(1)
					print(f"Doctor Fate got power because of a {card.name} and {c.name}")
				#draw portion
				if c.df_draw == False and card.df_draw == False:
					#find third match
					for c2 in self.player.played.played_this_turn:
						if c2 != c and c2 != card and c2.df_draw == False and (abs(c.cost-c2.cost) == 1 or abs(c2.cost-card.cost) == 1) and c.df_draw == False and card.df_draw == False:
							card.df_draw = True
							c.df_draw = True
							c2.df_draw = True
							player.draw_card()
							print(f"Doctor Fate Drew because of a {card.name}, {c.name}, and {c2.name}")

		return 0


	def ready(self):
		self.cards_registered = []
		if self.active:
			self.player.played.card_mods.append(self.mod)

	#resets all cards that have been touched
	def reset(self):
		for c in self.cards_registered:
			c.df_power = False
			c.df_draw = False


class jay_garrick(persona_frame.persona):
	name = "Jay Garrick"
	text = "When a card tells you to draw one or more cards, before\ndrawing, reveal the top card of your deck and you may\ndiscard it."
	image = "crossover_1/images/personas/Jay Garrick MC.jpg"
	accounted_for = False

	def ai_overvalue(self,card):
		if card.text.lower().count('draw') > 0:
			return persona_frame.overvalue()
		return 0

	def draw_power(self):
		if self.active:
			revealed = self.player.reveal_card(public = True)
			if effects.ok_or_no(f"Would you like to discard the {revealed.name}?",self.player,revealed,ai_hint.IFBAD):
				self.player.discard_a_card(revealed)
		return


class mister_terricic(persona_frame.persona):
	name = "Mister Terrific"
	text = "Once during each of your turns, you may discard a Punch card.\nIf you do, reveal the top three cards of your deck, draw one\nEquipment revealed this way, and put the rest back in any order."
	image = "crossover_1/images/personas/Mister Terrific MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.EQUIPMENT):
			#Really need equipment
			return persona_frame.overvalue()*2
		return 0

	def special_action_click(self,player):
		#We must ensure that we are doing this on our turn
		if player.pid == globe.boss.whose_turn:
			for c in self.player.hand.contents:
				if c.name == "Punch" and self.action in self.player.played.special_options:
					self.player.discard_a_card(c)

					assemble = []
					for i in range(3):
						assemble.append(player.reveal_card(public = False))
						player.deck.contents.pop()

					equipment_assemble = []
					for c in assemble:
						if c.ctype_eq(cardtype.EQUIPMENT):
							equipment_assemble.append(c)
					effects.reveal(f"These were the top 3 cards on {player.persona.name}'s deck",player,assemble)
					if len(equipment_assemble) > 0:
						result = effects.choose_one_of("Choose one of these to draw.",player,assemble,ai_hint.BEST)
						#must be there to be drawn
						player.deck.contents.append(result)
						player.draw_card(from_card = False)
						assemble.remove(result)
					total_times = len(assemble)
					while len(assemble) > 0:
						result = effects.choose_one_of(f"Place card back on top of your deck ({total_times - len(assemble) + 1}/{total_times})?",player,assemble,ai_hint.WORST)
						assemble.remove(result)
						player.deck.contents.append(result)

					self.player.played.special_options.remove(self.action)
					return True
		return False


	def ready(self):
		if self.active:
			self.action = actions.special_action("Mister Terrific",self.special_action_click)
			self.player.played.special_options.append(self.action)

	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		total_left = 0
		for c in self.player.deck.contents:
			if c.ctype_eq(cardtype.EQUIPMENT):
				total_left += 1
		if total_left/(len(self.player.deck.contents)+1) > 0.2:
			if self.action in self.player.played.special_options:
				return self.special_action_click(self.player)
			#return self.any_time()
		return False


class power_girl(persona_frame.persona):
	name = "Power Girl"
	text = "Each time you play a different Super Power during your\nturn, put a Punch from your discard pile into your hand."
	image = "crossover_1/images/personas/Power Girl MC.jpg"

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.SUPERPOWER):
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.ctype_eq(cardtype.SUPERPOWER):
			already_played = False
			for c in self.player.played.played_this_turn:
				if c != card and card.name == c.name:
					already_played = True
			if not already_played:
				for c in player.discard.contents:
					if c.name == "Punch":
						c.pop_self()
						player.hand.contents.append(c)
						return 0
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)


class stargirl(persona_frame.persona):
	name = "Stargirl"
	text = "When you play a Defense card during your turn or avoid\nan Attack, you may draw a card and then discard a card."
	image = "crossover_1/images/personas/Stargirl MC.jpg"
	
	def ai_overvalue(self,card):
		if card.defence:
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.defence:
			player.draw_card(from_card = False)
			result = effects.choose_one_of("Discard a card",player,player.hand.contents,ai_hint.WORST)
			player.discard_a_card(result)
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

	def avoided_attack(self):
		self.player.draw_card(from_card = False)
		result = effects.choose_one_of("Discard a card",self.player,self.player.hand.contents,ai_hint.WORST)
		self.player.discard_a_card(result)
		return


class wildcat(persona_frame.persona):
	name = "Wildcat"
	text = "The first time you play a Punch dueing each of your turns:\n-If you have played a Hero this turn, draw a card.\n-If you have played a Villain this turn, draw a card."
	image = "crossover_1/images/personas/Wildcat MC.jpg"

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.HERO) or card.ctype_eq(cardtype.VILLAIN):
			return persona_frame.overvalue()
		return 0

	def mod(self,card,player):
		if card.name == "Punch" and self.mod in self.player.played.card_mods:
			hero_played = False
			villain_played = False
			for c in self.player.played.played_this_turn:
				if c.ctype_eq(cardtype.HERO):
					hero_played = True
				if c.ctype_eq(cardtype.VILLAIN):
					villain_played = True
			if hero_played:
				player.draw_card(from_card = False)
			if villain_played:
				player.draw_card(from_card = False)

			self.player.played.card_mods.remove(self.mod)
		return 0


	def ready(self):
		if self.active:
			self.player.played.card_mods.append(self.mod)

