import option
import globe
import cardtype
import ai_hint


def ensure_int(i):
	if not type(i) is int:
		print("ERR: not an integer")
		return False
	else:
		return True

def attack_all(card):
	total_hit = 0
	for p in globe.boss.players:
		if attack(p,card):
			total_hit += 1
	return total_hit

#Returns true if hit by attack
def attack(player,card,by_player = None):
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
				assemble[result[1]].defend()
				return False
		elif result[0] == option.NO:
			return True
		else:
			print("Err: responce")
			return attack(player,card,by_player)
	else:
		return True

def choose_a_player(instruction_text,player,includes_self = True):
	assemble = []
	for i,p in enumerate(globe.boss.players):
		if p != player or includes_self:
			assemble.append(p)
	result = player.controler.choose_a_player(instruction_text,player,assemble)
	if globe.boss.DEBUG:
		print("choose_a_player",result)
	if not ensure_int(result[0]):
		return choose_a_player(instruction_text,player,includes_self)
	elif result[0] < 0 or result[0] >= len(assemble):
		print(f"ERR: invalid number. max:{len(assemble)-1}")
		return choose_a_player(instruction_text,player,includes_self)
	return assemble[result[0]]

def choose_one_of(instruction_text,player,cards,hint = ai_hint.WORST):
	result = player.controler.choose_one_of(instruction_text,player,cards,hint)
	if globe.boss.DEBUG:
		print("choose_one_of",result)
	if not ensure_int(result[0]):
		return choose_one_of(instruction_text,player,cards)
	elif result[0] < 0 or result[0] >= len(cards):
		print(f"ERR: invalid number. max:{len(cards)-1}")
		return choose_one_of(instruction_text,player,cards)
	return cards[result[0]]

def may_choose_one_of(instruction_text,player,cards,hint = ai_hint.BEST):
	result = player.controler.may_choose_one_of(instruction_text,player,cards,hint)
	if globe.boss.DEBUG:
		print("may_choose_one_of",result)
	if result[0] == option.NO:
		return None
	else:
		if not ensure_int(result[1]):
			return may_choose_one_of(instruction_text,player,cards)
		elif result[1] < 0 or result[1] >= len(cards):
			print(f"ERR: invalid number. max:{len(cards)-1}")
			return choose_one_of(instruction_text,player,cards)
		return cards[result[1]]

def ok_or_no(instruction_text,player,card = None,hint = ai_hint.IFBAD):
	result = player.controler.ok_or_no(instruction_text,player,card,hint)
	if globe.boss.DEBUG:
		print("ok_or_no",result)
	if result[0] == option.OK:
		return True
	elif result[0] == option.NO:
		return False
	else:
		print(f"ERR: invalid responce code")
		return ok_or_no(instruction_text,player,hint)

def reveal(reveal_text,player,cards):
	player.controler.reveal(player,cards)

#True for even
def choose_even_or_odd(instruction_text,player):
	result = player.controler.choose_even_or_odd(instruction_text,player)
	if globe.boss.DEBUG:
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
	if globe.boss.DEBUG:
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
def discard_a_card(player):
	result = player.controler.discard_a_card()
	if globe.boss.DEBUG:
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
	return (option.OK,card_to_discard)

def x_ray_vision_reveal(player):
	assemble = []
	for p in globe.boss.players:
		if p != player:
			revealed = p.reveal_card()
			if revealed != None:
				assemble.append(revealed)
	if len(assemble) > 0:
		result = player.controler.may_play_one_of_these_cards(assemble)
		if globe.boss.DEBUG:
			print("x_ray_vision_reveal",result)
		if result[0] == option.NO:
			return option.NO
		elif not ensure_int(result[1]):
			return x_ray_vision_reveal(player)
		elif result[1] < 0 or result[1] >= player.hand.size():
			print("ERR: invalid number")
			return x_ray_vision_reveal(player)
		elif assemble[result[1]].ctype == cardtype.LOCATION:
			print("ERR: Cannot play a location this way")
			return x_ray_vision_reveal(player)

		#This should be the card that was revealed
		assemble[result[1]].owner.deck.contents.pop()
		player.play_and_return(assemble[result[1]],assemble[result[1]].owner.deck)
		return option.OK
	return option.CANNOT

#(no/ok, if ok:#)
def may_destroy_card_in_discard(player):
	result = player.controler.may_destroy_card_in_discard()
	if globe.boss.DEBUG:
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
		return may_destroy_card_in_hand_or_discard(player)


def replace_cards_in_lineup(player):
	return

def discard_top_of_deck(player):
	return None

def play_random_card_from_opponents_hands(player):
	for p in globe.boss.players:
		if p != player:
			#since cards cants be ordered, the first card is random
			card = p.hand.contents.pop()
			player.play_and_return(card,p.hand)
	return 0

def may_destroy_two_cards(player):
	return  []

def gain_card_from_lineup(player):
	return None

def may_discard_a_card(player):
	return None

#This effects 1 player
def fa_add_card_to_lineup(caused_by,player):
	#if attack(player,caused_by):
	#	player.
	return

def fa_hide_card_under_superhero(caused_by,player):
	return

def return_hidden_cards(player):
	return

def fa_destroy_or_discard_hand(caused_by,player,card_to_destroy):
	return

def fa_random_shuffle_two_cards(caused_by,player):
	return []

def fa_disable_superhero(caused_by,player):
	return

def enable_superhero(player):
	return

def fa_reveal_villain_or_discard_two(caused_by,player):
	return

def fa_destroy_hero_villain_superpower_in_hand_discard(caused_by,player):
	return None

def fa_card_in_discard_to_left(caused_by,player):
	return None

def fa_gain_weakness_villains_lineup(caused_by,player):
	return None

def fa_discard_two_or_less(caused_by,player):
	return

