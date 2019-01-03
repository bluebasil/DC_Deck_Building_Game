import deck_builder
import cardtype

def print_card(card, num = 0):
	print("\033[;7m" + colour[card.ctype] + f"{num:<2} {card.name:<20}vp:{card.vp:>2} cost:{card.cost:>2}" + colour[cardtype.ANY] + \
		f"\n{card.text}")

colour = {cardtype.STARTER: '\033[93m', \
			cardtype.WEAKNESS: '\033[92m', \
			cardtype.HERO: '\033[94m', \
			cardtype.VILLAIN: '\033[91m', \
			cardtype.SUPERPOWER: '\033[96m', \
			cardtype.EQUIPMENT: '\033[89m', \
			cardtype.LOCATION: '\033[95m', \
			cardtype.ANY: '\033[0m'}


deck = deck_builder.initialize_deck()

for num, c in enumerate(deck):
	print_card(c,num)
	