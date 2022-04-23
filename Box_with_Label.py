import pyglet
from pyglet.text import Label
import resources

class Box_with_Label:
    def __init__(self, x, y, height, width, text,target, fontsize):
        self.backgrounds = [resources.encryptbuttondef,	resources.encryptbuttonhover,resources.encryptbuttonshadow]
        self.bg = pyglet.sprite.Sprite(self.backgrounds[0].get_region(0,0,width,height), x,y)
        self.bodyheight		= 	height
        self.bodywidth 		= 	width
        self.body			=	Label(text, x = x, y = y, height = height, width = width)
        self.execute		=	target
    def draw(self):
        self.bg.draw()
        self.body.draw()