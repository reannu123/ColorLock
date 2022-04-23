#All pyglet bindings and references to pyglet classes are based on the examples at pyglet.readthedocs.io/en/stable/programming_quide/quick_start.html
import pyglet
from pyglet.window import mouse
from pyglet.text import Label
import resources

class Button:
	def __init__(self, x, y, shadowoffset, height, width, text,target,buttontype, fontsize,xadjustment,yadjustment):
		self.shadowoffset = shadowoffset
		self.pressed = False
		if buttontype == 'MMencrypt':
			self.backgrounds = [resources.encryptbuttondef,	
								resources.encryptbuttonhover,	
								resources.encryptbuttonshadow]
		elif buttontype == 'MMdecrypt':
			self.backgrounds = [resources.decryptbuttondef,	
								resources.decryptbuttonhover,	
								resources.decryptbuttonshadow]

		elif buttontype == 'back':
			self.backgrounds = [resources.greenbuttondef,	
								resources.greenbuttonhover,	
								resources.greenbuttonshadow]
		
		elif buttontype == 'change':
			self.backgrounds = [resources.green2buttondef,	
								resources.green2buttonhover,	
								resources.green2buttonshadow]
		
		elif buttontype == 'changed':
			self.backgrounds = [resources.redbuttondef,	
								resources.redbuttonhover,	
								resources.redbuttonshadow]

		else:
			self.backgrounds = [resources.defaultbutton,	
								resources.hoverbutton,	
								resources.buttonshadow]

		self.bgdefault 			= pyglet.sprite.Sprite(self.backgrounds[0].get_region(0,0,width,height), x,y)
		self.bghover 			= pyglet.sprite.Sprite(self.backgrounds[1].get_region(0,0,width,height), x,y)
		self.bgshadow			= pyglet.sprite.Sprite(self.backgrounds[2].get_region(0,0,width,25), x,y-self.shadowoffset)
		
		#bg is the current color of the button
		self.bg = self.bgdefault

		self.xpos1			=	x
		self.ypos1			=	y
		self.bodyheight		= 	height
		self.bodywidth 		= 	width
		self.body = Label()


		if resources.want_font() == False:
			if text == 'Yes':
				width -=30
			if text == 'Info':
				width +=10
			if text == 'Change':
				width -= 40
			if text == 'Stop':
				width +=40
			if text == 'X':
				width += 30
			if text == '1' or text == '2' or text == '3':
				width +=20
			if text == 'BACK':
				width = width - 3
			self.body			=	Label(text, x = x+width/4, y = y + height/3, height = height, width = width)

		
		else:
			if text == "X":
				self.body			=	Label(text, x = x+22, y = y-5, height = height, width = width)

			else:
				if text == 'Yes':
					width = 0
				self.body			=	Label(text, x = x+width/xadjustment, y = y + height/yadjustment, height = height, width = width)
		self.body.font_size = fontsize


		self.body.font_name = "Minecraftia"
		self.execute		=	target


	def draw(self):
		self.bgshadow.draw()
		self.bg.draw()
		self.body.draw()

	def bind_left_click(self,x,y,button):
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1 <= y <= self.ypos1+self.bodyheight and button==mouse.LEFT:
			if self.pressed == False:
				self.bg.y = self.bg.y-(0.6*self.shadowoffset)
				self.body.y = self.body.y-(0.6*self.shadowoffset)
				self.pressed = True

	def bind_hover(self,x,y):
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1<= y <= self.ypos1+self.bodyheight:
			self.bg = self.bghover
		else:
			self.bg = self.bgdefault
			
	def bind_release(self,x,y,button):
		if self.pressed:
				self.onbutton = True
				self.bg.y = self.bg.y+(0.6*self.shadowoffset)
				self.body.y = self.body.y+(0.6*self.shadowoffset)
				self.pressed = False
		
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1 <= y <= self.ypos1+self.bodyheight:
			if button==mouse.LEFT and self.onbutton:
				self.execute()
				self.bg = self.bgdefault
			else:
				self.bg = self.bghover
		else:
			self.bg = self.bgdefault
		self.onbutton = False


class Button_with_hint:
	def __init__(self, x, y, shadowoffset, height, width, text,target,buttontype, fontsize,xadjustment,yadjustment):
		self.shadowoffset = shadowoffset
		self.pressed = False
		self.backgrounds = [resources.defaultbutton,	
								resources.hoverbutton,	
								resources.buttonshadow]

		self.bgdefault 			= pyglet.sprite.Sprite(self.backgrounds[0].get_region(0,0,width,height), x,y)
		self.bghover 			= pyglet.sprite.Sprite(self.backgrounds[1].get_region(0,0,width,height), x,y)
		self.bgshadow			= pyglet.sprite.Sprite(self.backgrounds[2].get_region(0,0,width,25), x,y-self.shadowoffset)
		
		#bg is the current color of the button
		self.bg = self.bgdefault

		self.xpos1			=	x
		self.ypos1			=	y
		self.bodyheight		= 	height
		self.bodywidth 		= 	width
		self.body = Label()


		if resources.want_font() == False:
			self.body			=	Label(text, x = x+width/4, y = y + height/3, height = height, width = width)
		else:
			self.body			=	Label(text, x = x+width/xadjustment, y = y + height/yadjustment, height = height, width = width)

		self.body.font_size = fontsize
		self.body.font_name = "Minecraftia"
		self.execute		=	target

		self.show_hoverbox = False
		self.fastmode_hint = ['For small files only. <256MB','Uses more memory','May hang with large files']
		self.slowmode_hint = ['For large files','Less memory used','Good for multi-tasking']
		self.hint_list = []
		if text == 'Small':
			self.hint_list = self.fastmode_hint
		else:
			self.hint_list = self.slowmode_hint

		self.mouse_x = 0
		self.mouse_y = 0
		self.onbutton = False

	def draw(self):
		self.bgshadow.draw()
		self.bg.draw()
		self.body.draw()
		if self.show_hoverbox:
			pyglet.sprite.Sprite(resources.statusimage.get_region(0,0,300,100),self.mouse_x-300,self.mouse_y-100).draw()
			line1 = Label(text = self.hint_list[0], x = self.mouse_x-290, y = self.mouse_y-105+75)
			line2 = Label(text = self.hint_list[1], x = self.mouse_x-290, y = self.mouse_y-105+45)
			line3 = Label(text = self.hint_list[2], x = self.mouse_x-290, y = self.mouse_y-105+15)
			line1.font_name = "Minecraftia"
			line2.font_name = "Minecraftia"
			line3.font_name = "Minecraftia"
			line1.draw()
			line2.draw()
			line3.draw()


	def bind_left_click(self,x,y,button):
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1 <= y <= self.ypos1+self.bodyheight and button==mouse.LEFT:
			if self.pressed == False:
				self.bg.y = self.bg.y-(0.6*self.shadowoffset)
				self.body.y = self.body.y-(0.6*self.shadowoffset)
				self.pressed = True
				self.show_hoverbox = False

	def bind_hover(self,x,y):
		self.mouse_x = x
		self.mouse_y = y
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1<= y <= self.ypos1+self.bodyheight:
			self.show_hoverbox = True
			
			self.bg = self.bghover
		else:
			self.bg = self.bgdefault
			self.show_hoverbox = False
			
	def bind_release(self,x,y,button):
		if self.pressed:
				self.onbutton = True
				self.bg.y = self.bg.y+(0.6*self.shadowoffset)
				self.body.y = self.body.y+(0.6*self.shadowoffset)
				self.pressed = False
		
		if self.xpos1<=x<=self.xpos1+self.bodywidth and self.ypos1 <= y <= self.ypos1+self.bodyheight:
			if button==mouse.LEFT and self.onbutton:
				self.execute()
				self.bg = self.bgdefault
			else:
				self.bg = self.bghover
		else:
			self.bg = self.bgdefault
		self.onbutton = False