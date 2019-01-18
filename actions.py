ENDTURN = 0

class special_action:
	button_text = ""
	click_action = None

	def __init__(self,button_text,click_action):
		self.button_text = button_text
		self.click_action = click_action