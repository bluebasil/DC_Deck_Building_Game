import uuid

ENDTURN = 0


class special_action:
    button_text = ""
    click_action = None
    card = None

	def __init__(self,button_text,click_action):
		self.action_id = str(uuid.uuid4())
		self.button_text = button_text
		self.click_action = click_action
    def __init__(self, button_text, click_action, card=None):
        self.action_id = str(uuid.uuid4())
        self.button_text = button_text
        self.click_action = click_action
        self.card = card
