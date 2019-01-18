import threading

class coach:
	header = ""
	content = None

	def __init__(self,header,content):
		self.header = header
		self.content = content

class question:
	text = ""
	card = None
	options = []

	def __init__(self,text,card,options):
		self.text = text
		self.card = card
		self.options = options


class event_bus:
	on_bus = []
	display = None

	def __init__(self):
		self.lock = threading.Lock()
		self.on_bus = []
		print("CREATED?",flush = True)

	def query(self,text,card,options):
		new_question = question(text,card,options)
		print("settingDisplay",options,flush=True)
		self.display = new_question

	def satisfy_query(self):
		self.display = None
		

	def card_clicked(self,c):
		print("try click",flush = True)
		self.lock.acquire()
		try:
			print('Acquired a lock',flush = True)
			self.on_bus.append(coach("card",c))
		finally:
			print('Released a lock',flush = True)
			self.lock.release()

		print("CLICK HEARD:",c.name,len(self.on_bus),flush = True)

	def button_clicked(self,button_action):
		print("try click",flush = True)
		self.lock.acquire()
		try:
			print('Acquired a lock',flush = True)
			self.on_bus.append(coach("button",button_action))
		finally:
			print('Released a lock',flush = True)
			self.lock.release()

		print("CLICK HEARD:",button_action,len(self.on_bus),flush = True)
		

	def clear(self):
		print("try clear",flush = True)
		self.lock.acquire()
		try:
			self.on_bus = []
			self.display = None
		finally:
			print('Released a lock',flush = True)
			self.lock.release()

	def read(self):
		print("try read")
		self.lock.acquire()
		to_return = None
		try:
			print('Acquired a lock',len(self.on_bus),flush = True)
			to_return = self.on_bus.pop(0)
		finally:
			print('Released a lock',flush = True)
			self.lock.release()
		return to_return

