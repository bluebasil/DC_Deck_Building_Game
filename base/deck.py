from . import cards
import random



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

deck = {cards.aquamans_trident: 3, \
		cards.bane: 2, \
		cards.the_batmobile: 3, \
		cards.the_bat_signal: 3, \
		cards.bizarro: 1, \
		cards.blue_beetle: 1, \
		cards.bulletproof: 3, \
		cards.the_cape_and_cowl: 3, \
		cards.catwoman: 3, \
		cards.cheetah: 2, \
		cards.clayface: 2, \
		cards.the_dark_knight: 1, \
		cards.doomsday: 2, \
		cards.the_emerald_knight: 1, \
		cards.fastest_man_alive: 1, \
		cards.gorilla_grodd: 2, \
		cards.green_arrow: 3, \
		cards.green_arrows_bow: 3, \
		cards.harley_quinn: 2, \
		cards.heat_vision: 3, \
		cards.high_tech_hero: 3, \
		cards.jonn_jonzz: 1, \
		cards.kid_flash: 4, \
		cards.king_of_atlantis: 1, \
		cards.lasso_of_truth: 3, \
		cards.lobo: 1, \
		cards.the_man_of_steel: 1, \
		cards.mera: 2, \
		cards.nth_metal: 4, \
		cards.the_penguin: 2, \
		cards.poison_ivy: 2, \
		cards.power_ring: 3, \
		cards.princess_diana_of_themyscira: 1, \
		cards.the_riddler: 2, \
		cards.robin: 3, \
		cards.scarecrow: 2, \
		cards.solomon_grundy: 2, \
		cards.starro: 1, \
		cards.suicide_squad: 6, \
		cards.super_speed: 4, \
		cards.super_strength: 3, \
		cards.super_girl: 2, \
		cards.swamp_thing: 2, \
		cards.two_face: 2, \
		cards.utility_belt: 3, \
		cards.x_ray_vision: 3, \
		cards.zatanna_zatara: 2, \
		cards.arkham_asylum: 1, \
		cards.the_batcave: 1, \
		cards.fortress_of_solitude: 1, \
		cards.titans_tower: 1, \
		cards.the_watchtower: 1, \
		}

def initialize_deck():
	assemble = []
	for card,num in deck.items():
		for i in range(num):
			assemble.append(card())
	random.shuffle(assemble)
	return assemble
"""
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

	assemble.append(cards.arkham_asylum())
	assemble.append(cards.the_batcave())
	assemble.append(cards.fortress_of_solitude())
	assemble.append(cards.titans_tower())
	assemble.append(cards.the_watchtower())

	random.shuffle(assemble)
	return assemble


"""