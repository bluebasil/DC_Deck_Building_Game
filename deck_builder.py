import cards
import random

def get_starting_deck(player):
	assemble = []
	#for c in range(7):
	#	assemble.append(cards.punch(player))
	#for c in range(3):
	#	assemble.append(cards.vunerability(player))
	for c in range(10):
		assemble.append(cards.punch(player))
	assemble.append(cards.the_bat_signal(player))
	for c in range(3):
		assemble.append(cards.punch(player))
	assemble.append(cards.fastest_man_alive(player))
	assemble.append(cards.the_batmobile(player))
	"""assemble.append(cards.punch(player))
	assemble.append(cards.lasso_of_truth(player))
	assemble.append(cards.high_tech_hero(player))
	assemble.append(cards.x_ray_vision(player))
	assemble.append(cards.heat_vision(player))
	assemble.append(cards.king_of_atlantis(player))"""
	for c in range(3):
		assemble.append(cards.punch(player))
	assemble.append(cards.king_of_atlantis(player))
	assemble.append(cards.weakness(player))
	assemble.append(cards.kick(player))
	assemble.append(cards.vunerability(player))
	assemble.append(cards.punch(player))
	assemble.append(cards.suicide_squad(player))
	assemble.append(cards.suicide_squad(player))
	assemble.append(cards.suicide_squad(player))
	

	return assemble

def initialize_weaknesses():
	assemble = []
	for c in range(20):
		assemble.append(cards.weakness())
	return assemble

def initialize_kicks():
	assemble = []
	for c in range(16):
		assemble.append(cards.kick())
	return assemble


def initialize_supervillains():
	assemble = []
	assemble.append(cards.ras_al_ghul())
	return assemble

def initialize_deck():
	assemble = []

	for c in range(3):
		assemble.append(cards.aquamans_trident())

	for c in range(2):
		assemble.append(cards.bane())

	assemble.append(cards.fastest_man_alive())

	for c in range(3):
		assemble.append(cards.green_arrow())

	for c in range(3):
		assemble.append(cards.heat_vision())

	for c in range(3):
		assemble.append(cards.high_tech_hero())

	assemble.append(cards.king_of_atlantis())

	for c in range(3):
		assemble.append(cards.lasso_of_truth())

	for c in range(2):
		assemble.append(cards.poison_ivy())

	for c in range(6):
		assemble.append(cards.suicide_squad())

	for c in range(3):
		assemble.append(cards.x_ray_vision())

	random.shuffle(assemble)
	return assemble


