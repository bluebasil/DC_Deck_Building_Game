from . import cards
from . import persona
import random
from frames import deck_frame

#There are in order
def initialize_supervillains():
	assemble = []
	assemble.append(cards.gog())
	assemble.append(cards.eclipso())
	assemble.append(cards.gentleman_ghost())
	assemble.append(cards.ultra_humanite())
	assemble.append(cards.kobra())
	assemble.append(cards.icicle())
	assemble.append(cards.mordru_the_merciless())
	assemble.append(cards.solomon_grundy())
	return assemble

deck = {cards.citizen_steel: 1, \
		cards.dr_mid_nite: 1, \
		cards.girl_power: 1, \
		cards.liberty_belle: 1, \
		cards.monument_point: 1, \
		cards.mystic_bolts: 1, \
		cards.per_degaton: 1, \
		cards.t_spheres: 1, \
		cards.the_hourglass: 1, \
		}

def initialize_deck():
	assemble = []
	for card,num in deck.items():
		for i in range(num):
			assemble.append(card())
	random.shuffle(assemble)
	return assemble


this_set = deck_frame.deck_set("Crossover 1, Justice Society of America",persona.get_personas,initialize_deck,initialize_supervillains,False)

