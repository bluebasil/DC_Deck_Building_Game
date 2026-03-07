import threading


class coach:
    header = ""
    content = None

    def __init__(self, header, content):
        self.header = header
        self.content = content


class question:
    text = ""
    card = None
    options = []

    def __init__(self, text, card, options):
        self.text = text
        self.card = card
        self.options = options


class event_bus:
	on_bus = []
	display = None
	# Optional callback fired whenever the display (query) changes.
	# The web server sets this to emit state updates to connected clients.
	on_state_change = None

	def __init__(self):
		self.lock = threading.Lock()
		self.on_bus = []
		self.on_state_change = None

	def query(self,text,card,options):
		new_question = question(text,card,options)
		self.display = new_question
		if self.on_state_change:
			try:
				self.on_state_change()
			except Exception:
				pass

	def satisfy_query(self):
		self.display = None


	def card_clicked(self,c):
		self.lock.acquire()
		try:
			self.on_bus.append(coach("card",c))
		finally:
			self.lock.release()

	def button_clicked(self,button_action):
		self.lock.acquire()
		try:
			self.on_bus.append(coach("button",button_action))
		finally:
			self.lock.release()


	def clear(self):
		self.lock.acquire()
		try:
			self.on_bus = []
			self.display = None
		finally:
			self.lock.release()

	def read(self):
		self.lock.acquire()
		to_return = None
		try:
			to_return = self.on_bus.pop(0)
		finally:
			self.lock.release()
		return to_return
