import random
#from base import persona as base_personas
from base import deck as base_deck

from hu import persona as hu_personas
#from hu import persona as hu_personas
#from fe import persona as fe_personas
from fe import deck as fe_deck
#from base import deck as sv_deck
#from base import cards as helper
from crossover_1 import deck as c1_deck
from crossover_2 import deck as c2_deck
#from crossover_1 import cards as custom
from frames import card_frame
import arcade
import globe


decks = [base_deck.this_set,fe_deck.this_set,c1_deck.this_set,c2_deck.this_set]
choosen_sets = []
#Specifies wether small set personas muct be picked when playing with small sets
any_pick = False


def choose_sets():
	print("Which sets would you like to play with? type 'play' to start game.")
	for i,d in enumerate(decks):
		print(f"{i}  {d.name}    (large set:{d.large_set})")
	x = input()
	if x == 'play':
		if len(choosen_sets) == 0:
			print("You must choose at least 1 set.")
			return choose_sets()
		return
	else:
		intx = -1
		safe = True
		try:
			intx = int(x)
		except:
			print("?")
			safe = False
		if safe and intx >= 0 and intx < len(decks):
			choosen_sets.append(decks.pop(intx))
		return choose_sets()

def get_personas():
	small_sets = []
	large_sets = []
	for d in choosen_sets:
		if globe.DEBUG:
			print(f"Loading {d.name}'s personas...",flush = True)
		if d.large_set:
			large_sets.extend(d.load_personas())
		else:
			small_sets.extend(d.load_personas())
	if not any_pick:
		if len(small_sets) > 0:
			return small_sets
	else:
		large_sets.extend(small_sets)
		large_sets.extend(hu_personas.get_personas())
	return large_sets

def get_starting_deck(player):
	assemble = []
	for c in range(3):
		assemble.append(card_frame.vunerability(player))
	for c in range(7):
		assemble.append(card_frame.punch(player))

	random.shuffle(assemble)
	#assemble.append(custom.gentleman_ghost(player))
	#assemble.append(custom.citizen_steel(player))
	#assemble.append(custom.liberty_belle(player))

	return assemble

def debug_discard(player):
	assemble = []
	return assemble



def initialize_weaknesses():
	assemble = []
	for c in range(20):
		assemble.append(card_frame.weakness())
	return assemble

def initialize_kicks():
	assemble = []
	for c in range(16):
		assemble.append(card_frame.kick())
	return assemble

#if there are any small sets, it only pulls SV's out of them
#i will choose
#the number of SV's to use is the most of the avalable sets of SV's
#first and last SV is chosen from the first and last SV of one of the avalabel sets
def initialize_supervillains():
	small_sets = []
	large_sets = []
	for d in choosen_sets:
		if globe.DEBUG:
			print(f"Loading {d.name}'s SV's...",flush = True)
		if d.large_set:
			large_sets.append(d.load_supervilains())
		else:
			small_sets.append(d.load_supervilains())
	prioritize = large_sets
	if len(small_sets) > 0:
		prioritize = small_sets
	largest_villain_amount = 0
	for d in prioritize:
		largest_villain_amount = max(largest_villain_amount,len(d))
	if len(prioritize) > 1:
		assemble = []
		#Set last SV
		assemble.append(random.choice(prioritize)[0])
		for d in prioritize:
			d.pop(0)
		#Set first SV
		first_SV = random.choice(prioritize)[-1]
		for d in prioritize:
			d.pop()
		while len(assemble) < largest_villain_amount - 1:
			random_set = random.choice(prioritize)
			if len(random_set) > 0:
				choosen_SV = random.choice(random_set)
				assemble.append(choosen_SV)
				random_set.remove(choosen_SV)
		assemble.append(first_SV)
	else:
		assemble = prioritize[0]
	return assemble

def initialize_deck():
	small_sets_cards = []
	#large_sets = []
	assemble = []
	for d in choosen_sets:
		if globe.DEBUG:
			print(f"Loading {d.name}'s deck...",flush = True)
		if d.large_set:
			assemble.extend(d.load_deck())
		else:
			small_sets_cards.extend(d.load_deck())
	#All large sets should be shuffled (although there may be none)
	random.shuffle(assemble)
	random.shuffle(small_sets_cards)
	if len(assemble) == 0:
		return small_sets_cards
	elif len(small_sets_cards) > 0:
		bottom_split = assemble[:int(len(assemble)/2)]
		top_split = assemble[int(len(assemble)/2):]
		top_split.extend(small_sets_cards)
		random.shuffle(top_split)
		assemble = bottom_split
		assemble.extend(top_split)
	return assemble
	


