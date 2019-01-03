import option
import ai_hint
import time
import random
import globe
import cardtype

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

	def choose_persona(self,persona_list):
		return persona_list[0]

	# Choose to end turn or play any cards
	def turn(self):
		#This is where turn logic goes
		return True

	def may_defend(self, options, attacking_card, attacking_player = None):
		return (option.OK,0)

	def choose_one_of(self,instruction_text,player,cards,hint):
		#base on hint
		return [0]

	def may_choose_one_of(self,instruction_text,player,cards,hint):
		#base on hint
		return [option.NO]

	def may_put_on_top(self,instruction_text):
		return [option.OK]

	def ok_or_no(self,instruction_text,player,card,hint):
		return [option.NO]

	#No responce needed
	def reveal(self,instruction_text,player,cards):
		return

	def choose_even_or_odd(self,instruction_text,player):
		return [option.EVEN]

	def choose_a_player(self,player,options):
		return options[0]

	#NO,HAND,DISCARD
	def may_destroy_card_in_hand_or_discard(self):
		return (option.NO,-1)

	#only OK or CANNOT are accepted
	def discard_a_card(self):
		return (option.OK,0)

	#NO,OK
	def may_play_one_of_these_cards(self,cards):
		return (option.NO,-1)

	#NO,OK
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
	def state_name(self):
		print(f" - {self.player.pid} - {self.player.persona.name} - ")

	def turn(self):
		view.print_board()
		print(f"{self.player.pid}'s Turn!")
		while True:
			x = get_input()
			if x[0] == "end":
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
					safe = True
					intx = -1
					try:
						intx = int(x[1])
					except:
						print("?")
						safe == False
					if safe:
						result = self.player.buy(int(x[1]))
						view.print_board()
				if not result:
					print("COULD NOT BUY")
			elif x[0] == "riddle":
				if self.player.played_riddler:
					result = self.player.riddle()
					if not result:
						print("COULD NOT BUY")
				else:
					print("You have not played the riddler this turn")

			else:
				safe = True
				intx = -1
				try:
					intx = int(x[0])
				except:
					print("?")
					safe == False
				if safe:
					if intx < 0 or intx >= self.player.hand.size():
						print("Err: Not a valid card")
					else:
						self.player.play(intx)
						view.print_board()
				else:
					print("?")
			#except Exception as e:
			#	print("?", e)
			#except:
			#	print("?")

	def choose_persona(self,persona_list):
		print("Who would you like to be?")
		for i,p in enumerate(persona_list):
			print(f"{i} {p.name}: {p.text}")
		x = get_input()
		try:
			intx = int(x[0])
		except:
			print("?")
			return self.choose_persona(persona_list)
		return persona_list[intx]


	def may_defend(self, options, attacking_card, attacking_player = None):
		global view
		self.state_name()
		print(f"!{self.player.pid}! may_defend")
		print(f"{attacking_card.name}'s attack: {attacking_card.attack_text}.")
		view.print_custom(options)
		x = get_input()
		if x[0] == "no":
			return (option.NO,-1)
		elif x[0] == "ok":
			intx = -1
			try:
				intx = int(x[1])
			except:
				print("?")
				return self.may_defend(options,attacking_card,attacking_player)
			return (option.OK,intx)
		else:
			print("?")
			return self.may_defend(options,attacking_card,attacking_player)

	def choose_one_of(self,instruction_text,player,cards,hint):
		self.state_name()
		global view
		print(instruction_text)
		view.print_custom(cards)
		print(instruction_text)
		x = get_input()
		intx = -1
		try:
			intx = int(x[0])
		except:
			print("?")
			return self.choose_one_of(instruction_text,player,cards,hint)
		return [intx]

	def may_choose_one_of(self,instruction_text,player,cards,hint):
		self.state_name()
		global view
		print(instruction_text)
		view.print_custom(cards)
		print(instruction_text)
		x = get_input()
		if x[0] == "no":
			return [option.NO]
		elif x[0] == "ok":
			intx = -1
			safe = True
			try:
				intx = int(x[1])
			except:
				print("?")
				safe = False
			if safe:
				return [option.OK,intx]
		print("??")
		return self.may_choose_one_of(instruction_text,player,cards,hint)

	def ok_or_no(self,instruction_text,player,card,hint):
		self.state_name()
		global view
		print(instruction_text)
		if card != None:
			view.print_card(card)
			print(instruction_text)
		x = get_input()
		if x[0] == "ok":
			return [option.OK]
		elif x[0] == "no":
			return [option.NO]
		else:
			print("?")
			return self.ok_or_no(instruction_text,player,card,hint)

	def reveal(self,instruction_text,player,cards):
		self.state_name()
		global view
		print(instruction_text, flush = True)
		view.print_custom(cards)
		time.sleep(3)
		return

	def choose_even_or_odd(self,instruction_text,player):
		self.state_name()
		print(f"{instruction_text} (even/odd)")
		x = get_input()
		if x[0] == "even":
			return [option.EVEN]
		elif x[0] == "odd":
			return [option.ODD]
		else:
			return choose_even_or_odd(instruction_text,player)

	def choose_a_player(self,instruction_text,player,options):
		self.state_name()
		print(instruction_text)
		for i,p in enumerate(options):
			print(f"{i} - {p.persona.name}")
		x = get_input()
		intx = -1
		try:
			intx = int(x[0])
		except:
			print("?")
			return self.choose_a_player(instruction_text,player,options)
		return [intx]


	# card number, 0 is none
	def may_destroy_card_in_hand_or_discard(self):
		self.state_name()
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
					return self.may_destroy_card_in_hand_or_discard()
				return (option.DISCARD,intx)
		print("?")
		return self.may_destroy_card_in_hand_or_discard()

	#card number
	def discard_a_card(self):
		self.state_name()

		print("discard_a_card")
		x = get_input()
		intx = -1
		try:
			intx = int(x[0])
		except:
			print("?")
			return self.discard_a_card()
		return (option.OK,intx)
		
			

	def may_play_one_of_these_cards(self,cards):
		self.state_name()
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
				return self.may_play_one_of_these_cards(cards)
			return (option.OK,intx)
				
		
		print("?")
		return self.may_play_one_of_these_cards(cards)

	def may_destroy_card_in_discard(self):
		self.state_name()
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



class cpu(controler):
	#sleep length between actions
	slti = 0
	invisible = False

	def __init__(self,player,invisible = False):
		#self.boss = boss
		self.player = player
		self.invisible = invisible

	def display_thought(self,text):
		if not self.invisible:
			print(text, flush = True)
			time.sleep(self.slti)

	def sort_by_cost(self,card):
		if card.name == "Weakness":
			return -2
		if card.name == "Vunerability":
			return -1
		#if card.name == "Punch":
		return card.cost

	def sort_by_play_order(self,card):
		if card.name == "Weakness":
			return 500
		if card.name == "Vunerability":
			return 750
		if card.name == "Punch":
			return 250
		if card.ctype == cardtype.LOCATION:
			return -1
		return card.cost

	def choose_persona(self,persona_list):
		return random.choice(persona_list)

	# Choose to end turn or play any cards
	def turn(self):
		global view
		if not self.invisible:
			view.print_board()
		self.display_thought(f"Begining of AI {self.player.pid}'s turn")
		self.player.hand.contents.sort(key = self.sort_by_play_order)
		
		while self.player.hand.size() > 0:
			size_check = self.player.hand.size()
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} is going to play a {self.player.hand.contents[0].name} (total power = {self.player.played.power})")
			self.player.play(0)
			if size_check - 1 != self.player.hand.size():
				self.display_thought("(Differtent cards than expected)")
				self.player.hand.contents.sort(key = self.sort_by_play_order)

		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} has {self.player.played.power} power!")
		if globe.boss.supervillain_stack.size() > 0 and self.player.played.power >= globe.boss.supervillain_stack.contents[-1].cost:
			self.player.buy_supervillain()
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} is buying the supervillain! ({self.player.played.power} power left)")
		assemble = []
		for c in globe.boss.lineup.contents:
			assemble.append(c)
		assemble.sort(key = self.sort_by_cost)
		#Tries to buy everything from most to least expensive
		while len(assemble) > 0:
			test = assemble.pop()
			if self.player.buy_c(test):
				self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} bought {test.name} ({self.player.played.power} power left)")
		while self.player.played.power >= 3 and globe.boss.kick_stack.size() > 0:
			self.player.buy_kick()
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} bought a kick ({self.player.played.power} power left)")

		return


	def choose_one_of(self,instruction_text,player,cards,hint):
		cards.sort(key = self.sort_by_cost)
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} got:{instruction_text}")
		if hint == ai_hint.BEST:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose {cards[-1].name}")
			return [len(cards)-1]
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose {cards[0].name}")
		return [0]

	def may_choose_one_of(self,instruction_text,player,cards,hint):
		cards.sort(key = self.sort_by_cost)
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} got:{instruction_text}")
		if len(cards) == 0:
			return [option.NO]
		if hint == ai_hint.BEST and cards[-1].cost >= 3:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose {cards[-1].name}")
			return [option.OK,len(cards)-1]
		elif hint == ai_hint.WORST and cards[0].cost <= 2:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose {cards[0].name}")
			return [option.OK,0]
		else:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose not yo")
			return [option.NO]
		

	def may_put_on_top(self,instruction_text):
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} got:{instruction_text}")
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose to do so")
		return option.OK

	def ok_or_no(self,instruction_text,player,card,hint):
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} got:{instruction_text}")
		if hint == ai_hint.ALWAYS:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose to do so")
			return [option.OK]
		elif hint == ai_hint.IFBAD and card.cost > 1:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose NOT to do so")
			return [option.NO]
		else:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose to do so (by default)")
			return [option.OK]

	#only OK or CANNOT are accepted
	def discard_a_card(self):
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} told to discard a card")
		if self.player.hand.size() == 0:
			self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} does not have a hand")
			return option.CANNOT
		else:
			lowest_cost = 20
			lowest_position = -1
			for i,c in enumerate(self.player.hand.contents):
				if c.cost < lowest_cost:
					lowest_cost = c.cost
					lowest_position = i
				elif c.cost == lowest_cost:
					if c.name == "Vunerability" or c.name == "Weakness":
						lowest_position = i
		self.display_thought(f"AI {self.player.pid}-{self.player.persona.name} choose to discard a {self.player.hand.contents[lowest_position].name}")
		return (option.OK,lowest_position)
