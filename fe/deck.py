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
