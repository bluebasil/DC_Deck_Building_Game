import globe
import time
import _thread
import io
import controlers


class dupe_checker:
	all_cards = []
	all_piles = []
	players = 0
	keep_checking = True
	displayed = False
	def __init__(self):
		self.all_cards = []
		self.all_piles = []
		self.keep_checking = True
		self.displayed = False
		self.all_piles.append(globe.boss.main_deck)
		#print("Main deck",self.all_piles[-1],file = buf)
		self.all_piles.append(globe.boss.lineup)
		#print("Lineup",self.all_piles[-1],file = buf)
		self.all_piles.append(globe.boss.destroyed_stack)
		#print("Destroyed",self.all_piles[-1],file = buf)
		self.all_piles.append(globe.boss.supervillain_stack)
		#print("SV stack",self.all_piles[-1],file = buf)
		self.all_piles.append(globe.boss.kick_stack)
		#print("Kick stack",self.all_piles[-1],file = buf)
		self.all_piles.append(globe.boss.weakness_stack)
		#print("Weaknesses",self.all_piles[-1],file = buf)
		for i,p in enumerate(globe.boss.players):
			self.all_piles.append(p.deck)
			#print(f"p{i} deck",self.all_piles[-1],file = buf)
			self.all_piles.append(p.hand)
			#print(f"p{i} hand",self.all_piles[-1],file = buf)
			self.all_piles.append(p.ongoing)
			#print(f"p{i} ongoing",self.all_piles[-1],file = buf)
			self.all_piles.append(p.discard)
			#print(f"p{i} discard",self.all_piles[-1],file = buf)
			self.all_piles.append(p.played)
			#print(f"p{i} played",self.all_piles[-1],file = buf)
			self.all_piles.append(p.under_superhero)
			#print(f"p{i} under_superhero",self.all_piles[-1],file = buf)
			self.all_piles.append(p.over_superhero)
			#print(f"p{i} over_superhero",self.all_piles[-1],file = buf)


		for pile in self.all_piles:
			self.all_cards.extend(pile.contents)



	def check(self):
		buf = io.StringIO()
		#print("hello",file=buf)
		#print(buf.getvalue())


		#print("test",flush=True)
		if len(globe.boss.supervillain_stack.contents) > 0 and self.displayed == False:
			for c in self.all_cards:
				count = 0
				found = []
				for p in self.all_piles:
					add = p.contents.count(c)
					if add > 0:
						found.append(p)
						#Ongoing cards can be played by others.  Once they are discarded tho, they should
						#go back to their owners
						#This is done in the 'discard_a_card' area
						if p.owner != c.owner and p != globe.boss.players[globe.boss.whose_turn].played and p.name != "Ongoing":
							print("ERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO",file = buf)
							print(f"Owner not set properly.",c.name,c,c.owner,p.name,p.owner,file = buf)
							if c.owner	!= None:
								print("card owner:",c.owner.persona.name,file = buf)
							if p.owner	!= None:
								print("pile owner:",p.owner.persona.name,file = buf)
							self.keep_checking = False
					count += add
				if count != 1:
					print("ERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO\nERRORERRORERRORERRORERRORERRORERRORERRORERRROERRORERRORERRORERRORERRORERRORERRORERRORERRRO",file = buf)
					print("ERROR card number unexpected:",c.name,count,c.owner,file = buf)
					for p in found:
						print("pile ",p.name,file = buf)
						if p.owner != None:
							print("-",p.owner.persona.name,file = buf)
					self.keep_checking = False

			if self.keep_checking == False and self.displayed == False:

				self.displayed = True
				print(buf.getvalue(),flush = True)
				globe.boss.players[0].controler = controlers.human(globe.boss.players[0],False)

				#return (True,buf.getvalue())
				#globe.boss.players[0].controler = controlers.human(globe.boss.players[0],False)
				#quit()
		return (False,None)

	def constant_check(self,thread_name,delay):
		while True:
			self.check()
			time.sleep(0.1)


	def setup_checker(self):
		print("STARTING ERR CHECKER",file = buf)
		try:
			_thread.start_new_thread(self.constant_check,("Error Checker", 2, ))
		except Exception as e:
			print("ERR:", e)
			print("Exception in user code:")
			print('-'*60)
			traceback.print_exc(file=sys.stdout)
			print('-'*60)
