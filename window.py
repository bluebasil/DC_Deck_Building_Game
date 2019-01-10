
import arcade
import os
import globe
import math
import _thread
import view
import model
import random
import time

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 3000
SCREEN_HEIGHT = 2000
CARD_SCALE = 0.5
BASE_TEXTURE = arcade.load_texture("base/images/cards/back.jpeg")
BACKGROUND_TEXTURE = arcade.load_texture("images/blue_background2.png")
CPU_TEXTURE = arcade.load_texture("images/cpu_frame.png")
POINT_TEXTURE = arcade.load_texture("images/pointer.png")


class MyGame(arcade.Window):
	""" Our custom Window Class"""

	def __init__(self):
		""" Initializer """
		# Call the parent class initializer
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

		# Set the working directory (where we expect to find files) to the same
		# directory this .py file is in. You can leave this out of your own
		# code, but it is needed to easily run the examples using "python -m"
		# as mentioned at the top of this program.
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)

		# Variables that will hold sprite lists
		#self.player_list = None
		#self.coin_list = None

		# Set up the player info
		#self.player_sprite = None
		#self.score = 0

		# Don't show the mouse cursor
		self.set_mouse_visible(True)

		arcade.set_background_color(arcade.color.AMAZON)

	def setup(self):
		
		""" Set up the game and initialize the variables. """

		# Sprite lists
		#self.player_list = arcade.SpriteList()
		#self.coin_list = arcade.SpriteList()

		# Score
		#self.score = 0

		# Set up the player
		# Character image from kenney.nl
		#self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
		#self.player_sprite.center_x = 50
		#self.player_sprite.center_y = 50
		#self.player_list.append(self.player_sprite)

		# Create the coins
		"""for i in range(COIN_COUNT):

			# Create the coin instance
			# Coin image from kenney.nl
			coin = arcade.Sprite("images/coin_01.png", SPRITE_SCALING_COIN)

			# Position the coin
			coin.center_x = random.randrange(SCREEN_WIDTH)
			coin.center_y = random.randrange(SCREEN_HEIGHT)

			# Add the coin to the lists
			self.coin_list.append(coin)"""

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		#self.coin_list.draw()
		#self.player_list.draw()

		# Put the text on the screen.
		#output = f"Score: {self.score}"

		#arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
		scale = 0.95
		arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,3000, \
							  2000, BACKGROUND_TEXTURE, 0)

		game_board = boss()
		game_board.draw(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

		#arcade.finish_render()





	def on_mouse_motion(self, x, y, dx, dy):
		""" Handle Mouse Motion """

		# Move the center of the player sprite to match the mouse x, y
		#self.player_sprite.center_x = x
		#self.player_sprite.center_y = y
		pass

	def update(self, delta_time):
		""" Movement and game logic """
	   #print(f"updating {delta_time}",flush=True)

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		pass

	def draw_card(self,card,x,y,angle,i):
		arcade.draw_texture_rectangle(x, y, card.texture.width*CARD_SCALE, \
							  card.texture.height*CARD_SCALE, card.texture, angle)

	def draw_back(self,x,y,angle):
		arcade.draw_texture_rectangle(x, y, BASE_TEXTURE.width*CARD_SCALE, \
							  BASE_TEXTURE.height*CARD_SCALE, BASE_TEXTURE, angle)

	

	def draw_deck(self,pile,x,y,angle,visible):
		self.draw_back(x,y,angle)

	def draw_player(self,player,x,y,angle):
		

		
		siz = len(pile.contents)
		start_horizontal = -(siz/2)*(BASE_TEXTURE.width)*CARD_SCALE


		for i,c in enumerate(pile.contents):
			cx = x + start_horizontal*math.sin((angle+90)/180*math.pi)
			cy = y + start_horizontal*math.cos((angle+90)/180*math.pi)
			if visible:
				self.draw_card(c,cx,cy,angle,i)
			else:
				self.draw_back(cx,cy,angle)
			start_horizontal += (BASE_TEXTURE.width-15)*CARD_SCALE

class drawable:
	jminx = jminy = jmaxx = jmaxy = 0
	juristiction_angle = 0
	children = []

	def __init__(self):
		self.children = []

	def draw(self):
		self.children = []

	def clicked(self,x,y):
		return

	def set_juristiction(self,jminx,jminy,jmaxx,jmaxy,angle):
		for c in self.children:
			if c.jminx < jminx:
				self.jminx = c.jminx
			else:
				self.jminx = jminx
			if c.jminy < jminy:
				self.jminy = c.jminy
			else:
				self.jminy = jminy
			if c.jmaxx > jmaxx:
				self.jmaxx = c.jmaxx
			else:
				self.jmaxx = jmaxx
			if c.jmaxy > jmaxy:
				self.jmaxy = c.jmaxy
			else:
				self.jmaxy = jmaxy
		self.juristiction_angle = angle

def draw_stack_size(stack,x,y,scale = 1):
	x = x + BASE_TEXTURE.width*CARD_SCALE*0.5*scale-30
	y = y + BASE_TEXTURE.height*CARD_SCALE*0.5*scale-30
	arcade.draw_rectangle_filled(x,y , 50, 50, arcade.color.BLACK)
	wid = len(stack.contents)
	arcade.draw_text(f"{len(stack.contents)}", x-int(math.log(wid,10))*6 - 4, y-5, arcade.color.WHITE, 15)

class boss(drawable):
	def draw(self,x,y):
		super().draw()
		"""play_num = len(globe.boss.players)
		progress = math.pi*2/play_num
		angle = math.pi/2
		hype1 = SCREEN_HEIGHT/2 - 1.5*(BASE_TEXTURE.height+15)*CARD_SCALE
		hype2 = SCREEN_WIDTH/2 - 1.5*(BASE_TEXTURE.height+15)*CARD_SCALE
		if hype1 < 0:
			print(f"HYPE FAILED: {hype1}.  {SCREEN_HEIGHT}, {BASE_TEXTURE.height}")
		cx = x - hype2*math.cos(angle)
		cy = y - hype1*math.sin(angle)


		for p in globe.boss.players:
			cx = x - hype2*math.cos(angle)
			cy = y - hype1*math.sin(angle)


			new_player = player()
			self.children.append(new_player)
			new_player.draw(p,cx,cy,angle-math.pi/2)

			angle += progress
		"""
		

		#player
		new_player = player()
		self.children.append(new_player)
		new_player.draw(globe.boss.players[0],0,0,0)
		siz = 200
		start = SCREEN_HEIGHT-25
		#Other players
		for i,p in enumerate(globe.boss.players[1:]):
			new_player = player_icon()
			self.children.append(new_player)
			new_player.draw(p,0,start,0)
			#enumerate will start at 0
			if i+1 == globe.boss.whose_turn:
				point_scale = 0.25
				arcade.draw_texture_rectangle(400, start-100, POINT_TEXTURE.width*point_scale, \
							  POINT_TEXTURE.height*point_scale, POINT_TEXTURE, 0)
			start -= siz +25

		if 0 == globe.boss.whose_turn:
			point_scale = 0.25
			arcade.draw_texture_rectangle(400, 800, POINT_TEXTURE.width*point_scale, \
						  POINT_TEXTURE.height*point_scale, POINT_TEXTURE, 90)



		lineup = pile()
		self.children.append(lineup)
		lineup.draw(globe.boss.lineup,SCREEN_WIDTH/2,SCREEN_HEIGHT/2+BASE_TEXTURE.height*CARD_SCALE + 15,True)

		svstack = card()
		self.children.append(svstack)
		x = SCREEN_WIDTH/2
		y = SCREEN_HEIGHT/2+2.125*(BASE_TEXTURE.height*CARD_SCALE + 15)
		if globe.boss.supervillain_stack.current_sv == globe.boss.supervillain_stack.contents[-1]: 
			svstack.draw(globe.boss.supervillain_stack.current_sv,x,y,1.25)
		else:
			svstack.draw_down(x,y,1.25)
		draw_stack_size(globe.boss.supervillain_stack,x,y,1.25)

		if len(globe.boss.main_deck.contents) > 0:
			deck = card()
			self.children.append(deck)
			x = SCREEN_WIDTH/2+2*(BASE_TEXTURE.width*CARD_SCALE + 15)+50
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15)
			deck.draw_down(x,y)
			draw_stack_size(globe.boss.main_deck,x,y)

		if len(globe.boss.weakness_stack.contents) > 0:
			weaknesses = card()
			self.children.append(weaknesses)
			x = SCREEN_WIDTH/2-(BASE_TEXTURE.width*CARD_SCALE + 15)-50
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15)
			weaknesses.draw(globe.boss.weakness_stack.contents[-1],x,y)
			draw_stack_size(globe.boss.weakness_stack,x,y)

		if len(globe.boss.kick_stack.contents) > 0:
			kicks = card()
			self.children.append(kicks)
			x = SCREEN_WIDTH/2-2*(BASE_TEXTURE.width*CARD_SCALE + 15)-50
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15)
			kicks.draw(globe.boss.kick_stack.contents[-1],x,y)
			draw_stack_size(globe.boss.kick_stack,x,y)

		if len(globe.boss.destroyed_stack.contents) > 0:
			destroyed = card()
			self.children.append(destroyed)
			x = SCREEN_WIDTH/2+(BASE_TEXTURE.width*CARD_SCALE + 15)+50
			y = SCREEN_HEIGHT/2+2*(BASE_TEXTURE.height*CARD_SCALE + 15)
			destroyed.draw(globe.boss.destroyed_stack.contents[-1],x,y)
			draw_stack_size(globe.boss.destroyed_stack,x,y)


		#play area
		for p in globe.boss.players:
			play = pile()
			self.children.append(play)
			play.draw(p.played,SCREEN_WIDTH/2,SCREEN_HEIGHT/2,True)


class player_icon(drawable): 
	def draw(self,player,x,y,angle):
		super().draw()
		wid = 330
		hight = wid/1.96
		arcade.draw_texture_rectangle(wid/2, y - hight/2+7, wid, \
							  hight, CPU_TEXTURE, 0)
		
		
		#arcade.draw_text(player.persona, 10, 20, arcade.color.WHITE, 14)
		#if player.persona != None:

		#	arcade.draw_text(f"{player.pid} - {player.persona.name}\n Deck:{len(player.deck.contents)}, Discard:{len(player.discard.contents)} \nOngoing:{len(player.ongoing.contents)}, Hand:{len(player.hand.contents)}", x, y, arcade.color.BLACK, 15)

		if player.persona != None:
			if player.persona.texture == None:
				player.persona.texture = arcade.load_texture(player.persona.image)
			MC = personas()
			self.children.append(MC)
			MC.draw(player.persona,x+player.persona.texture.width*0.2/2,y-player.persona.texture.height*0.2/2,0.2)

		if len(player.discard.contents) > 0:
			discard = card()
			self.children.append(discard)
			discard.draw(player.discard.contents[-1],x+player.persona.texture.width*0.2*1.25,y-BASE_TEXTURE.height*0.2*0.25,0.2)

		if len(player.deck.contents) > 0:
			deck = card()
			self.children.append(deck)
			deck.draw_down(x+player.persona.texture.width*0.2*1.25,y-player.persona.texture.height*0.2+BASE_TEXTURE.height*0.2*0.25,0.2)


		if len(player.ongoing.contents) > 0:
			ongoing = pile()
			self.children.append(ongoing)
			ongoing.draw_squished(player.ongoing,x+player.persona.texture.width*0.2*1.75,y-BASE_TEXTURE.height*0.2*0.25,150,True,0.2)

		if len(player.hand.contents) > 0:
			hand = pile()
			self.children.append(hand)
			hand.draw_squished(player.hand,x+player.persona.texture.width*0.2*1.75,y-player.persona.texture.height*0.2+BASE_TEXTURE.height*0.2*0.25,150,False,0.2)

	   

class player(drawable): 
	def draw(self,player,x,y,angle):
		super().draw()


		self.maxy = 2*(BASE_TEXTURE.height*CARD_SCALE+15) 
		self.miny = 0
		buffx = 0
		buffy = 0
		if player.persona != None:
			if player.persona.texture == None:
				player.persona.texture = arcade.load_texture(player.persona.image)

			MC = personas()
			self.children.append(MC)
			MC.draw(player.persona,x+player.persona.texture.width/2,self.maxy/2,0.75)
			buffx += player.persona.texture.width

		if len(player.discard.contents) > 0:
			discard = card()
			self.children.append(discard)
			x = buffx+CARD_SCALE*BASE_TEXTURE.width/2
			y = BASE_TEXTURE.height*CARD_SCALE/2
			discard.draw(player.discard.contents[-1],x,y)
			draw_stack_size(player.discard,x,y)

		if len(player.deck.contents) > 0:
			hand = card()
			self.children.append(hand)
			x = buffx+CARD_SCALE*BASE_TEXTURE.width/2
			y = 1.5*(BASE_TEXTURE.height*CARD_SCALE+15)
			hand.draw_down(x,y)
			draw_stack_size(player.deck,x,y)


		ongoing = pile()
		self.children.append(ongoing)
		ongoing.draw(player.ongoing,SCREEN_WIDTH-BASE_TEXTURE.width*CARD_SCALE/2,1.5*(BASE_TEXTURE.height*CARD_SCALE+15))

		hand = pile()
		self.children.append(hand)
		hand.draw(player.hand,SCREEN_WIDTH-BASE_TEXTURE.width*CARD_SCALE/2,BASE_TEXTURE.height*CARD_SCALE/2)

class pile(drawable):
	def draw(self,pile,x,y,center = False):
		super().draw()
		pos = x
		if center:
			pos = x + len(pile.contents)/2*(BASE_TEXTURE.width*CARD_SCALE + 15) - (BASE_TEXTURE.width*CARD_SCALE + 15)/2
		seperation = BASE_TEXTURE.width*CARD_SCALE + 15
		for c in pile.contents:
			new_card = card()
			self.children.append(new_card)
			new_card.draw(c,pos,y)
			pos -= seperation
	def draw_squished(self,pile,x,y,width,visible,scale = 1):
		seperation = width/len(pile.contents)
		pos = x
		for c in pile.contents:
			new_card = card()
			self.children.append(new_card)
			if visible:
				new_card.draw(c,pos,y,scale)
			else:
				new_card.draw_down(pos,y,scale)
			pos += seperation


		
		#start_horizontal = -(10*BASE_TEXTURE.width/2)*CARD_SCALE
		"""start_vertical = -(BASE_TEXTURE.height+15)*CARD_SCALE

		start_horizontal = (7*BASE_TEXTURE.width/2)*CARD_SCALE
		cx = x + start_horizontal*math.cos(angle) + start_vertical*math.sin(angle)
		cy = y + start_horizontal*math.sin(angle) + start_vertical*math.cos(angle)
		deck = pile()
		self.children.append(deck)
		deck.draw(player.deck,cx,cy,angle,False,False)

		start_horizontal -= BASE_TEXTURE.width*CARD_SCALE + 15

		cx = x + start_horizontal*math.cos(angle) + start_vertical*math.sin(angle)
		cy = y + start_horizontal*math.sin(angle) + start_vertical*math.cos(angle)
		discard = pile()
		self.children.append(discard)
		discard.draw(player.discard,cx,cy,angle,True,False)

		start_vertical = 0
		start_horizontal = 0

		cx = x + start_horizontal*math.cos(angle) + start_vertical*math.sin(angle)
		cy = y + start_horizontal*math.sin(angle) + start_vertical*math.cos(angle)
		ongoing = pile()
		self.children.append(ongoing)
		ongoing.draw(player.ongoing,cx,cy,angle,True,True)

		start_vertical = (BASE_TEXTURE.height+15)*CARD_SCALE
		start_horizontal = 0

		cx = x + start_horizontal*math.cos(angle) - start_vertical*math.sin(angle)
		cy = y + start_horizontal*math.sin(angle) + start_vertical*math.cos(angle)
		hand = pile()
		self.children.append(hand)
		hand.draw(player.hand,cx,cy,angle,True,True)

		#Should i make the play area global?
		start_vertical = 2*(BASE_TEXTURE.height+15)*CARD_SCALE
		start_horizontal = 0

		cx = x + start_horizontal*math.cos(angle) - start_vertical*math.sin(angle)
		cy = y + start_horizontal*math.sin(angle) + start_vertical*math.cos(angle)
		play = pile()
		self.children.append(play)
		play.draw(player.played,cx,cy,angle,True,True)

		self.set_juristiction(x-(7*BASE_TEXTURE.width/2)*CARD_SCALE,y - (BASE_TEXTURE.height+15)*CARD_SCALE,x + (7*BASE_TEXTURE.width/2)*CARD_SCALE,y + 2*(BASE_TEXTURE.height+15)*CARD_SCALE,angle)
		arcade.draw_point(x, y, arcade.color.RED, 10)"""


"""class pile(drawable):
	def draw(self,pile,x,y,angle,visible,spread):
		siz = len(pile.contents)
		start_horizontal = 0
		if spread:
			start_horizontal = -(siz/2)*(BASE_TEXTURE.width+5)*CARD_SCALE
		else:
			start_horizontal = BASE_TEXTURE.width*CARD_SCALE/2
		for i,c in enumerate(pile.contents):
			
			cx = x + start_horizontal*math.cos(angle)
			cy = y + start_horizontal*math.sin(angle)
			new_drawable = card()
			self.children.append(new_drawable)
			new_drawable.draw(c,cx,cy,angle,i,visible)
			if spread:
				start_horizontal += (BASE_TEXTURE.width+5)*CARD_SCALE

		self.set_juristiction(x-(siz/2)*(BASE_TEXTURE.width+5)*CARD_SCALE,y,x+(siz/2)*(BASE_TEXTURE.width+5)*CARD_SCALE,y+ BASE_TEXTURE.height*CARD_SCALE,angle)
"""

class card(drawable):
	def draw(self,card,x,y,scale = 1):
		super().draw()
		#print(card.name)
		arcade.draw_texture_rectangle(x, y, card.texture.width*CARD_SCALE*scale, \
				card.texture.height*CARD_SCALE*scale, card.texture, 0)
		#arcade.draw_point(x, y, arcade.color.RED, 10)
	def draw_down(self,x,y,scale = 1):
		super().draw()
		arcade.draw_texture_rectangle(x, y, BASE_TEXTURE.width*CARD_SCALE*scale, \
				BASE_TEXTURE.height*CARD_SCALE*scale, BASE_TEXTURE, 0)
		#arcade.draw_point(x, y, arcade.color.RED, 10)

class personas(drawable):
	def draw(self,persona,x,y,scale = 1):
		super().draw()
		#print(card.name)
		arcade.draw_texture_rectangle(x, y, persona.texture.width*scale, \
				persona.texture.height*scale, persona.texture, 0)
		#arcade.draw_point(x, y, arcade.color.RED, 10)


##############################################

def thread_game(thread_name,delay):
	globe.boss.start_game()
	
	

def main():
	globe.view = view.view_controler()
	globe.boss = model.model()
	""" Main method """
	window = MyGame()
	window.setup()
	
	print("GHGsyhsH")
	_thread.start_new_thread(thread_game,("Game", 2, ))
	print("GHsewrGH")
	time.sleep(1)
	arcade.run()
	
	#_thread.start_new_thread(,("View", 2, ))
	
	print("GDSFGD")
	#arcade.run()


if __name__ == "__main__":
	main()




"""class window_manager:
	SCREEN_WIDTH = 1000
	SCREEN_HEIGHT = 1000
	CARD_SCALE = 0.5
	def __init__(self,x,y):
		self.SCREEN_HEIGHT = x
		self.SCREEN_WIDTH = y
		arcade.open_window(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Drawing Example")
		arcade.set_background_color(arcade.color.AMAZON)

	def render(self):
		arcade.start_render()


		self.draw_pile(globe.boss.players[0].hand,1000,1000,0,True)

		# Finish drawing and display the result
		arcade.finish_render()

	def draw_card(self,card,x,y,angle,i):
		#coin = arcade.Sprite(card.image, 0.8)
		texture = arcade.load_texture(card.image)
		arcade.draw_texture_rectangle(x, y, texture.width*self.CARD_SCALE, \
							  texture.height*self.CARD_SCALE, texture, angle)

	def draw_back(self,x,y,angle):
		texture = arcade.load_texture("base/images/cards/back.jpeg")
		arcade.draw_texture_rectangle(x, y, texture.width*self.CARD_SCALE, \
							  texture.height*self.CARD_SCALE, texture, angle)

	def draw_pile(self,pile,x,y,angle,visible):
		texture = arcade.load_texture("base/images/cards/back.jpeg")
		siz = len(pile.contents)
		start_horizontal = -(siz/2)*(texture.width-15)*self.CARD_SCALE
		for i,c in enumerate(pile.contents):
			cx = x + start_horizontal*math.sin((angle+90)/180*math.pi)
			cy = y + start_horizontal*math.cos((angle+90)/180*math.pi)
			if visible:
				self.draw_card(c,cx,cy,angle,i)
			else:
				self.draw_back(cx,cy,angle)
			start_horizontal += (texture.width-15)*self.CARD_SCALE

	def draw_deck(self,pile,x,y,angle,visible):
		self.draw_back(x,y,angle)




	def run(self):
		arcade.run()


#window = window_manager(500,500)
#window.render()
#window.run()
#input()
#window.render2()
#window.run()
#input()
"""