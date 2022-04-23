
import pyglet
from pyglet import text
from pyglet.text import caret,document,layout
from pyglet import image
from pyglet import sprite
import resources

class TextWidget:
    def __init__(self,x,y,width,height,text,batch):
        self.text = text
        
        self.textboxbg = resources.textbg               
        self.usablebg = self.textboxbg.get_region(0,0,width,height)
        self.textboxsprite = sprite.Sprite(self.usablebg,x,y)

        self.textinput = document.FormattedDocument(text)
        self.textinput.set_style(
            start = 0, 
            end = len(self.textinput.text),
            attributes = dict(color = (0,0,0,255))
        )
        
        self.layout = layout.IncrementalTextLayout(
            document = self.textinput,
            width = width-15,
            height = height*4/5,                         #Height of the textbox
            multiline = False,
            batch = batch
        )
        self.caret = caret.Caret(self.layout)
        self.layout.x = x+10
        self.layout.y = y


    def check_hover(self, x, y):
        return (0 < x - self.layout.x < self.layout.width 
                and
                0 < y - self.layout.y < self.layout.height)

    def draw(self):
        self.textboxsprite.draw()

    def mouse_press(self,x,y,button,modifiers,focused):
        if self == focused:
            self.caret.on_mouse_press(x,y,button,modifiers)

    def ontext(self,text,focused):
        if self == focused:
            self.caret.on_text(text)
            
    def istextmoving(self,motion,focused):
        if self == focused:
            self.caret.on_text_motion(motion)

    def keypresses(self,symbol,modifiers,focused,boxes):
        i = 0
        direction = 0
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                direction = -1
            else:
                direction = 1

            if self in boxes:
                i = boxes.index(self)
            else:
                i = 0
                direction = 0
        return i,direction
        

    def gettext(self):
        text = self.textinput.text
        self.textinput.text = ''
        return text