from pyglet import image
#Use of the pyglet image class is based on the documentation found at https://pyglet.readthedocs.io/en/stable/modules/image/index.html
from pyglet import sprite
#Use of the pyglet sprite class is based on the documentation found at https://pyglet.readthedocs.io/en/stable/modules/sprite.html
import resources

class Tile(sprite.Sprite):
    def __init__(self,x,y,tilecolor,hue):
        self.tilecolor=tilecolor
        self.hue=hue
        sprite.Sprite.__init__(self, self.tilecolor)
        self.x=x
        self.y=y
        self.w=tilecolor.width
        self.h=tilecolor.height

    def change_color(self,tilecolor,hue):
        self.image=tilecolor
        self.tilecolor=tilecolor
        self.hue=hue

    def on_click(self,x,y,button):
        if x > self.x and x < self.x+self.w and y > self.y and y < self.y+self.h:
            return True
        return False

class Grid():
    def __init__(self,default_color='r'):
        self.tiles=[]
        self.last_tile=0
        self.tw=resources.redcell.width+30
        self.th=resources.redcell.height+5
        for tile in range(25):
            self.tx,self.ty=20+(self.tw*(5-(tile%5))),300+(self.th*(5-(tile//5)))
            self.tiles.append(Tile(self.tx,self.ty,self.get_color(default_color),default_color))

    def get_color(self,color):
        if color == 'r':
            return resources.redcell
        elif color == 'g':
            return resources.greencell
        elif color == 'b':
            return resources.bluecell
        elif color == 'c':
            return resources.cyancell
        elif color == 'y':
            return resources.yellowcell
        elif color == 'm':
            return resources.magentacell

    def get_tile(self,tile=0):
        return (self.tiles[tile].hue)
    
    def draw(self):
        for tile in self.tiles:
            tile.draw()

    def on_click(self,x,y,button):
        for tile in range(len(self.tiles)):
            if self.tiles[tile].on_click(x,y,button):
                if self.tiles[tile].hue == 'r':
                    self.tiles[tile].change_color(self.get_color('g'),'g')
                elif self.tiles[tile].hue == 'g':
                    self.tiles[tile].change_color(self.get_color('b'),'b')
                elif self.tiles[tile].hue == 'b':
                    self.tiles[tile].change_color(self.get_color('c'),'c')
                elif self.tiles[tile].hue == 'c':
                    self.tiles[tile].change_color(self.get_color('y'),'y')
                elif self.tiles[tile].hue == 'y':
                    self.tiles[tile].change_color(self.get_color('m'),'m')
                elif self.tiles[tile].hue == 'm':
                    self.tiles[tile].change_color(self.get_color('r'),'r')
                self.last_tile = tile

    def on_key_press(self,symbol):
        try:
            if symbol == 114:
                self.tiles[self.last_tile].change_color(self.get_color('r'),'r')
            elif symbol == 103:
                self.tiles[self.last_tile].change_color(self.get_color('g'),'g')
            elif symbol == 98:
                self.tiles[self.last_tile].change_color(self.get_color('b'),'b')
            elif symbol == 99:
                self.tiles[self.last_tile].change_color(self.get_color('c'),'c')
            elif symbol == 121:
                self.tiles[self.last_tile].change_color(self.get_color('y'),'y')
            elif symbol == 109:
                self.tiles[self.last_tile].change_color(self.get_color('m'),'m')
        except:
            pass

