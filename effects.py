import option
import globe
import cardtype


def ensure_int(i):
	if not type(i) is int:
		print("ERR: not an integer")
		return False
	else:
		return True

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
		globe.boss.destroyed_stack.add(card_to_destroy)
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
			discard_a_card(player)
	elif result[1] < 0 or result[1] >= player.hand.size():
		print(f"ERR: invalid number. max:{player.hand.size()-1}")
		return discard_a_card(player)
	card_to_discard = player.hand.pop(result[1])
	player.discard.append(card_to_discard)
	return (option.OK,card_to_discard)

def x_ray_vision_reveal(player):
	assemble = []
	for p in globe.boss.players:
		if p != player:
			revealed = p.reveal_card()
			if revealed != None:
				assemble.append(revealed)
	if len(assemble) > 0:
		print(assemble)
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
		print("PLATYIONG",assemble[result[1]].owner.deck.size())
		player.play_and_return(assemble[result[1]],assemble[result[1]].owner.deck)
		print("RETURNED",assemble[result[1]].owner.deck.size())
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
		card_to_destroy = player.discard.pop(result[1])
		globe.boss.destroyed_stack.add(card_to_destroy)
		return (option.OK,card_to_destroy)
	else:
		print(f"ERR: invalid responce code: {result[0]}")
		return may_destroy_card_in_hand_or_discard(player)