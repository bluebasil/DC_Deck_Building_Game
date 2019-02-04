class deck_set:
	large_set = True
	name = "Set Name"
	load_personas = None
	load_deck = None
	load_supervilains = None

	def __init__(self,name,personas,deck,supervillains,large_set = False):
		self.large_set = large_set
		self.name = name
		self.load_personas = personas
		self.load_deck = deck
		self.load_supervilains = supervillains