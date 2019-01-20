import random
from fe import persona as base_personas
from fe import cards as base_card
from fe import deck as base_deck
from base import deck as sv_deck
from base import cards as helper
import card_frame
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
		assemble.append(card_frame.vunerability(player))
	for c in range(7):
		assemble.append(card_frame.punch(player))
	

	#for c in range(5):
	#	assemble.append(card_frame.weakness(player))
	assemble.append(helper.ras_al_ghul(player))
	#assemble.append(base_card.cosmic_staff(player))
	#assemble.append(helper.clayface(player))
	#assemble.append(base_card.firestorm_matrix(player))
	#assemble.append(base_card.star_labs(player))
	assemble.append(card_frame.punch(player))
	assemble.append(card_frame.punch(player))
	assemble.append(card_frame.punch(player))
	assemble.append(card_frame.punch(player))
	assemble.append(card_frame.punch(player))
	assemble.append(card_frame.punch(player))
	assemble.append(base_card.element_woman(player))
	#assemble.append(helper.clayface(player))
	assemble.append(base_card.firestorm_matrix(player))

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
		assemble.append(card_frame.weakness())
	load_textures(assemble)
	return assemble

def initialize_kicks():
	assemble = []
	for c in range(16):
		assemble.append(card_frame.kick())
	load_textures(assemble)
	return assemble


def initialize_supervillains():
	assemble = sv_deck.initialize_supervillains()
	load_textures(assemble)
	return assemble

def initialize_deck():
	assemble = base_deck.initialize_deck()
	load_textures(assemble)
	return assemble
	


