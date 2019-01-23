from . import cards
import random


def initialize_supervillains():
	assemble = []
	assemble.append(cards.aquaman())
	assemble.append(cards.batman())
	assemble.append(cards.constantine())
	assemble.append(cards.cyborg())
	assemble.append(cards.green_arrow())
	assemble.append(cards.green_lantern())
	assemble.append(cards.martian_manhunter())
	assemble.append(cards.shazam())
	assemble.append(cards.superman())
	assemble.append(cards.swamp_thing())
	assemble.append(cards.wonder_woman())
	random.shuffle(assemble)
	#assemble.append(cards.the_joker())
	assemble.append(cards.the_flash())
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
		cards.giant_growth: 3, \
		cards.giant_growth: 3, \
		cards.giganta: 2, \
		cards.grid: 2, \
		cards.insanity: 3, \
		cards.invulnerable: 3, \
		cards.johnny_quick: 2, \
		cards.mallet: 3, \
		cards.man_bat_serum: 3, \
		cards.man_bat: 2, \
		cards.owlman: 1, \
		cards.pandora: 1, \
		cards.pandoras_box: 2, \
		cards.phantom_stranger: 1, \
		cards.power_armor: 1, \
		cards.power_drain: 2, \
		cards.power_girl: 3, \
		cards.power_ring: 1, \
		cards.royal_flush_gang: 5, \
		cards.secret_society_communicator: 2, \
		cards.sledgehammer: 2, \
		cards.stargirl: 2, \
		cards.steel: 2, \
		cards.steve_trevor: 2, \
		cards.super_intellect: 2, \
		cards.superwoman: 1, \
		cards.the_blight: 2, \
		cards.transmutation: 3, \
		cards.ultra_strength: 1, \
		cards.ultraman: 1, \
		cards.venom_injector: 2, \
		cards.vibe: 2, \
		cards.word_of_power: 2, \
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