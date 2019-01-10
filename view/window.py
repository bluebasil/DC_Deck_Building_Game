import arcade
from . import globe
class window_manager:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    def __init__(self,x,y):
        self.SCREEN_HEIGHT = x
        self.SCREEN_WIDTH = y
        arcade.open_window(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Drawing Example")
        arcade.set_background_color(arcade.color.AMAZON)

    def render(self):
        arcade.start_render()

        # Draw the face
        x = 300
        y = 300
        radius = 200
        arcade.draw_circle_filled(x, y, radius, arcade.color.YELLOW)

        # Draw the right eye
        x = 370
        y = 350
        radius = 20
        arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

        # Draw the left eye
        x = 230
        y = 350
        radius = 20
        arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

        # Draw the smile
        x = 300
        y = 280
        width = 120
        height = 100
        start_angle = 190
        end_angle = 350
        arcade.draw_arc_outline(x, y, width, height, arcade.color.BLACK, start_angle, end_angle, 10)

        self.draw_card(globe.players[0].hand.contents[0],10,10,0)

        # Finish drawing and display the result
        arcade.finish_render()

    def draw_card(self,card,x,y,angle):
        coin = arcade.Sprite(card.image, 1)


    def run(self):
        arcade.run()


window = window_manager(500,500)
window.render()
#window.run()
input()
window.render2()
#window.run()
input()
