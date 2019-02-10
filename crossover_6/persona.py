from constants import cardtype
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from frames import actions
import random
from constants import owners
from constants import trigger

def get_personas():
	return []


class batwoman(persona_frame.persona):
	name = "Batwoman"
	text = "You may pay 1 less to buy cards in the Line-Up with the same card type\nas rotated cards you control."
	image = "crossover_6/images/personas/Batwoman MC.jpg"

	def ai_overvalue(self,card):
		match = False
		for c in player.ongoing.contents:
			if c.rotation != 0:
				rotated_types = rotated_types.union(set(c.get_ctype()))
		for c in player.played.contents:
			if c.rotation != 0:
				rotated_types = rotated_types.union(set(c.get_ctype()))
		#There is a match between the rotated types in play, and the current card
		if len(rotated_types.intersection(set(card.get_ctype()))) >= 1:
			return persona_frame.overvalue()
		return 0

	def trigger(self,ttype,data,player,active,immediate):
		if globe.DEBUG:
			print("test",self.name,flush=True)
		if trigger.test(immediate,\
						trigger.PRICE, \
						self.trigger, \
						player,ttype,active) \
				and data[1].owner_type == owners.LINEUP:
			if globe.DEBUG:
				print("active",self.name,flush=True)
			rotated_types = set()
			
			match = False
			for c in player.ongoing.contents:
				if c.rotation != 0:
					rotated_types = rotated_types.union(set(c.get_ctype()))
			for c in player.played.contents:
				if c.rotation != 0:
					rotated_types = rotated_types.union(set(c.get_ctype()))
			#There is a match between the rotated types in play, and the current card
			if len(rotated_types.intersection(set(data[1].get_ctype()))) >= 1:
				return data[0] - 1

	def ready(self):
		self.player.triggers.append(self.trigger)


class black_canary(persona_frame.persona):
	name = "Black Canary"
	text = "Once during each of your turns, if you control two or more different\nSuper Powers, rotate a card you control 90D clockwise.\nEach time a card you control rotates upright, you may put a card\nfrom your discard pile on top of your deck."
	image = "crossover_6/images/personas/Black Canary BOP MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.SUPERPOWER):
			return persona_frame.overvalue()
		return 0

	def special_action_click(self,player):
		assemble = []
		assemble.extend(player.ongoing.contents)
		assemble.extend(player.played.contents)
		super_count = 0
		for c in assemble:
			if c.ctype_eq(cardtype.SUPERPOWER):
				super_count += 1
		if super_count >= 2:
			instruction_text = "Rotate a card you control 90 Degrees"
			result = effects.may_choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
			if result != None:
				self.player.played.special_options.remove(self.action)
				result.rotate(player)
				return True
		return False

	def trigger(self,ttype,data,player,active,immediate):
		if globe.DEBUG:
			print("test",self.name,flush=True)
		if trigger.test(not immediate,\
						trigger.ROTATE, \
						self.trigger, \
						player,ttype,active)\
				and data[1]:
			if globe.DEBUG:
				print("active",self.name,flush=True)
			if len(player.discard.contents):
				result = effects.may_choose_one_of("You may put a card from your\ndiscard on top of your deck",player,player.discard.contents,ai_hint.BEST)			
				if result !=  None:
					result.pop_self()
					player.deck.contents.append(result)

	def ready(self):
		self.player.triggers.append()
		if self.active:
			self.action = actions.special_action("Black Canary",self.special_action_click)
			self.player.played.special_options.append(self.action)

	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)
		return False

class catwoman(persona_frame.persona):
	name = "Cat Woman"
	text = "Once during each of your turns, if you control four or more rotated\ncards, gain the top card of the main deck.\nEach time you play a villain, you may rotate an upright card you\ncontrol 90Degreen clockwise"
	image = "crossover_6/images/personas/Catwoman MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.VILLAIN):
			return persona_frame.overvalue()
		return 0

	def special_action_click(self,player):
		assemble = []
		assemble.extend(player.ongoing.contents)
		assemble.extend(player.played.contents)
		rotate_count = 0
		for c in assemble:
			if c.rotation != 0:
				rotate_count += 1
		if rotate_count >= 4:
			top_card = globe.boss.main_deck.reveal()
			player.gain(top_card)
			self.player.played.special_options.remove(self.action)
			return True
		return False

	def trigger(self,ttype,data,player,active,immediate):
		if globe.DEBUG:
			print("test",self.name,flush=True)
		if trigger.test(not immediate,\
						trigger.PLAY, \
						self.trigger, \
						player,ttype,active)\
				and data[0].ctype_eq(cardtype.VILLAIN):
			if globe.DEBUG:
				print("active",self.name,flush=True)
			assemble = []
			for c in player.ongoing.contents:
				if c.rotation == 0:
					assemble.append(c)
			for c in player.played.contents:
				if c.rotation == 0:
					assemble.append(c)
			if len(assemble) > 0:
				result = effects.may_choose_one_of("You may rotate an upright card you control",player,assemble,ai_hint.BEST)
				if result != None:
					result.rotate(player)

	def ready(self):
		self.player.triggers.append()
		if self.active:
			self.action = actions.special_action("Catwoman",self.special_action_click)
			self.player.played.special_options.append(self.action)


	#If there is more than a 50% chance of getting a card that does anything,
	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)
		return False

class huntress(persona_frame.persona):
	name = "Huntress"
	text = "Each time one or more players avoid an Attack you play, you may rotate\na card you control 90 Degrees clockwise\nEach time you avoid an Attack, you may rotate a card you control 90D clockwise."
	image = "crossover_6/images/personas/Huntress MC.jpg"

	def ai_overvalue(self,card):
		if card.attack or card.defence:
			return persona_frame.overvalue()
		return 0

	def triggerAV(self,ttype,data,player,active,immediate):
		if trigger.test(not immediate,\
						trigger.AVOIDED_ATTACK, \
						self.triggerAV, \
						player,ttype,active):
			assemble = []
			assemble.extend(player.ongoing.contents)
			assemble.extend(player.played.contents)
			if len(assemble) > 0:
				instruction_text = "You may rotate a card you control"
				result = effects.may_choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
				if result != None:
					result.rotate()
			
			

	def triggerReset(self,ttype,data,player,active,immediate):
		if trigger.test(immediate,\
						trigger.PLAY, \
						self.triggerReset, \
						player,ttype):
			self.same_attack = False

	#FA = Failed to Avoid
	def triggerFA(self,ttype,data,player,active,immediate):
		if trigger.test(not immediate,\
						trigger.MY_ATTACK_AVOIDED, \
						self.triggerFA, \
						player,ttype,active) \
				and self.same_attack == False:
			if globe.DEBUG:
				print("test",self.name,flush=True)
			assemble = []
			assemble.extend(player.ongoing.contents)
			assemble.extend(player.played.contents)
			if len(assemble) > 0:
				instruction_text = "You may rotate a card you control"
				result = effects.may_choose_one_of(instruction_text,player,assemble,ai_hint.BEST)
				if result != None:
					result.rotate()

	def reset(self):
		self.player.triggers.append(self.triggerAV)
		self.player.triggers.append(self.triggerFA)
		self.player.triggers.append(self.triggerReset)

class katana(persona_frame.persona):
	name = "Katana"
	text = "Once during each of your turns, if you control two or more\nEquipment, you may destroy a Starter in your hand or rotate a card\nyou control 90D clockwise."
	image = "crossover_6/images/personas/Katana MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.EQUIPMENT):
			return persona_frame.overvalue()
		return 0

	def special_action_click(self,player):
		assemble = []
		assemble.extend(player.ongoing.contents)
		assemble.extend(player.played.contents)
		super_count = 0
		for c in assemble:
			if c.ctype_eq(cardtype.EQUIPMENT):
				super_count += 1
		if super_count >= 2:
			temp_assemble = []
			for c in player.hand.contents:
				if c.ctype_eq(cardtype.STARTER):
					temp_assemble.append(c)
			if len(temp_assemble) > 0:
				result = effects.may_choose_one_of("Would you like to destroy a starter in your hand?",player,temp_assemble,ai_hint.WORST)
				if result != None:
					self.player.played.special_options.remove(self.action)
					result.destroy(player)
					return True
			#If we are here, try the seccond option
			result = effects.may_choose_one_of("you may rotate a card you control",player,assemble,ai_hint.BEST)
			if result != None:
				self.player.played.special_options.remove(self.action)
				result.rotate(player)
				return True
		return False

	def ready(self):
		if self.active:
			self.action = actions.special_action("Katana",self.special_action_click)
			self.player.played.special_options.append(self.action)

	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)
		return False

class oracle(persona_frame.persona):
	name = "Oracle"
	text = "Once during each of your turns, if you control two or more\nHeros, draw a card and rotate a card you control 90D clockwise."
	image = "crossover_6/images/personas/Oracle MC.jpg"
	action = None

	def ai_overvalue(self,card):
		if card.ctype_eq(cardtype.HERO):
			return persona_frame.overvalue()
		return 0

	def special_action_click(self,player):
		assemble = []
		assemble.extend(player.ongoing.contents)
		assemble.extend(player.played.contents)
		super_count = 0
		for c in assemble:
			if c.ctype_eq(cardtype.HERO):
				super_count += 1
		if super_count >= 2:
			player.draw_card()
			result = effects.choose_one_of("Rotate a card you control",player,assemble,ai_hint.BEST)
			self.player.played.special_options.remove(self.action)
			result.rotate()
			return True
		return False

	def ready(self):
		if self.active:
			self.action = actions.special_action("Oracle",self.special_action_click)
			self.player.played.special_options.append(self.action)

	def ai_is_now_a_good_time(self):
		if self.action in self.player.played.special_options:
			return self.special_action_click(self.player)
		return False
