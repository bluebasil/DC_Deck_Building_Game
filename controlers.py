import option

view = None
def set_view(vi):
	global view
	view = vi


#import view
class controler:
	#boss = None
	player = None

	def __init__(self,player):
		#self.boss = boss
		self.player = player

	# Choose to end turn or play any cards
	def turn(self):
		#This is where turn logic goes
		return True

	# card number, 0 is none
	def may_destroy_card_in_hand_or_discard(self):
		return (option.NO,-1)

	#card number
	def discard_a_card(self):
		return (option.OK,0)

	def may_play_one_of_these_cards(self,cards):
		return (option.NO,-1)

	def may_destroy_card_in_discard(self):
		return (option.NO,-1)


def get_input():
	global view
	x = input().split(" ")
	#try:
	if x[0] == "back":
		view.print_board()
	elif x[0] == "destroyed":
		view.print_destroyed()
	elif x[0] == "discard":
		if len(x) == 1:
			view.print_discard()
		else:
			try:
				intx = int(x[1])
				view.print_discard(intx)
			except:
				print("?")
	elif x[0] == "help":
		print("back, discard, others discard, help, ok, no, or a #")
	elif x[0] == "deck":
		if len(x) == 1:
			view.print_deck()
		else:
			try:
				intx = int(x[1])
				view.print_deck(intx)
			except:
				print("?")
	elif x[0] == "hand":
		if len(x) == 1:
			print("?")
		else:
			try:
				intx = int(x[1])
				view.print_hand(intx)
			except:
				print("?")
	elif x[0] == "play":
		if len(x) == 1:
			print("?")
		else:
			try:
				intx = int(x[1])
				view.print_played(intx)
			except:
				print("?")
	else:
		return x
	return get_input()


class human(controler):
	global view
	def turn(self):
		view.print_board()
		print(f"{self.player.pid}'s Turn!")
		while True:
			x = get_input()
			if x[0] == "end":
				self.player.end_turn()
				return
			#print(int(x))
			#try:
			if x[0] == "buy":
				result = False
				if x[1] == "sv":
					result = self.player.buy_supervillain()
					view.print_power()
				elif x[1] == "kick":
					result = self.player.buy_kick()
					view.print_power()
				else:
					result = self.player.buy(int(x[1]))
					view.print_board()
				if not result:
					print("COULD NOT BUY")
			else:
				intx = int(x[0])
				if intx < 0 or intx >= self.player.hand.size():
					print("Err: Not a valid card")
				else:
					self.player.play(intx)
					view.print_board()
			#except Exception as e:
			#	print("?", e)
			#except:
			#	print("?")


	# card number, 0 is none
	def may_destroy_card_in_hand_or_discard(self):
		print("may_destroy_card_in_hand_or_discard (Example: 'ok hand 2', or 'no')")
		x = get_input()
		if x[0] == "no":
			return (option.NO,-1)
		elif x[0] == "ok":
			if x[1] == "hand":
				intx = -1
				try:
					intx = int(x[2])
				except:
					print("?")
				if intx != -1:
					return (option.HAND,intx)
			elif x[1] == "discard":
				intx = -1
				try:
					intx = int(x[2])
				except:
					print("?")
				if intx != -1:
					return (option.DISCARD,intx)
		print("?")
		return self.may_destroy_card_in_hand_or_discard()

	#card number
	def discard_a_card(self):
		print("discard_a_card")
		x = get_input()
		intx = -1
		try:
			intx = int(x[0])
		except:
			print("?")
		if intx != -1:
			return (option.OK,intx)
		else:
			return self.discard_a_card()

	def may_play_one_of_these_cards(self,cards):
		global view
		print("may_play_one_of_these_cards:")
		print(cards)
		view.print_custom(cards)
		x = get_input()
		if x[0] == "no":
			return (option.NO,-1)
		elif x[0] == "ok":
			intx = -1
			try:
				intx = int(x[1])
			except:
				print("?")
			if intx != -1:
				return (option.OK,intx)
			else:
				return self.may_play_one_of_these_cards(cards)
		
		print("?")
		return self.may_play_one_of_these_cards(cards)

	def may_destroy_card_in_discard(self):
		print("may_destroy_card_in_discard (Example: 'ok 2', or 'no')")
		x = get_input()
		if x[0] == "no":
			return (option.NO,-1)
		elif x[0] == "ok":
			try:
				intx = int(x[1])
			except:
				print("?")
			if intx != -1:
				return (option.OK,intx)

		print("?")
		return may_destroy_card_in_discard()



