import random
from base import persona as base_personas
from base import cards as base_card
from base import deck as base_deck
import arcade

def load_textures(cards):
	#for c in cards:
	#	c.texture = arcade.load_texture(c.image)
	pass

def get_personas():
	return base_personas.get_personas()

def get_starting_deck(player):
	assemble = []
	for c in range(3):
		assemble.append(base_card.vunerability(player))
	for c in range(7):
		assemble.append(base_card.punch(player))
	

	#for c in range(10):
	#	assemble.append(base_card.weakness(player))

	#assemble.append(base_card.x_ray_vision(player))
	assemble.append(base_card.the_riddler(player))

	#random.shuffle(assemble)
	load_textures(assemble)
	return assemble

def debug_discard(player):
	assemble = []
	#assemble.append(cards.vunerability(player))
	#assemble.append(cards.punch(player))
	#assemble.append(cards.kick(player))

	#random.shuffle(assemble)
	load_textures(assemble)
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
		assemble.append(base_card.weakness())
	load_textures(assemble)
	return assemble

def initialize_kicks():
	assemble = []
	for c in range(16):
		assemble.append(base_card.kick())
	load_textures(assemble)
	return assemble


def initialize_supervillains():
	assemble = base_deck.initialize_supervillains()
	load_textures(assemble)
	return assemble

def initialize_deck():
	assemble = base_deck.initialize_deck()
	load_textures(assemble)
	return assemble
	


