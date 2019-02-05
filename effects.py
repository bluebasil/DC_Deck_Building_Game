from constants import option
import globe
from constants import cardtype
from constants import ai_hint


def new_assemble(list):
	assemble = []
	for i in list:
		assemble.append(i)
	return assemble


def ensure_int(i):
	if not type(i) is int:
		print("ERR: not an integer")
		return False
	else:
		return True

#depreciated
def attack_all(card):
	total_hit = 0
	for p in globe.boss.players:
		if attack(p,card):
			total_hit += 1
	return total_hit

#Returns true if hit by attack
def attack(player,card,by_player = None,avoid_twise = False):
	if by_player != None:
		for t in by_player.triggers.copy():
			result = t("attacking",[player,card],by_player):
			#The attacking trigger will return true or false, but nested
			#So that it can be distinquished from other triggers
			#I should probbaly set up a uniform trigger responce
			if result != False:
				return result[0]

	assemble = []
	for c in player.hand.contents:
		if c.defence:
			assemble.append(c)
	for c in player.ongoing.contents:
		if c.defence:
			assemble.append(c)

	if len(assemble) > 0:
		result = player.controler.may_defend(assemble,card,by_player)
		if result[0] == option.OK:
			if not ensure_int(result[1]):
				return attack(player,card,by_player)
			elif result[1] < 0 or result[1] >= len(assemble):
				print("Err: invalid number")
				return attack(player,card,by_player)
			else:
				#Attack avoided
				assemble[result[1]].defend(attacker = by_player, defender = player)
				#avoid twise, like in crossover 2's deadshot
				if avoid_twise:
					return attack(player,card,by_player,avoid_twise = False)
				else:
					#If you avoid the attack but not twise when nessesary (crossover 2's deadshot)
					#do you get to trigger your avoided attack abilities?
					player.persona.avoided_attack(result[1])
					return False
		elif result[0] == option.NO:
			if by_player != None:
				by_player.persona.failed_to_avoid_power()
			return True
		else:
			print("Err: responce")
			return attack(player,card,by_player)
	else:
		if by_player != None:
			by_player.persona.failed_to_avoid_power()
		return True

def choose_a_player(instruction_text,player,includes_self = True,hint = ai_hint.WORST):
	assemble = []
	for i,p in enumerate(globe.boss.players):
		if p != player or includes_self:
			assemble.append(p.persona)

	result = player.controler.choose_a_player(instruction_text,player,assemble,hint)
	if globe.DEBUG:
		print("choose_a_player",result)
	if not ensure_int(result):
		return choose_a_player(instruction_text,player,includes_self)
	elif result < 0 or result >= len(assemble):
		print(f"ERR: invalid number. max:{len(assemble)-1}")
		return choose_a_player(instruction_text,player,includes_self)
	return assemble[result].player

def choose_one_of(instruction_text,player,cards,hint = ai_hint.WORST):
	result = player.controler.choose_one_of(instruction_text,player,cards,hint)
	if globe.DEBUG:
		print("choose_one_of",result)
	if not ensure_int(result[0]):
		return choose_one_of(instruction_text,player,cards)
	elif result[0] < 0 or result[0] >= len(cards):
		print(f"ERR: invalid number. max:{len(cards)-1}")
		return choose_one_of(instruction_text,player,cards)
	return cards[result[0]]

def may_choose_one_of(instruction_text,player,cards,hint = ai_hint.BEST):
	if len(cards) == 0:
		return None
	result = player.controler.may_choose_one_of(instruction_text,player,cards,hint)
	if globe.DEBUG:
		print("may_choose_one_of",result)
	if result[0] == option.NO:
		return None
	elif result[0] == option.OK:
		if not ensure_int(result[1]):
			return may_choose_one_of(instruction_text,player,cards,hint)
		elif result[1] < 0 or result[1] >= len(cards):
			print(f"ERR: invalid number. max:{len(cards)-1}")
			return may_choose_one_of(instruction_text,player,cards,hint)
		return cards[result[1]]
	else:
		print(f"ERR: invalid responce code")
		return may_choose_one_of(instruction_text,player,cards,hint)


def ok_or_no(instruction_text,player,card = None,hint = ai_hint.IFBAD):
	result = player.controler.ok_or_no(instruction_text,player,card,hint)
	if globe.DEBUG:
		print("ok_or_no",result)
	if result[0] == option.OK:
		return True
	elif result[0] == option.NO:
		return False
	else:
		print(f"ERR: invalid responce code")
		return ok_or_no(instruction_text,player,hint)

def reveal(reveal_text,player,cards):
	for p in globe.boss.players:
		p.controler.reveal(reveal_text,player,cards)

#True for even
def choose_even_or_odd(instruction_text,player):
	result = player.controler.choose_even_or_odd(instruction_text,player)
	if globe.DEBUG:
		print("choose_even_or_odd",result)
	if result[0] == option.EVEN:
		return True
	if result[0] == option.ODD:
		return False
	else:
		return choose_even_or_odd(instruction_text,player)


# (no/hand/disccard, if hand or discard: #)
def may_destroy_card_in_hand_or_discard(player):
	result = player.controler.may_destroy_card_in_hand_or_discard()
	if globe.DEBUG:
		print("may_destroy_card_in_hand_or_discard",result)
	if len(result) != 2:
		print("ERR: not 2 attributes")
		return may_destroy_card_in_hand_or_discard(player)
	if result[0] == option.NO:
		return (option.NO,)
	elif result[0] == option.HAND or result[0] == option.DISCARD:
		if not ensure_int(result[1]):
			return may_destroy_card_in_hand_or_discard(player)
		elif result[0] == option.HAND and (result[1] < 0 or result[1] >= player.hand.size()):
			print(f"ERR: invalid number. max:{player.hand.size()-1}")
			return may_destroy_card_in_hand_or_discard(player)
		elif result[0] == option.DISCARD and (result[1] < 0 or result[1] >= player.discard.size()):
			print(f"ERR: invalid number. max:{player.discard.size()-1}")
			return may_destroy_card_in_hand_or_discard(player)
		card_to_destroy = None
		if result[0] == option.HAND:
			card_to_destroy = player.hand.contents.pop(result[1])
		else:
			card_to_destroy = player.discard.contents.pop(result[1])
		card_to_destroy.destroy()
		return (result[0],card_to_destroy)
	else:
		print(f"ERR: invalid responce code: {result[0]}")
		return may_destroy_card_in_hand_or_discard(player)


#(,#)
"""def discard_a_card(player):
	result = player.controler.discard_a_card()
	if globe.DEBUG:
		print("discard_a_card",result)
	if result[0] == option.CANNOT:
		if not player.hand.size() == 0:
			print(f"ERR: You can.")
			return discard_a_card(player)
		else:
			return(option.CANNOT,)
	if not ensure_int(result[1]):
		return discard_a_card(player)
	elif result[1] < 0 or result[1] >= player.hand.size():
		print(f"ERR: invalid number. max:{player.hand.size()-1}")
		return discard_a_card(player)
	card_to_discard = player.hand.contents.pop(result[1])
	player.discard.add(card_to_discard)
	return (option.OK,card_to_discard)"""

"""def x_ray_vision_reveal(player):
	assemble = []
	for p in globe.boss.players:
		if p != player:
			revealed = p.reveal_card()
			if revealed != None:
				assemble.append(revealed)
	if len(assemble) > 0:
		result = player.controler.may_play_one_of_these_cards(assemble)
		if globe.DEBUG:
			print("x_ray_vision_reveal",result)
		if result[0] == option.NO:
			return option.NO
		elif not ensure_int(result[1]):
			return x_ray_vision_reveal(player)
		elif result[1] < 0 or result[1] >= player.hand.size():
			print("ERR: invalid number")
			return x_ray_vision_reveal(player)
		elif assemble[result[1]].ctype_eq(cardtype.LOCATION):
			print("ERR: Cannot play a location this way")
			return x_ray_vision_reveal(player)

		#This should be the card that was revealed
		assemble[result[1]].owner.deck.contents.pop()
		player.play_and_return(assemble[result[1]],assemble[result[1]].owner.deck)
		return option.OK
	return option.CANNOT"""

#(no/ok, if ok:#)
"""def may_destroy_card_in_discard(player):
	result = player.controler.may_destroy_card_in_discard()
	if globe.DEBUG:
		print("may_destroy_card_in_discard",result)
	if result[0] == option.NO:
		return (option.NO,-1)
	elif result[0] == option.OK:
		if not ensure_int(result[1]):
			return may_destroy_card_in_discard(player)
		elif result[1] < 0 or result[1] >= player.discard.size():
			print(f"ERR: invalid number. max:{player.discard.size()-1}")
			return may_destroy_card_in_discard(player)
		card_to_destroy = player.discard.contents.pop(result[1])
		card_to_destroy.destroy()
		return (option.OK,card_to_destroy)
	else:
		print(f"ERR: invalid responce code: {result[0]}")
		return may_destroy_card_in_discard(player)"""


def choose_however_many(instruction_text,player,cards,hint):
	result = player.controler.choose_however_many(instruction_text,player,cards,hint = ai_hint.IFBAD)
	if globe.DEBUG:
		print("choose_however_many",result)
	if result[0] == option.NO:
		return None
	elif result[0] == option.OK:
		assemble = []
		for r in result[1:]:
			#print("FJFHJFHFHFHF",r)
			if not ensure_int(r):
				print(f"ERR: invalid symbol {r}.")
				return choose_however_many(instruction_text,player,cards,hint)
			elif r < 0 or r >= len(cards):
				print(f"ERR: invalid number {r}. max:{len(cards)-1}")
				return choose_however_many(instruction_text,player,cards,hint)
			assemble.append(cards[r])
		return assemble
	else:
		print(f"ERR: invalid responce code: {result[0]}")
		return choose_however_many(instruction_text,player,cards,hint)

