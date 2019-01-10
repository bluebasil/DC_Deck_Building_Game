import arcade

def overvalue():
	return 1.1

class persona:
	player = None
	name = ""
	text = ""
	active = True
	image = "base/images/personas/Aquaman MC.jpg"
	texture = None

	def __init__(self,player):
		self.player = player


	def ai_overvalue(self,card):
		return 0

	def ready(self):
		return

	def gain_power(self,card):
		return

	def draw_power(self):
		return

	def reset(self):
		return

	def any_time(self):
		return False

	def ai_is_now_a_good_time(self):
		return False

	def avoided_attack(self):
		return