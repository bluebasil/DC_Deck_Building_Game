import threading

class coach:
	header = ""
	content = None

	def __init__(self,header,content):
		self.header = header
		self.content = content

class event_bus:
	on_bus = []

	def __init__(self):
		self.lock = threading.Lock()
		self.on_bus = []
		print("CREATED?",flush = True)

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
		finally:
			print('Released a lock',flush = True)
			self.lock.release()

	def read(self):
		print("try read")
		self.lock.acquire()
		to_return = None
		try:
			print('Acquired a lock',flush = True)
			to_return = self.on_bus.pop(0)
		finally:
			print('Released a lock',flush = True)
			self.lock.release()
		return to_return