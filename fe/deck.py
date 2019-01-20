from . import cards
import random


def initialize_supervillains():
	assemble = []

	return assemble

deck = {}

def initialize_deck():
	assemble = []
	for card,num in deck.items():
		for i in range(num):
			assemble.append(card())
	random.shuffle(assemble)
	return assemble

deck = {cards.amanda_waller: 2, \
		cards.atomica: 2, \
		cards.bizarro_power: 2, \
		cards.catwoman: 2, \
		cards.cold_gun: 3, \
		cards.commissioner_gordon: 3, \
		cards.constructs_of_fear: 2, \
		cards.cosmic_staff: 3, \
		cards.deathstorm: 1, \
		cards.despero: 1, \
		cards.dr_light: 2, \
		cards.element_woman: 2, \
		cards.emperor_penguin: 2, \
		cards.expert_marksman: 2, \
		cards.firestorm_matrix: 1, \
		cards.firestorm: 1, \
		
		cards.belle_reve: 1, \
		cards.blackgate_prison: 1, \
		cards.central_city: 1, \
		cards.earth_3: 1, \
		cards.happy_harbor: 1, \
		cards.star_labs: 1, \
		}

def initialize_deck():
	assemble = []
	for card,num in deck.items():
		for i in range(num):
			assemble.append(card())
	random.shuffle(assemble)
	return assemble