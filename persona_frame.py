import arcade
import globe

def overvalue():
	return 1.1

class persona:
	player = None
	name = ""
	text = ""
	active = True
	image = "base/images/personas/Aquaman MC.jpg"
	texture = None

	def __init__(self,player = None):
		self.texture = arcade.load_texture(self.image)
		if player != None:
			self.set_owner(player)

	def set_owner(self,player):
		self.player = player


	def ai_overvalue(self,card):
		return 0

	def ready(self):
		return

	def gain_power(self,card):
		return

	def draw_power(self):
		return

	def destory_power(self):
		return

	def discard_power(self):
		return

	def card_pass_power(self):
		return

	def gain_vp_power(self):
		return

	def failed_to_avoid_power(self):
		return

	def reset(self):
		return

	def any_time(self):
		return False

	def ai_is_now_a_good_time(self):
		return False

	def avoided_attack(self):
		return


#For "has all players superhero/supervillain ext"
class dispatch(persona):
	name = "..."
	text = "Has the text of all personas"
	image = "..."
	texture = None
	persona_list = []
	old_persona = None

	def __init__(self,player):
		self.texture = player.persona.texture
		self.player = player
		self.name = player.persona.name
		self.persona_list = []
		for p in globe.boss.players:
			self.persona_list.append(p.persona)
			p.persona.old_player = p
			p.persona.player = player
			p.persona.ready()
		self.old_persona = player.persona
		player.persona = self

	def restore(self):
		self.player.persona = self.old_persona
		for p in self.persona_list:
			p.player = p.old_player
			p.reset()



	def gain_power(self,card):
		for p in self.persona_list:
			p.gain_power(card)
		return

	def draw_power(self):
		for p in self.persona_list:
			p.draw_power()
		return

	def destory_power(self):
		for p in self.persona_list:
			p.destory_power()
		return

	def discard_power(self):
		for p in self.persona_list:
			p.discard_power()
		return

	def card_pass_power(self):
		for p in self.persona_list:
			p.card_pass_power()
		return

	def gain_vp_power(self):
		for p in self.persona_list:
			p.gain_vp_power()
		return

	def failed_to_avoid_power(self):
		for p in self.persona_list:
			p.failed_to_avoid_power()
		return

	def ai_is_now_a_good_time(self):
		for p in self.persona_list:
			p.ai_is_now_a_good_time()
		return False

	def avoided_attack(self):
		for p in self.persona_list:
			p.avoided_attack()
		return
