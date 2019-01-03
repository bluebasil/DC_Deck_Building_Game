import cards
import random

def get_starting_deck(player):
	assemble = []
	for c in range(7):
		assemble.append(cards.punch(player))
	for c in range(3):
		assemble.append(cards.vunerability(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.kick(player))
	#assemble.append(cards.catwoman(player))
	#assemble.append(cards.catwoman(player))
	#assemble.append(cards.the_dark_knight(player))
	#assemble.append(cards.clayface(player))


	random.shuffle(assemble)

	return assemble


"""assemble.append(cards.punch(player))
	assemble.append(cards.lasso_of_truth(player))
	assemble.append(cards.high_tech_hero(player))
	assemble.append(cards.x_ray_vision(player))
	assemble.append(cards.heat_vision(player))
	assemble.append(cards.king_of_atlantis(player))
	for c in range(3):
		assemble.append(cards.punch(player))
	assemble.append(cards.king_of_atlantis(player))
	assemble.append(cards.weakness(player))
	assemble.append(cards.nth_metal(player))
	
	
	assemble.append(cards.the_penguin(player))
	assemble.append(cards.fastest_man_alive(player))
	assemble.append(cards.heat_vision(player))
	assemble.append(cards.mera(player))
"""


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
	assemble.append(cards.the_anti_monitor())
	assemble.append(cards.atrocitus())
	assemble.append(cards.black_manta())
	assemble.append(cards.brainiac())
	assemble.append(cards.captain_cold())
	assemble.append(cards.darkseid())
	assemble.append(cards.deathstroke())
	assemble.append(cards.the_joker())
	assemble.append(cards.lex_luther())
	assemble.append(cards.parallax())
	assemble.append(cards.sinestro())
	random.shuffle(assemble)
	assemble.append(cards.ras_al_ghul())
	return assemble

def initialize_deck():
	assemble = []

	for c in range(3):
		assemble.append(cards.aquamans_trident())

	for c in range(2):
		assemble.append(cards.bane())

	for c in range(3):
		assemble.append(cards.the_batmobile())

	for c in range(3):
		assemble.append(cards.the_bat_signal())

	assemble.append(cards.bizarro())

	assemble.append(cards.blue_beetle())

	for c in range(3):
		assemble.append(cards.bulletproof())

	for c in range(3):
		assemble.append(cards.the_cape_and_cowl())

	for c in range(3):
		assemble.append(cards.catwoman())

	for c in range(2):
		assemble.append(cards.cheetah())

	for c in range(2):
		assemble.append(cards.clayface())

	assemble.append(cards.the_dark_knight())

	for c in range(2):
		assemble.append(cards.doomsday())

	assemble.append(cards.the_emerald_knight())

	assemble.append(cards.fastest_man_alive())

	for c in range(2):
		assemble.append(cards.gorilla_grodd())

	for c in range(3):
		assemble.append(cards.green_arrow())

	for c in range(3):
		assemble.append(cards.green_arrows_bow())

	for c in range(2):
		assemble.append(cards.harley_quinn())

	for c in range(3):
		assemble.append(cards.heat_vision())

	for c in range(3):
		assemble.append(cards.high_tech_hero())

	assemble.append(cards.jonn_jonzz())

	for c in range(4):
		assemble.append(cards.kid_flash())

	assemble.append(cards.king_of_atlantis())

	for c in range(3):
		assemble.append(cards.lasso_of_truth())

	assemble.append(cards.lobo())

	assemble.append(cards.the_man_of_steel())

	for c in range(2):
		assemble.append(cards.mera())

	for c in range(4):
		assemble.append(cards.nth_metal())

	for c in range(2):
		assemble.append(cards.the_penguin())

	for c in range(2):
		assemble.append(cards.poison_ivy())

	for c in range(3):
		assemble.append(cards.power_ring())

	assemble.append(cards.princess_diana_of_themyscira())

	for c in range(2):
		assemble.append(cards.the_riddler())

	for c in range(3):
		assemble.append(cards.robin())

	for c in range(2):
		assemble.append(cards.scarecrow())

	for c in range(2):
		assemble.append(cards.solomon_grundy())

	assemble.append(cards.starro())

	for c in range(6):
		assemble.append(cards.suicide_squad())

	for c in range(4):
		assemble.append(cards.super_speed())

	for c in range(3):
		assemble.append(cards.super_strength())

	for c in range(2):
		assemble.append(cards.super_girl())

	for c in range(2):
		assemble.append(cards.swamp_thing())

	for c in range(2):
		assemble.append(cards.two_face())

	for c in range(3):
		assemble.append(cards.utility_belt())

	for c in range(3):
		assemble.append(cards.x_ray_vision())

	for c in range(2):
		assemble.append(cards.zatanna_zatara())

	random.shuffle(assemble)
	return assemble


