import pyglet
import urllib
from urllib import request
import zipfile
from pyglet.resource import image
import os


pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


#~~~~~~~~~~~~~~~~~~~~~~ Main Menu ~~~~~~~~~~~~~~~~~~~~~~~~~
screenimage = image("screen.png")
screenimagesprite = pyglet.sprite.Sprite(screenimage.get_region(0,0,475,300),37.5,310)

statusimage = image("statusscreen.png")
statusimagesprite = pyglet.sprite.Sprite(statusimage.get_region(0,0,350,100),30,30)

infoimage = image('textbg.png')
infoimagesprite = pyglet.sprite.Sprite(infoimage.get_region(0,0,510,610),20,20)

screentext = pyglet.image.load_animation('resources/titlescreen.gif')
screentextsprite = pyglet.sprite.Sprite(screentext,52,425)
encryptbuttondef = image("encryptdefault.png")
encryptbuttonhover = image("encrypthover.png")
encryptbuttonshadow = image("encryptshadow.png")

decryptbuttondef = image("decryptdefault.png")
decryptbuttonhover = image("decrypthover.png")
decryptbuttonshadow = image("decryptshadow.png")

#decoration

yellowled = pyglet.sprite.Sprite(image("defbutton.png").get_region(0,0,10,20),500,280)
greenled = pyglet.sprite.Sprite(image("green2shadow.png").get_region(0,0,10,20),480,280)

#grid buttons
redcell = image("Red.png")
bluecell = image("Blue.png")
greencell = image("Green.png")
cyancell = image("Cyan.png")
yellowcell = image("Yellow.png")
magentacell = image("Magenta.png")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




textbg = image("textbg.png")


#other buttons
greenbuttondef = image("greendefault.png")
greenbuttonhover = image("greenhover.png")
greenbuttonshadow = image("greenshadow.png")

green2buttondef = image("green2default.png")
green2buttonhover = image("green2hover.png")
green2buttonshadow = image("green2shadow.png")

redbuttondef = image("reddefault.png")
redbuttonhover = image("redhover.png")
redbuttonshadow = image("redshadow.png")

#Default Buttons
grayedbutton = image ("graybutton.png")
defaultbutton = image("defbutton.png")
hoverbutton = image("hoverbtn.png")
buttonshadow = image("shadow.png")

def finish_encrypting_notif():
    try:
        source = pyglet.media.load('resources/Ping2.wav', streaming = False)
        source.play()
    except:
        pass
        
#Font Functions
#Checks if the user has already been prompted before
def downloadfont():
    
    open('resources/yesfont', "wb")
    try:
        open('resources/nofont')
        os.remove('resources/nofont')
    except:
        pass

    open('resources/yesfont', "wb")
    if is_font_present():
        pass
    else:
        downloadMinecraftia()

def not_downloadfont():
    
    open('resources/nofont', "wb")
    try:
        open('resources/yesfont')
        os.remove('resources/yesfont')
    except:
        pass

def is_prompted():
    try:
        open('resources/yesfont')
        return True
    except:
        try:
            open('resources/nofont')
            return True
        except:
            return False

def want_font():
    try:
        open('resources/yesfont')
        return True
    except:
        return False

def is_font_present():
    try:
        open('resources/Minecraftia-Regular.ttf', "rb")
        return True

    except:
        return False

#Downloads and extracts font
def downloadMinecraftia():
    url = 'https://dl.dafont.com/dl/?f=minecraftia'
    urllib.request.urlretrieve(url, 'resources/Minecraftia.zip')

    with zipfile.ZipFile("resources/Minecraftia.zip","r") as zip_ref:
        zip_ref.extractall("resources/")
    os.remove('resources/Minecraftia.zip')
    os.remove('resources/sample.png')
    os.remove('resources/readme.txt')


#Load font
def loadfont():
    try:
        pyglet.font.add_file('resources/Minecraftia-Regular.ttf')
        minecraftia = pyglet.font.load('Minecraftia')
    except:
        pass

    


# Citations and Licenses

# Minecraftia font was created by Andrew Tyler. The download URL is 'https://dl.dafont.com/dl/?f=minecraftia'
# Minecraftia is free for personal use 
# This program does not include the Minecraftia font
# It downloads the font under the discretion of the user. 

# The font file in this archive was created by Andrew Tyler www.AndrewTyler.net and font@andrewtyler.net
# Use at 12 or 24 px size with anti-alising off for best results.

# Note of the author
# Free for personal use.
# For commercial use, including apps, a commercial licence is required.

# Purchase Minecraftia commercial licence at https://sellfy.com/p/S0VS/
# Upon payment of the nonrefundable license fee, AndrewTyler.net grants you a nonexclusive, nontransferable, 
# limited right to use the Font Software according to the EULA found at andrewtyler.net/fonts




# GIF was made using an online GIF maker with URL https://ezgif.com/maker
# Ezgif.com is a free, simple to use toolset designed primarily for creating and editing animated GIFs, 
# but we also support editing and can perform conversions for many other image formats, including animated WebP, 
# PNG, MNG and FLIF, as well as some basic video editing. Our most popular online tools are GIF maker, Video to GIF 
# converter and image resizer.




# The logo in the GIF was made using Textcraft.net
# Copyright / License
# You're free to do as you please with text or logos created on the site without any compensation or obligations to us - you don't need to ask us for permission to use them in personal or commercial projects.
# If you're making text for a Minecraft related project, you might want to also have a look at Mojang's brand guidelines. Note: We have no connection to Mojang and can't advise on their guidelines.
# Font and texture resources used by the site are credited on at the bottom of the front page and on the font download page.
# As far as we are aware, at the time they were added to Textcraft, these were all made available through public domain or similar unrestricted licenses.
# Note that font licenses may change in newer versions of any particular font - check the attribution links on the font download page for more information.
# All other aspects of this site not sourced from 3rd parties are © 2019 textcraft.net.




#The syntax for reading and writing binary files was taken from https://www.tutorialsteacher.com/python/python-read-write-file
#Use of the urllib library is based on https://docs.python.org/3/library/urllib.request.html#module-urllib.request
#While the syntax for downloading files was taken from https://stackabuse.com/download-files-with-python/
#Use of the zipfile library is based on the documentation found at https://docs.python.org/3/library/zipfile.html
#Use of the pyglet resource class is based on the documentation found at https://pyglet.readthedocs.io/en/stable/modules/resource.html
#Use of the python os library is based on the documentation found at https://docs.python.org/2/library/os.html




# glass_ping-Go445-1207030150.wav was retrieved from http://soundbible.com/2084-Glass-Ping.html
# glass_ping-Go445-1207030150.wav was recorded by Go445
# Recorded using zoom h4n by hitting a large wine glass with a butter knife. Processed in reaper.
# Creative Commons Attribution-NonCommercial 3.0 License