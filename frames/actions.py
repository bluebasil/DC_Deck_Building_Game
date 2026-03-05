ENDTURN = 0


class special_action:
    button_text = ""
    click_action = None
    card = None

    def __init__(self, button_text, click_action, card=None):
        self.button_text = button_text
        self.click_action = click_action
        self.card = card
