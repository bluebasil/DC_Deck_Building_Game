from . import cards
from . import persona
import random
from frames import deck_frame

#There are in order
def initialize_supervillains():
	assemble = []
	assemble.append(cards.slade_wilson())
	assemble.append(cards.isabel_rochev())
	assemble.append(cards.brother_blood())
	assemble.append(cards.malcolm_merlyn())
	assemble.append(cards.count_vertigo())
	assemble.append(cards.deadshot())
	assemble.append(cards.china_white())
	assemble.append(cards.edward_fyers())
	return assemble

deck = {cards.arrows_bow: 1, \
		cards.bronze_tiger: 1, \
		cards.collapsible_staff: 1, \
		cards.detective_lance: 1, \
		cards.explosive_arrow: 1, \
		cards.huntress: 1, \
		cards.laurel_lance: 1, \
		cards.mirakuru: 1, \
		cards.moira_queen: 1, \
		cards.mr_blank: 1, \
		cards.promise_to_a_friend: 1, \
		cards.shado: 1, \
		cards.verdant: 1, \
		cards.you_have_failed_this_city: 1, \
		}

def initialize_deck():
	assemble = []
	#for debug
	#for i in range(3):
	for card,num in deck.items():
		for i in range(num):
			assemble.append(card())
	random.shuffle(assemble)
	return assemble


this_set = deck_frame.deck_set("Crossover 2, Arrow",persona.get_personas,initialize_deck,initialize_supervillains,False)

