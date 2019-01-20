import globe
import time
import _thread


class dupe_checker:
	all_cards = []
	all_piles = []
	players = 0
	keep_checking = True
	displayed = False
	def __init__(self):
		self.all_piles.append(globe.boss.main_deck)
		print("Main deck",self.all_piles[-1],flush = True)
		self.all_piles.append(globe.boss.lineup)
		print("Lineup",self.all_piles[-1],flush = True)
		self.all_piles.append(globe.boss.destroyed_stack)
		print("Destroyed",self.all_piles[-1],flush = True)
		self.all_piles.append(globe.boss.supervillain_stack)
		print("SV stack",self.all_piles[-1],flush = True)
		self.all_piles.append(globe.boss.kick_stack)
		print("Kick stack",self.all_piles[-1],flush = True)
		self.all_piles.append(globe.boss.weakness_stack)
		print("Weaknesses",self.all_piles[-1],flush = True)
		for i,p in enumerate(globe.boss.players):
			self.all_piles.append(p.deck)
			print(f"p{i} deck",self.all_piles[-1],flush = True)
			self.all_piles.append(p.hand)
			print(f"p{i} hand",self.all_piles[-1],flush = True)
			self.all_piles.append(p.ongoing)
			print(f"p{i} ongoing",self.all_piles[-1],flush = True)
			self.all_piles.append(p.discard)
			print(f"p{i} discard",self.all_piles[-1],flush = True)
			self.all_piles.append(p.played)
			print(f"p{i} played",self.all_piles[-1],flush = True)
			self.all_piles.append(p.under_superhero)
			print(f"p{i} under_superhero",self.all_piles[-1],flush = True)


		for pile in self.all_piles:
			self.all_cards.extend(pile.contents)



	def check(self):
		print("test",flush=True)
		if len(globe.boss.supervillain_stack.contents) > 0 and self.displayed == False:
			for c in self.all_cards:
				count = 0
				found = []
				for p in self.all_piles:
					add = p.contents.count(c)
					if add > 0:
						found.append(p)
						if p.owner != c.owner and p != globe.boss.players[globe.boss.whose_turn].played:
							print("ERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO",flush = True)
							print(f"Owner not set properly.",c.name,c,c.owner,p,p.owner,flush = True)
							if c.owner	!= None:
								print(c.owner.persona.name)
							if p.owner	!= None:
								print(p.owner.persona.name)
							self.keep_checking = False
					count += add
				if count != 1:
					print("ERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO",flush = True)
					print("ERROR card number unexpected:",c.name,count,c.owner,flush = True)
					for p in found:
						print("pile ",p,flush = True)

					self.keep_checking = False

			if self.keep_checking == False and self.displayed == False:

				self.displayed = True
				#globe.boss.players[0].controler = controlers.human(globe.boss.players[0],False)
				#quit()

	def constant_check(self,thread_name,delay):
		self.check()
		time.sleep(0.01)


	def setup_checker(self):
		print("STARTING ERR CHECKER",flush = True)
		try:
			_thread.start_new_thread(self.constant_check,("Error Checker", 2, ))
		except Exception as e:
			print("ERR:", e)
			print("Exception in user code:")
			print('-'*60)
			traceback.print_exc(file=sys.stdout)
			print('-'*60)
