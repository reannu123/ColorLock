from _thread            import start_new_thread 
import pyglet
import resources
from TextWidget         import TextWidget
from Button             import Button
from Button             import Button_with_hint
from pyglet.window      import Window
from pyglet.text        import Label
from pyglet.graphics    import Batch
from encryptor          import Encryptor
from grid               import Grid



class App(Window):
    def __init__(self):
        Window.__init__(self,width = 550, height = 650, caption = "ColorLock")
        pyglet.gl.glClearColor(.7, .7, .7, 1) 


        #Menu States - What screen will be shown
        self.mainmenu = True
        self.decryptmenu = False
        self.encryptmenu = False


        self.focused = None
        self.text_cursor = self.get_system_mouse_cursor('text')




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#                                   Draw Elements

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #                              Font Prompt
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.disconnected = False
        # Checks if the user has been prompted to use a font or not, if the font is present, and if the user wants to use the font or not
        self.prompted = resources.is_prompted()
        self.fontpreference = resources.want_font()
        self.fontexists = resources.is_font_present()


        #the texts for prompting font installation, different positions for different situations (diff font)
        self.fontprompttext = [
            ['Welcome to',                                              '700','24'],    
            ['ColorLock!',                                              '650','24'],     
            ['This program will look better with the' ,                 '580','18'],    
            ['Minecraftia Font by Andrew Tyler.',                       '540','18'],   
            ['Would you like to download it?',                          '470','18'],
            ['If yes, make sure that you are connected',                '400','18'],
            ['to the Internet.',                                        '360','18']]   

        self.fontprompttext2 = [
            ['Welcome to',                                              '700','24'],    
            ['ColorLock!',                                              '650','24'],     
            ['Minecraftia font not found.',                             '580','18'],
            ['This program will look better with the' ,                 '510','18'],    
            ['Minecraftia Font by Andrew Tyler.',                       '470','18'],   
            ['Would you like to download it again?',                    '400','18'],
            ['If yes, make sure that you are',                          '360','18'],
            ['connected to the Internet.',                              '320','18']]   

        self.fontprompttext3 = [
            ['Welcome to',                                              '700','24'],    
            ['ColorLock!',                                              '650','24'],     
            ['Minecraftia font already exists.',                        '580','18'],
            ['This program will look better with the' ,                 '510','18'],    
            ['Minecraftia Font by Andrew Tyler.',                       '470','18'],   
            ['Would you like to use it?',                               '400','18']]  

        self.fontprompttext_nointernet = [
            ['Welcome to',                                              '700','24'],    
            ['ColorLock!',                                              '650','24'],     

            ['This program will look better with the' ,                 '580','18'],    
            ['Minecraftia Font by Andrew Tyler.',                       '540','18'],     

            ['You are not connected to the Internet',                   '470','18'],
            ['Would you still like to try again?',                      '400','18']]   

        
        
        #Changes the font promp texts depending on the font
        if self.fontexists == False and self.fontpreference and self.prompted:
            self.prompted = False
            self.fontprompttext = self.fontprompttext2

        if self.fontexists and self.prompted == False:
            self.fontprompttext = self.fontprompttext3
        


        # Loads the background image for the promptscreen (same as the information screen background)
        self.fontpromptscreen = resources.infoimagesprite 
        
        self.fontpromptyesbutton = Button(
                                text = "Yes",
                                x = 150,
                                y = 50,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.call_download,
                                buttontype = 'change',
                                fontsize = 18,
                                xadjustment = 1,
                                yadjustment = 4
                            )

        self.fontpromptnobutton = Button(
                                text = "No",
                                x = 350,
                                y = 50,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.call_notdownload ,
                                buttontype = 'MMdecrypt',
                                fontsize = 18,
                                xadjustment = 3.8,
                                yadjustment = 4
                            )

        # if the user wants to use the font, then the program will load the font
        if self.fontpreference:
            resources.loadfont()
        

        # Loads all the elements on the screen regardless of font preference
        self.load_all()






                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #                                Main Menu
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def load_all(self):
    	# Title screen
        self.MMscreen = resources.screenimagesprite
        self.MMscreentext = resources.screentextsprite        #Main Menu Title Screen
        
        # Decorations
        self.MMyled = resources.yellowled
        self.MMgled = resources.greenled

        
        self.encryptbutton = Button(
                                text = "Encrypt",
                                x = 50,
                                y = 150,
                                height = 100,
                                width = 200,
                                shadowoffset = 25,
                                target = self.encrypt_screen,
                                buttontype = 'MMencrypt',
                                fontsize = 20,
                                xadjustment = 5.5,
                                yadjustment = 5.5,
                            )
       
        self.decryptbutton = Button(
                                text = "Decrypt",
                                x = 300,
                                y = 150,
                                height = 100,
                                width = 200,
                                shadowoffset = 25,
                                target = self.decrypt_screen,
                                buttontype = 'MMdecrypt',
                                fontsize = 20,
                                yadjustment = 5.5,
                                xadjustment = 5.5
                            )

        self.MMinfobutton = Button(
                                text = "Info",
                                x = 245,
                                y = 40,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.show_infoscreen,
                                buttontype = '',
                                fontsize = 10,
                                xadjustment = 5,
                                yadjustment = 6.8
                            )
        









                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #                       Encrypt and Decrypt Menu 
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Fast or Slow Encryption
        self.fast_encrypt = True

    #       Buttons
        self.grid_unlocked = False 					 # the grid is initially locked until the user presses the "Change" button
        self.enable_buttons = True            	     #will turn false if the user has successfully crypted a file to avoid excessive presses

        self.EDbuttonlist = list()
        self.EDBackButton = Button(
                                text = "BACK",
                                x = 405,
                                y = 45,
                                height = 80,
                                width = 125,
                                shadowoffset = 15,
                                target = self.mainmenu_screen,
                                buttontype = 'MMencrypt',
                                fontsize = 17,
                                xadjustment = 4.3,
                                yadjustment = 6.8
                            )
        self.EDBackButton2 = Button(
                                text = "BACK",
                                x = 405,
                                y = 45,
                                height = 80,
                                width = 125,
                                shadowoffset = 15,
                                target = self.mainmenu_screen,
                                buttontype = 'MMdecrypt',
                                fontsize = 17,
                                xadjustment = 4.3,
                                yadjustment = 6.8
                            )

        self.EDchange_pattern = Button(
                                text = "Change",
                                x = 210,
                                y = 290,
                                height = 50,
                                width = 150,
                                shadowoffset = 15,
                                target = self.EDchange_patternState,
                                buttontype = 'change',
                                fontsize = 20,
                                xadjustment =8,
                                yadjustment = 1100
                            )

        self.EDchange_pattern2 = Button(
                                text = "Stop",
                                x = 210,
                                y = 290,
                                height = 50,
                                width = 150,
                                shadowoffset = 15,
                                target = self.EDchange_patternState,
                                buttontype = 'changed',
                                fontsize = 20,
                                xadjustment = 4,
                                yadjustment = 1100
                            )
        
        self.EDchange_mode_button = Button_with_hint(
                                text = "Small",
                                x = 405,
                                y = 290,
                                height = 50,
                                width = 125,
                                shadowoffset = 15,
                                target = self.EDchange_mode,
                                buttontype = '',
                                fontsize = 20,
                                xadjustment =5,
                                yadjustment = 1100
                            )

        self.EDchange_mode_button2 = Button_with_hint(
                                text = "Large",
                                x = 405,
                                y = 290,
                                height = 50,
                                width = 125,
                                shadowoffset = 15,
                                target = self.EDchange_mode,
                                buttontype = '',
                                fontsize = 20,
                                xadjustment = 9,
                                yadjustment = 1100
                            )

        self.EDstart_encrypt_button = Button(
                                    text = "Start",
                                    x = 405,
                                    y = 160,
                                    height = 100,
                                    width = 125,
                                    shadowoffset = 15,
                                    target = self.EDcryptpress,
                                    buttontype = 'MMencrypt',
                                    fontsize = 20,
                                    xadjustment = 6,
                                    yadjustment = 5
                                )
        self.EDstart_decrypt_button = Button(
                                    text = "Start",
                                    x = 405,
                                    y = 160,
                                    height = 100,
                                    width = 125,
                                    shadowoffset = 15,
                                    target = self.EDcryptpress,
                                    buttontype = 'MMdecrypt',
                                    fontsize = 20,
                                    xadjustment = 6,
                                    yadjustment = 5
                                )
        self.EDbuttonlist.append(self.EDBackButton)
        self.EDbuttonlist.append(self.EDBackButton2)
        self.EDbuttonlist.append(self.EDchange_pattern)
        self.EDbuttonlist.append(self.EDchange_pattern2)
        self.EDbuttonlist.append(self.EDchange_mode_button2)
        self.EDbuttonlist.append(self.EDchange_mode_button)

        #Text Boxes
        self.textbatch = Batch()
        self.textboxes = list()
        self.outputfilebox = TextWidget(
                                text = '', 
                                x = 30, 
                                y = 145, 
                                width = 350, 
                                height = 40,
                                batch = self.textbatch
                            )
        self.inputfilebox = TextWidget(
                                text = '', 
                                x = 30, 
                                y = 220, 
                                width = 350, 
                                height = 40,
                                batch = self.textbatch
                            )

        self.textboxes.append(self.outputfilebox)
        self.textboxes.append(self.inputfilebox)


        #Grid
        self.grid = None

        # Creates different font adjustments that change the positions of texts on the screen depending on the font preferred
        if self.fontpreference == False:
            self.fontadjustment = 20
        else:
            self.fontadjustment =0

        #Labels
        self.inputlabel = Label(text = 'Input filename', x = 30, y = self.fontadjustment+255)
        self.inputlabel.font_name = "Minecraftia"
        self.inputlabel.font_size = 14

        self.outputlabel = Label(text = "Output filename", x = 30, y = self.fontadjustment+177)
        self.outputlabel.font_name = "Minecraftia"
        self.outputlabel.font_size = 14









        
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #                               Information Menu
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #Initially hides the information menu
        self.showinformation = False
        self.infopage1 = True
        self.infopage2 = False
        self.infopage3 = False

        self.infoscreen = resources.infoimagesprite 

        self.exitinfobutton = Button(
                                text = "X",
                                x = 450,
                                y = 560,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.hide_infoscreen,
                                buttontype = 'MMdecrypt',
                                fontsize = 20,
                                xadjustment = 5,
                                yadjustment = 10
                            )
        
        self.infopage1button = Button(
                                text = "1",
                                x = 40,
                                y = 50,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.changepage1,
                                buttontype = 'MMencrypt',
                                fontsize = 18,
                                xadjustment = 2.5,
                                yadjustment = 20
                            )
        self.infopage2button = Button(
                                text = "2",
                                x = 120,
                                y = 50,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.changepage2,
                                buttontype = 'MMencrypt',
                                fontsize = 18,
                                xadjustment = 2.5,
                                yadjustment = 20
                            )
        self.infopage3button = Button(
                                text = "3",
                                x = 200,
                                y = 50,
                                height = 50,
                                width = 60,
                                shadowoffset = 10,
                                target = self.changepage3,
                                buttontype = 'MMencrypt',
                                fontsize = 18,
                                xadjustment = 2.7,
                                yadjustment = 20
                            )
        
        # Different pages of the information menu
        self.information_texts1 = [
            [(20-int(self.fontadjustment*0.4))*' '+'                                          Page 1',  '195','18'],
            ['Welcome to',                                                                              '700','24'],   
            ['ColorLock!',                                                                              '650','24'],     

            ['An encrypting program that uses' ,                                                        '580','18'],   
            ['color patterns as keys.',                                                                 '540','18'],     

            ['This program XOR\'s each bit of',                                                         '470','18'],    
            ['a file to the key generated by',                                                          '430','18'],    
            ['the color pattern.',                                                                      '390','18']]     


        self.information_texts2 = [
            [(20-int(self.fontadjustment*0.4))*' '+'                                          Page 2',  '195','18'],
            ['How to use',                                                                              '700','24'],    #0
            ['ColorLock:',                                                                              '650','24'],     #1
            ['1. Place file in the INPUT folder.' ,                                                     '580','18'],    #2
            ['2. Input file name in the textbox.',                                                      '530','18'],     #3

            ['3. Create a color pattern.',                                                              '480','18'],     #4
            ['4. Choose if it is a large or a',                                                         '430','18'],     #5
            ['     small file.',                                                                        '380','18'],
            ['5. Type the output file name.',                                                           '330','18'],
            ['6. Push start and wait until done.',                                                      '280','18']]     #14	 


        self.information_texts3 = [
            [(20-int(self.fontadjustment*0.4))*' '+'                                          Page 3',  '195','18'],
            ['NOTE:',                                                                                   '700','24'],  
            ['',                                                                                        '650','24'],  
            ['1. Encrypting a file that\'s ',                                                           '600','18'],    
            ['     already encrypted just',                                                             '560','18'],    
            ['     decrypts it and vice versa.',                                                        '520','18'],  
            ['2. A file encrypted using \'Small\'',                                                     '460','18'],
            ['     mode cannot be decrypted via ',                                                      '420','18'],
            ['     \'Large\' mode and vice versa.',                                                     '380','18'],
            ['',                                                                                        '260','18']]    	 










        
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #                               Status Screen
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #Status Screen Background

        self.EDscreen = resources.statusimagesprite                     #status screen background

        #~~~~~~Status Screen Labels~~~~~~~~~

        self.status_texts = [
            ['Output field blank!',                        '100','18'],    #0
            ['Input field blank!',                          '50','18'],     #1
            ['Error: File not found!',                     '100','18'],     #2
            ['Make sure to include file extension',         '75','12'],     #3
            ['if it has one.',                              '50','12'],     #4
            ['Encrypting . . .',                            '55','20'],     #5
            ['Finished!',                                   '90','24'],     #6
            ['Please press \'Back\'        ---->',          '50','18'],     #7
            ['Input and Output are the Same!',              '90','14'],     #8
            ['We should not risk overwriting the file.',    '70','11'],     #9
            ['Welcome!',                                   '100','24'],    #10
            ['Press \'Change\' to change pattern.',         '75','12'],     #11
            ['Press \'Stop\' if you are satisfied',        '100','13'],    #12
            ['with the pattern.',                           '65','13'],     #13
            ['Press \'Start\' after.',                      '45','12'],
            ['Decrypting . . .',                            '55','20']]     #14		

        self.status_texts2 = [
            ['Input field blank!',                          '73','18'],    #0
            ['Output field blank!',                         '33','18'],     #1
            ['Error: File not found!',                      '80','18'],     #2
            ['Make sure to include file extension',         '60','12'],     #3
            ['if it has one.',                              '35','12'],     #4
            ['Encrypting . . .',                            '70','20'],     #5
            ['Finished!',                                   '80','18'],     #6
            ['Please press \'Back\'        ---->',          '50','14'],     #7
            ['Input and Output are the Same!',              '90','14'],     #8
            ['We should not risk overwriting the file.',    '70','11'],     #9
            ['Welcome!',                                    '80','18'],    #10
            ['Press \'Change\' to change pattern.',         '55','12'],     #11
            ['Press \'Stop\' if you are satisfied',         '80','13'],    #12
            ['with the pattern.',                           '50','13'],     #13
            ['Press \'Start\' after.',                      '30','12'],     #14
            ['Decrypting . . .',                            '70','20']]     #15	

        #Boolean values to determine the status in the status bar
        
        self.entry =                True                #Welcome text in the status bar
        self.encrypting =           False               #Status: Encrypting
        self.finish =               False               #Status: Finished
        self.inputerror =           False               #catch empty input textbox
        self.filenotfounderror =    False               #catch file not found
        self.outputerror =          False               #catch empty output textbox
        self.ready_encrypt =        False               #Boolean value to load the encryptor
        self.ready_encrypt2 =       False
        self.errorsamefilename =    False
    
        



























    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #                                   EVENTS


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def on_draw(self):


        self.clear()    
        
        #Main Menu Draw
        if self.mainmenu:
            self.MMscreen.draw()
            self.MMscreentext.draw()
            self.MMyled.draw()
            self.MMgled.draw()
            self.encryptbutton.draw()
            self.decryptbutton.draw()
            self.MMinfobutton.draw()

        #ED Menu Draw
        elif self.mainmenu == False:
            #buttons
            
            
            #text boxes
            for i in self.textboxes:
                i.draw()
            self.textbatch.draw()
            self.inputlabel.draw()
            self.outputlabel.draw()
            self.EDscreen.draw()
            
            #draws the grid
            self.grid.draw()

            #Status Screen Labels
            if self.outputerror:
                self.Show_Status_Label(1).draw()
                
            if self.inputerror:
                self.Show_Status_Label(0).draw()
            
            if self.filenotfounderror:
                self.Show_Status_Label(2).draw()
                self.Show_Status_Label(3).draw()
                self.Show_Status_Label(4).draw()

            if self.encrypting:
                if self.encryptmenu:
                    self.Show_Status_Label(5).draw()
                elif self.decryptmenu:
                    self.Show_Status_Label(15).draw()

            if self.finish:
                self.Show_Status_Label(6).draw()
                self.Show_Status_Label(7).draw()

            if self.entry:
                self.Show_Status_Label(10).draw()
                self.Show_Status_Label(11).draw()
                self.Show_Status_Label(14).draw()
            
            if self.grid_unlocked:
                self.Show_Status_Label(12).draw()
                self.Show_Status_Label(13).draw()


            if self.encryptmenu:
                self.EDstart_encrypt_button.draw()
            elif self.decryptmenu:
                self.EDstart_decrypt_button.draw()

            for i in self.EDbuttonlist:
                if i is self.EDchange_pattern or i is self.EDchange_pattern2:
                    if self.grid_unlocked:
                        self.EDchange_pattern2.draw()
                    else:
                        self.EDchange_pattern.draw()
                elif i != self.EDchange_mode_button and i != self.EDchange_mode_button2:
                    if i is self.EDBackButton or i is self.EDBackButton2:
                        if self.encryptmenu:
                            self.EDBackButton2.draw()
                        else:
                            self.EDBackButton.draw()
                    else: 
                        i.draw()
                else:
                    if self.fast_encrypt:
                        self.EDchange_mode_button.draw()
                    else:
                        self.EDchange_mode_button2.draw()

        if self.showinformation:
            self.infoscreen.draw()
            self.exitinfobutton.draw()
            self.infopage1button.draw()
            self.infopage2button.draw()
            self.infopage3button.draw()

            if self.infopage1:
                for i in range(len(self.information_texts1)):
                    self.Show_Information_Label(i, self.information_texts1).draw()

            elif self.infopage2:
                for i in range(len(self.information_texts2)):
                    self.Show_Information_Label(i, self.information_texts2).draw()

            elif self.infopage3:
                for i in range(len(self.information_texts3)):
                    self.Show_Information_Label(i, self.information_texts3).draw()
        
        if self.prompted == False:
            self.fontpromptscreen.draw()
            self.fontpromptnobutton.draw()
            self.fontpromptyesbutton.draw()

            if self.disconnected:
                prompttexts = self.fontprompttext_nointernet
            else:
                prompttexts = self.fontprompttext

            for i in range(len(prompttexts)):
                    self.Show_Information_Label(i, prompttexts).draw()
            #Show font prompt


        

    ###             Mouse Events
    def on_mouse_press(self,x,y,button,modifiers):
        if self.prompted:
            if self.mainmenu:
                self.MMinfobutton.bind_left_click(x,y,button)
                self.encryptbutton.bind_left_click(x,y,button)
                self.decryptbutton.bind_left_click(x,y,button)

            else:
                if self.grid_unlocked == False and self.enable_buttons:

                    for i in self.EDbuttonlist:
                        if i is self.EDchange_pattern or i is self.EDchange_pattern2:
                            self.EDchange_pattern.bind_left_click(x,y,button)
                        elif i is self.EDchange_mode_button or i is self.EDchange_mode_button2:
                            if self.fast_encrypt:
                                self.EDchange_mode_button.bind_left_click(x,y,button)
                            else:
                                self.EDchange_mode_button2.bind_left_click(x,y,button)
                        else:
                            i.bind_left_click(x,y,button)
                    i = 0
                    while i < len(self.textboxes):
                        activebox = self.textboxes[i]
                        if activebox.check_hover(x,y):
                            self.set_focus(activebox)
                            activebox.mouse_press(x,y,button,modifiers,self.focused)
                            break
                        else:
                            self.set_focus(None)
                        i+=1

                    if self.decryptmenu:
                        self.EDstart_decrypt_button.bind_left_click(x,y,button)
                    elif self.encryptmenu:
                        self.EDstart_encrypt_button.bind_left_click(x,y,button)

                elif self.grid_unlocked == False and self.enable_buttons == False and self.encrypting == False:
                    self.EDBackButton.bind_left_click(x,y,button)
                    self.EDBackButton2.bind_left_click(x,y,button)

                elif self.grid_unlocked == True and self.enable_buttons and self.encrypting == False:
                    self.EDchange_pattern2.bind_left_click(x,y,button)
                    self.grid.on_click(x,y,button)

            if self.showinformation:
                self.exitinfobutton.bind_left_click(x,y,button)
                self.infopage1button.bind_left_click(x,y,button)
                self.infopage2button.bind_left_click(x,y,button)
                self.infopage3button.bind_left_click(x,y,button)
        else:
            self.fontpromptyesbutton.bind_left_click(x,y,button)
            self.fontpromptnobutton.bind_left_click(x,y,button)


    def on_mouse_motion(self,x,y,dx,dy):
        if self.prompted:
            if self.mainmenu:
                self.encryptbutton.bind_hover(x,y)
                self.decryptbutton.bind_hover(x,y)
                self.MMinfobutton.bind_hover(x,y)

            else:
                if self.grid_unlocked == False and self.enable_buttons:

                    for i in self.EDbuttonlist:
                        if i is self.EDchange_pattern or i is self.EDchange_pattern2:
                            if self.grid_unlocked == False:
                                self.EDchange_pattern.bind_hover(x,y)

                        elif i is self.EDchange_mode_button or i is self.EDchange_mode_button2:
                            if self.fast_encrypt:
                                self.EDchange_mode_button.bind_hover(x,y)
                            else:
                                self.EDchange_mode_button2.bind_hover(x,y)
                        else:
                            i.bind_hover(x,y)


                    if self.inputfilebox.check_hover(x,y) or self.outputfilebox.check_hover(x,y):
                        self.set_mouse_cursor(self.text_cursor)
                    else:
                        self.set_mouse_cursor(None)

                    if self.decryptmenu:
                        self.EDstart_decrypt_button.bind_hover(x,y)
                    elif self.encryptmenu:
                        self.EDstart_encrypt_button.bind_hover(x,y)

                elif self.grid_unlocked == False and self.enable_buttons == False and self.encrypting == False:
                    self.EDBackButton.bind_hover(x,y)
                    self.EDBackButton2.bind_hover(x,y)

                else:
                    self.EDchange_pattern2.bind_hover(x,y)
                            

            if self.showinformation:
                self.exitinfobutton.bind_hover(x,y)
                self.infopage1button.bind_hover(x,y)
                self.infopage2button.bind_hover(x,y)
                self.infopage3button.bind_hover(x,y)
        else:
            self.fontpromptyesbutton.bind_hover(x,y)
            self.fontpromptnobutton.bind_hover(x,y)


    def on_mouse_release(self,x,y,button,modifiers):
        if self.prompted:
            if self.mainmenu:
                self.encryptbutton.bind_release(x,y,button)
                self.decryptbutton.bind_release(x,y,button)
                self.MMinfobutton.bind_release(x,y,button)
            else:
                if self.grid_unlocked == False and self.enable_buttons:
                    for i in self.EDbuttonlist:
                        if i is self.EDchange_pattern or i is self.EDchange_pattern2:
                            if self.grid_unlocked==False:
                                self.EDchange_pattern.bind_release(x,y,button)

                        elif i is self.EDchange_mode_button or i is self.EDchange_mode_button2:
                            if self.fast_encrypt:
                                self.EDchange_mode_button.bind_release(x,y,button)
                            else:
                                self.EDchange_mode_button2.bind_release(x,y,button)
                        else:
                            i.bind_release(x,y,button)
                    if self.decryptmenu:
                        self.EDstart_decrypt_button.bind_release(x,y,button)
                    elif self.encryptmenu:
                        self.EDstart_encrypt_button.bind_release(x,y,button)

                elif self.grid_unlocked == False and self.enable_buttons == False and self.encrypting == False:
                    self.EDBackButton.bind_release(x,y,button)
                    self.EDBackButton2.bind_release(x,y,button)

                else:
                    self.EDchange_pattern2.bind_release(x,y,button)

            if self.showinformation:
                self.exitinfobutton.bind_release(x,y,button)
                self.infopage1button.bind_release(x,y,button)
                self.infopage2button.bind_release(x,y,button)
                self.infopage3button.bind_release(x,y,button)
        else:
            self.fontpromptyesbutton.bind_release(x,y,button)
            self.fontpromptnobutton.bind_release(x,y,button)


    ###             Keyboard Events
    def on_text(self,text):
        for i in self.textboxes:
            i.ontext(text,self.focused)

    def on_text_motion(self,motion):
        for i in self.textboxes:
            i.istextmoving(motion,self.focused)

    def on_key_press(self,symbol, modifiers):
        if self.grid_unlocked:
            self.grid.on_key_press(symbol)





























    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #                                       Functions


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #When the Decrypt/Encrypt button is pressed in the encrypt/decrypt screen, not the main menu screen
    def EDcryptpress(self):
        self.entry = False
        self.outputerror = False
        self.inputerror = False
        self.filenotfounderror = False
        self.errorsamefilename = False
        self.infilename = self.passinputfilename()
        self.outfilename = self.passoutputfilename()
        
        if self.outfilename.strip() == '' and self.infilename.strip() =='':
            self.outputerror = True
            self.inputerror = True

        elif self.outfilename.strip() == '' and self.infilename.strip() != '':
            self.outputerror = True

        else:
            if self.infilename.strip() != '':
                try:
                    input_file = open('INPUT/'+self.infilename, "rb")                         #Will test first if the file exists
                    input_file.close()
                    self.enable_buttons = False
                    self.startencrypt(grid = self.grid, infilename = 'INPUT/'+ self.infilename, outfilename = 'OUTPUT/'+self.outfilename)
                    self.encrypting = True

                except:
                    self.filenotfounderror = True
            else:
                self.inputerror = True

        
    #Encryption starts when input and output are valid
    def startencrypt(self,grid,infilename,outfilename):
        encryptor = Encryptor(grid = grid, inputfile = infilename, outputfile = outfilename, target_when_done = self.finished_encrypting)
        if self.fast_encrypt==False:
            start_new_thread(encryptor.large_crypt,())
        else:
            start_new_thread(encryptor.crypt,())
        return


    #When there are no errors, the program passes the input filename to the encryptor
    def passinputfilename(self):
        infilename = self.inputfilebox.gettext()
        return infilename.strip()


    #When there are no errors, the program passes the output filename to the encryptor
    def passoutputfilename(self):
        outfilename = self.outputfilebox.gettext()
        return outfilename.strip()


    #When the change button is pressed, this locks/unlocks all the buttons and clickables on the screen
    def EDchange_patternState(self):
        self.grid.lastclicked = None
        if self.grid_unlocked:
            self.grid_unlocked = False
        else:
            self.grid_unlocked = True
        self.entry = False
        self.outputerror = False
        self.inputerror = False
        self.filenotfounderror = False
        self.finish = False

    def EDchange_mode(self):
        if self.fast_encrypt:
            self.fast_encrypt = False
        else:
            self.fast_encrypt = True

    def finished_encrypting(self):
        self.encrypting = False
        self.finish = True
        resources.finish_encrypting_notif()





    #Functions for changing screens
    def encrypt_screen(self):
        self.mainmenu = False
        self.decryptmenu = False
        self.encryptmenu = True
        self.grid = Grid()
    
    def decrypt_screen(self):
        self.mainmenu = False
        self.encryptmenu = False
        self.decryptmenu = True
        self.grid = Grid()
    
    def mainmenu_screen(self):
        self.mainmenu = True
        self.encryptmenu = False
        self.decryptmenu = False
        self.outputfilebox.gettext()
        self.inputfilebox.gettext()

        #Resets values when going back to the mainmenu
        self.encrypting = False
        self.outputerror = False
        self.inputerror = False
        self.filenotfounderror = False
        self.finish = False
        self.enable_buttons = True
        self.entry = True



    #These functions are the toggle for the information screen
    def show_infoscreen(self):
        self.showinformation = True
    
    def hide_infoscreen(self):
        self.showinformation = False
        self.changepage1()

    def changepage1(self):
        self.infopage1 = True
        self.infopage2 = False
        self.infopage3 = False
        return

    def changepage2(self):
        self.infopage1 = False
        self.infopage2 = True
        self.infopage3 = False
        return

    def changepage3(self):
        self.infopage1 = False
        self.infopage2 = False
        self.infopage3 = True
        return

    def Show_Information_Label(self, index, list):
        newlabel = Label(text = list[index][0],
                            x = 40,
                            y = int(list[index][1])-150)
        if self.prompted:
            newlabel.font_name = 'Minecraftia'
            
        newlabel.color = (0,0,0,255)
        newlabel.anchor_x = 'left'
        newlabel.font_size = int(list[index][2])
        return newlabel
    
    

    #for text box focusing
    def set_focus(self,focus):               
        self.focused
        if self.focused == focus:
            return
        else:
            for i in self.textboxes:
                if i == self.focused:
                    i.caret.visible = False
                    i.caret.mark = i.caret.position = 0
            
            self.focused = focus
            for i in self.textboxes:
                if i == self.focused:
                    i.caret.visible = True



    #For creating labels on the Status Screen
    def Show_Status_Label(self, index):
        if self.fontpreference:
            self.status_texts = self.status_texts2
        newlabel = Label(text = self.status_texts[index][0],
                            x = 40,
                            y = int(self.status_texts[index][1]))

        newlabel.font_name = "Minecraftia"
        newlabel.anchor_x = 'left'
        newlabel.font_size = int(self.status_texts[index][2])
        return newlabel
    


    
    #for prompting font installation
    def hidefontprompt(self):
        self.prompted = True
        return

    def call_download(self):
        try:
            resources.downloadfont()
            self.fontpreference = True
            self.reload_all()
        except:
            self.disconnected = True

    def call_notdownload(self):
        resources.not_downloadfont()
        self.load_all()
        self.prompted = True


    def reload_all(self):
        resources.loadfont()
        self.load_all()
        self.on_draw()
        self.prompted = True


#Citations
#Syntax for multi-threading was adapted from https://www.tutorialspoint.com/python3/python_multithreading.htm