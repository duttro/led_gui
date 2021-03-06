## 021715 class LED_TAB moved into file LED_TAB.py
## 030115 updated file references to support new file structure, added initialdir=('../led_data_files/'),
## 080115 LED matrix commands will use ether port 80



import pdb
import time
import serial
import socket
import string
import threading
import Queue
from PIL import Image, ImageDraw, ImageFont
from tkColorChooser import askcolor

import Tkdnd
from Tkinter import *
import Tkinter
import Tkinter, tkFileDialog, Dialog

import ttk
from ScrolledText import ScrolledText
from Dialog import Entry

############
## my classes
from DraggedDnd import *
from CanvasDnd import *
from LED_TAB import *
from Timeline_TAB import *


class LED_TAB(object):
    # List of coordinates to draw squares in the GIF file
    box_coord_vh = [[0 for x in xrange(8)] for x in xrange(8)]
    box_coord_vh = [\
                   ( 4, 4,12,12),(16, 4,24,12),(28, 4,36,12),(40, 4,48,12),(52, 4,60,12),(64, 4,72,12),(76, 4,84,12),(88, 4,96,12),\
                   ( 4,16,12,24),(16,16,24,24),(28,16,36,24),(40,16,48,24),(52,16,60,24),(64,16,72,24),(76,16,84,24),(88,16,96,24),\
                   ( 4,28,12,36),(16,28,24,36),(28,28,36,36),(40,28,48,36),(52,28,60,36),(64,28,72,36),(76,28,84,36),(88,28,96,36),\
                   ( 4,40,12,48),(16,40,24,48),(28,40,36,48),(40,40,48,48),(52,40,60,48),(64,40,72,48),(76,40,84,48),(88,40,96,48),\
                   ( 4,52,12,60),(16,52,24,60),(28,52,36,60),(40,52,48,60),(52,52,60,60),(64,52,72,60),(76,52,84,60),(88,52,96,60),\
                   ( 4,64,12,72),(16,64,24,72),(28,64,36,72),(40,64,48,72),(52,64,60,72),(64,64,72,72),(76,64,84,72),(88,64,96,72),\
                   ( 4,76,12,84),(16,76,24,84),(28,76,36,84),(40,76,48,84),(52,76,60,84),(64,76,72,84),(76,76,84,84),(88,76,96,84),\
                   ( 4,88,12,96),(16,88,24,96),(28,88,36,96),(40,88,48,96),(52,88,60,96),(64,88,72,96),(76,88,84,96),(88,88,96,96)]
            

    
    def __init__(self,win, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b):

        
##        #Tkinter.Tk.__init__(self)
##        ####win.title('Test')
##
##        # make the top right close button minimize (iconify) the main window
##        win.protocol("WM_DELETE_WINDOW", win.iconify)
##        ###win.protocol("WM_DELETE_WINDOW", lambda e: self.kill_it_all(win))
##        
##        # make Esc exit the program
##        ###win.bind('<Escape>', lambda e: kill_it_all(win))
##        win.bind('<Escape>', lambda e: self.kill_it_all(win))
##
##        # create a menu bar with an Exit command
##        menubar = Tkinter.Menu(win)
##        filemenu = Tkinter.Menu(menubar, tearoff=0)
##        filemenu.add_command(label="Exit", command=win.destroy)
##        menubar.add_cascade(label="File", menu=filemenu)
##        win.config(menu=menubar)
##
##        # create a Text widget with a Scrollbar attached
##        txt = ScrolledText(win, undo=True)
##        txt['font'] = ('consolas', '12')

        ##############################################################3
        print"GUI init"
        self.image0 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image1 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image2 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image3 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image4 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image5 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image6 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        self.image7 = Tkinter.PhotoImage(file = "../led_data_files/led_array_empty.gif")
        
        self.color0 = '#ff0000'
        self.color1 = '#00ff00'
        self.color2 = '#0000ff'
        self.color3 = '#000000'
        self.color4 = '#ffffff'
        self.color5 = '#ffffff'
        self.color6 = '#ffffff'
        self.color7 = '#ffffff'
        self.selected_color = '#ffffff'
    
        self.q1 = tx_queue1a
        self.q2 = tx_queue1b
        self.q3 = tx_queue2a
        self.q4 = tx_queue2b
        
        self.myFormats = [
          ('CompuServer GIF','*.gif'),
          ]

        
        self.bigMatrix = self.clear_colorArray()
        
        # create holding buffer for all items on the doodle screen, also initialized to 0
        self.b0 = bytearray(192)
        self.b1 = bytearray(192)
        self.b2 = bytearray(192)
        self.b3 = bytearray(192)
        self.b4 = bytearray(192)
        self.b5 = bytearray(192)
        self.b6 = bytearray(192)
        self.b7 = bytearray(192)
        #######################################
        # Set up the GUI                      #
        #######################################
        # TOP row of buttons
        self.button_selected_color = Tkinter.Button(win, text = "Selected Color", bg='white')
        self.button_selected_color.grid(row=0,column=7)
        
        self.button_clear_colors = Tkinter.Button(win, text = "Clear LEDs", bg='white', command = self.cb_clear_colors)
        self.button_clear_colors.grid(row=0,column=6)

        #######################################     
        self.button_Load0 = Tkinter.Button(win, text = "Load 0", command = self.cb_Load0, compound="left")
        self.button_Load0.grid(row=1, column=0)
        self.button_image0 = Tkinter.Button(win, image = self.image0, command = self.cb_image0)
        self.button_image0.grid(row=1, column=1)
        self.button_Store0 = Tkinter.Button(win, text = "Store 0", command = self.cb_Store0)
        self.button_Store0.grid(row=1, column=2)
      
    
        self.button_LED00  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,0", command = self.cb_led00 )
        self.button_LED00.grid(row=1, column=3)
        self.button_LED01  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,1", command = self.cb_led01 )
        self.button_LED01.grid(row=1, column=4)
        self.button_LED02  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,2", command = self.cb_led02 )
        self.button_LED02.grid(row=1, column=5)
        self.button_LED03  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,3", command = self.cb_led03 )
        self.button_LED03.grid(row=1, column=6)
        self.button_LED04  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,4", command = self.cb_led04 )
        self.button_LED04.grid(row=1, column=7)
        self.button_LED05  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,5", command = self.cb_led05 )
        self.button_LED05.grid(row=1, column=8)
        self.button_LED06  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,6", command = self.cb_led06 )
        self.button_LED06.grid(row=1, column=9)
        self.button_LED07  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 0,7", command = self.cb_led07 )
        self.button_LED07.grid(row=1, column=10)

        self.button_Color0 =  Tkinter.Button(win, bg=self.color0, text="Color0", command = self.cb_Color0 )
        self.button_Color0.grid(row=1, column=11)

        self.button_setColor0 = Tkinter.Button(win, bg='white',text="setColor0", command = self.cb_setColor0 )
        self.button_setColor0.grid(row=1, column=12)

        ######################################################
        self.button_Load1 = Tkinter.Button(win, text = "Load 1", command = self.cb_Load1, compound="left")
        self.button_Load1.grid(row=2, column=0)
        self.button_image1 = Tkinter.Button(win, image = self.image1, command = self.cb_image1)
        self.button_image1.grid(row=2, column=1)
        self.button_Store1 = Tkinter.Button(win, text = "Store 1", command = self.cb_Store1)
        self.button_Store1.grid(row=2, column=2)
        
        self.button_LED10  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,0", command = self.cb_led10)
        self.button_LED10.grid(row=2, column=3)
        self.button_LED11  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,1", command = self.cb_led11)
        self.button_LED11.grid(row=2, column=4)
        self.button_LED12  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,2", command = self.cb_led12)
        self.button_LED12.grid(row=2, column=5)
        self.button_LED13  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,3", command = self.cb_led13)
        self.button_LED13.grid(row=2, column=6)
        self.button_LED14  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,4", command = self.cb_led14)
        self.button_LED14.grid(row=2, column=7)
        self.button_LED15  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,5", command = self.cb_led15)
        self.button_LED15.grid(row=2, column=8)
        self.button_LED16  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,6", command = self.cb_led16)
        self.button_LED16.grid(row=2, column=9)
        self.button_LED17  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 1,7", command = self.cb_led17)
        self.button_LED17.grid(row=2, column=10)
        self.button_Color1 = Tkinter.Button(win, bg=self.color1,text="Color1", command = self.cb_Color1 )
        self.button_Color1.grid(row=2, column=11)
        self.button_setColor1 = Tkinter.Button(win, bg='white',text="setColor1", command = self.cb_setColor1 )
        self.button_setColor1.grid(row=2, column=12)

        self.button_Load2 = Tkinter.Button(win, text = "Load 2", command = self.cb_Load2, compound="left")
        self.button_Load2.grid(row=3, column=0)
        self.button_image2 = Tkinter.Button(win, image = self.image2, command = self.cb_image2)
        self.button_image2.grid(row=3, column=1)
        self.button_Store2 = Tkinter.Button(win, text = "Store 2", command = self.cb_Store2)
        self.button_Store2.grid(row=3, column=2)
        
        self.button_LED20  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,0", command = self.cb_led20)
        self.button_LED20.grid(row=3, column=3)
        self.button_LED21  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,1", command = self.cb_led21)
        self.button_LED21.grid(row=3, column=4)
        self.button_LED22  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,2", command = self.cb_led22)
        self.button_LED22.grid(row=3, column=5)
        self.button_LED23  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,3", command = self.cb_led23)
        self.button_LED23.grid(row=3, column=6)
        self.button_LED24  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,4", command = self.cb_led24)
        self.button_LED24.grid(row=3, column=7)
        self.button_LED25  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,5", command = self.cb_led25)
        self.button_LED25.grid(row=3, column=8)
        self.button_LED26  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,6", command = self.cb_led26)
        self.button_LED26.grid(row=3, column=9)
        self.button_LED27  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 2,7", command = self.cb_led27)
        self.button_LED27.grid(row=3, column=10)
        self.button_Color2 = Tkinter.Button(win, bg=self.color2,text="Color2", command = self.cb_Color2 )
        self.button_Color2.grid(row=3, column=11)
        self.button_setColor2 = Tkinter.Button(win, bg='white',text="setColor2", command = self.cb_setColor2 )
        self.button_setColor2.grid(row=3, column=12)

        self.button_Load3 = Tkinter.Button(win, text = "Load 3", command = self.cb_Load3, compound="left")
        self.button_Load3.grid(row=4, column=0)
        self.button_image3 = Tkinter.Button(win, image = self.image3, command = self.cb_image3)
        self.button_image3.grid(row=4, column=1)
        self.button_Store3 = Tkinter.Button(win, text = "Store 3", command = self.cb_Store3)
        self.button_Store3.grid(row=4, column=2)
        
        self.button_LED30  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,0", command = self.cb_led30)
        self.button_LED30.grid(row=4, column=3)
        self.button_LED31  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,1", command = self.cb_led31)
        self.button_LED31.grid(row=4, column=4)
        self.button_LED32  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,2", command = self.cb_led32)
        self.button_LED32.grid(row=4, column=5)
        self.button_LED33  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,3", command = self.cb_led33)
        self.button_LED33.grid(row=4, column=6)
        self.button_LED34  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,4", command = self.cb_led34)
        self.button_LED34.grid(row=4, column=7)
        self.button_LED35  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,5", command = self.cb_led35)
        self.button_LED35.grid(row=4, column=8)
        self.button_LED36  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,6", command = self.cb_led36)
        self.button_LED36.grid(row=4, column=9)
        self.button_LED37  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 3,7", command = self.cb_led37)
        self.button_LED37.grid(row=4, column=10)
        self.button_Color3 = Tkinter.Button(win, bg=self.color3, text="Color3", command = self.cb_Color3 )
        self.button_Color3.grid(row=4, column=11)
        self.button_setColor3 = Tkinter.Button(win, bg='white',text="setColor3", command = self.cb_setColor3 )
        self.button_setColor3.grid(row=4, column=12)

        self.button_Load4 = Tkinter.Button(win, text = "Load 4", command = self.cb_Load4, compound="left")
        self.button_Load4.grid(row=5, column=0)
        self.button_image4 = Tkinter.Button(win, image = self.image4, command = self.cb_image4)
        self.button_image4.grid(row=5, column=1)
        self.button_Store4 = Tkinter.Button(win, text = "Store 4", command = self.cb_Store4)
        self.button_Store4.grid(row=5, column=2)
        
        self.button_LED40  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,0", command = self.cb_led40)
        self.button_LED40.grid(row=5, column=3)
        self.button_LED41  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,1", command = self.cb_led41)
        self.button_LED41.grid(row=5, column=4)
        self.button_LED42  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,2", command = self.cb_led42)
        self.button_LED42.grid(row=5, column=5)
        self.button_LED43  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,3", command = self.cb_led43)
        self.button_LED43.grid(row=5, column=6)
        self.button_LED44  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,4", command = self.cb_led44)
        self.button_LED44.grid(row=5, column=7)
        self.button_LED45  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,5", command = self.cb_led45)
        self.button_LED45.grid(row=5, column=8)
        self.button_LED46  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,6", command = self.cb_led46)
        self.button_LED46.grid(row=5, column=9)
        self.button_LED47  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 4,7", command = self.cb_led47)
        self.button_LED47.grid(row=5, column=10)
        self.button_Color4 = Tkinter.Button(win, bg=self.color4, text="Color4", command = self.cb_Color4 )
        self.button_Color4.grid(row=5, column=11)
        self.button_setColor4 = Tkinter.Button(win, bg='white',text="setColor4", command = self.cb_setColor4 )
        self.button_setColor4.grid(row=5, column=12)

        self.button_Load5 = Tkinter.Button(win, text = "Load 5", command = self.cb_Load5, compound="left")
        self.button_Load5.grid(row=6, column=0)
        self.button_image5 = Tkinter.Button(win, image = self.image5, command = self.cb_image5)
        self.button_image5.grid(row=6, column=1)
        self.button_Store5 = Tkinter.Button(win, text = "Store 5", command = self.cb_Store5)
        self.button_Store5.grid(row=6, column=2)
        
        self.button_LED50  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,0", command = self.cb_led50)
        self.button_LED50.grid(row=6, column=3)
        self.button_LED51  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,1", command = self.cb_led51)
        self.button_LED51.grid(row=6, column=4)
        self.button_LED52  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,2", command = self.cb_led52)
        self.button_LED52.grid(row=6, column=5)
        self.button_LED53  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,3", command = self.cb_led53)
        self.button_LED53.grid(row=6, column=6)
        self.button_LED54  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,4", command = self.cb_led54)
        self.button_LED54.grid(row=6, column=7)
        self.button_LED55  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,5", command = self.cb_led55)
        self.button_LED55.grid(row=6, column=8)
        self.button_LED56  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,6", command = self.cb_led56)
        self.button_LED56.grid(row=6, column=9)
        self.button_LED57  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 5,7", command = self.cb_led57)
        self.button_LED57.grid(row=6, column=10)
        self.button_Color5 = Tkinter.Button(win, bg=self.color5, text="Color5", command = self.cb_Color5 )
        self.button_Color5.grid(row=6, column=11)
        self.button_setColor5 = Tkinter.Button(win, bg='white',text="setColor5", command = self.cb_setColor5 )
        self.button_setColor5.grid(row=6, column=12)

        self.button_Load6 = Tkinter.Button(win, text = "Load 6", command = self.cb_Load6, compound="left")
        self.button_Load6.grid(row=7, column=0)
        self.button_image6 = Tkinter.Button(win, image = self.image6, command = self.cb_image6)
        self.button_image6.grid(row=7, column=1)
        self.button_Store6 = Tkinter.Button(win, text = "Store 6", command = self.cb_Store6)
        self.button_Store6.grid(row=7, column=2)
        
        self.button_LED60  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,0", command = self.cb_led60)
        self.button_LED60.grid(row=7, column=3)
        self.button_LED61  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,1", command = self.cb_led61)
        self.button_LED61.grid(row=7, column=4)
        self.button_LED62  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,2", command = self.cb_led62)
        self.button_LED62.grid(row=7, column=5)
        self.button_LED63  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,3", command = self.cb_led63)
        self.button_LED63.grid(row=7, column=6)
        self.button_LED64  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,4", command = self.cb_led64)
        self.button_LED64.grid(row=7, column=7)
        self.button_LED65  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,5", command = self.cb_led65)
        self.button_LED65.grid(row=7, column=8)
        self.button_LED66  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,6", command = self.cb_led66)
        self.button_LED66.grid(row=7, column=9)
        self.button_LED67  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 6,7", command = self.cb_led67)
        self.button_LED67.grid(row=7, column=10)
        self.button_Color6 = Tkinter.Button(win, bg=self.color6, text="Color6", command = self.cb_Color6 )
        self.button_Color6.grid(row=7, column=11)
        self.button_setColor6 = Tkinter.Button(win, bg='white',text="setColor6", command = self.cb_setColor6 )
        self.button_setColor6.grid(row=7, column=12)

        self.button_Load7 = Tkinter.Button(win, text = "Load 7", command = self.cb_Load7, compound="left")
        self.button_Load7.grid(row=8, column=0)
        self.button_image7 = Tkinter.Button(win, image = self.image7, command = self.cb_image7)
        self.button_image7.grid(row=8, column=1)
        self.button_Store7 = Tkinter.Button(win, text = "Store 7", command = self.cb_Store7)
        self.button_Store7.grid(row=8, column=2)
        
        self.button_LED70  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,0", command = self.cb_led70)
        self.button_LED70.grid(row=8, column=3)
        self.button_LED71  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,1", command = self.cb_led71)
        self.button_LED71.grid(row=8, column=4)
        self.button_LED72  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,2", command = self.cb_led72)
        self.button_LED72.grid(row=8, column=5)
        self.button_LED73  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,3", command = self.cb_led73)
        self.button_LED73.grid(row=8, column=6)
        self.button_LED74  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,4", command = self.cb_led74)
        self.button_LED74.grid(row=8, column=7)
        self.button_LED75  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,5", command = self.cb_led75)
        self.button_LED75.grid(row=8, column=8)
        self.button_LED76  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,6", command = self.cb_led76)
        self.button_LED76.grid(row=8, column=9)
        self.button_LED77  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red',text="LED 7,7", command = self.cb_led77)
        self.button_LED77.grid(row=8, column=10)
        self.button_Color7 = Tkinter.Button(win, bg=self.color7, text="Color7", command = self.cb_Color7 )
        self.button_Color7.grid(row=8, column=11)
        self.button_setColor7 = Tkinter.Button(win, bg='white',text="setColor7", command = self.cb_setColor7 )
        self.button_setColor7.grid(row=8, column=12)

    def cb_clear_colors(self):
        Matrix = bytearray(192)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(Matrix)

    def cb_image0(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b0)
    def cb_image1(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b1)
    def cb_image2(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b2)
    def cb_image3(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b3)
    def cb_image4(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b4)
    def cb_image5(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b5)
    def cb_image6(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b6)
    def cb_image7(self):
        # send the full image to the display all in one message
        self.send_array_as_bin(self.b7)
    
    
    
    def cb_Store0(self):
        Matrix= bytearray()
        self.button_Store0.configure(text = 'ACTIVE')
        self.button_Store0.configure(text = 'Store0')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        print"cb_Store0: Saving gif file %s" % (save_filename)
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image0 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on to the button 
        self.button_image0.configure(image = self.image0)
        self.b0= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b0)
        
    def cb_Store1(self):
        Matrix= bytearray()
        self.button_Store1.configure(text = 'ACTIVE')
        self.button_Store1.configure(text = 'Store1')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image1 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image1.configure(image = self.image1)
        self.b1= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b1)
        
    def cb_Store2(self):
        Matrix= bytearray()
        self.button_Store2.configure(text = 'ACTIVE')
        self.button_Store2.configure(text = 'Store2')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image2 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image2.configure(image = self.image2)
        self.b2= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b2)
        
    def cb_Store3(self):
        Matrix= bytearray()
        self.button_Store3.configure(text = 'ACTIVE')
        self.button_Store3.configure(text = 'Store3')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image3 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image3.configure(image = self.image3)
        self.b3= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b3)
        
    def cb_Store4(self):
        Matrix= bytearray()
        self.button_Store4.configure(text = 'ACTIVE')
        self.button_Store4.configure(text = 'Store4')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image4 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image4.configure(image = self.image4)
        self.b4= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b4)
        
    def cb_Store5(self):
        Matrix= bytearray()
        self.button_Store5.configure(text = 'ACTIVE')
        self.button_Store5.configure(text = 'Store5')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image5 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image5.configure(image = self.image5)
        self.b5= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b5)
        
    def cb_Store6(self):
        Matrix= bytearray()
        self.button_Store6.configure(text = 'ACTIVE')
        self.button_Store6.configure(text = 'Store6')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image6 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image6.configure(image = self.image6)
        self.b6= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b6)
        
    def cb_Store7(self):
        Matrix= bytearray()
        self.button_Store7.configure(text = 'ACTIVE')
        self.button_Store7.configure(text = 'Store7')
        save_filename = tkFileDialog.asksaveasfilename(initialdir=('../led_data_files/'),filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        [filename,Matrix] = self.make_GIF_fromBigMatrix(save_filename)
        self.image7 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image7.configure(image = self.image7)
        self.b7= Matrix # now load the new image into the drawing pallet buffer
        self.update_file_LED_DAT(filename,Matrix)
        self.bigMatrix = self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b7)

    def cb_Load0(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'), filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image0 = Tkinter.PhotoImage(file = filename)   
        self.button_image0.configure(image = self.image0)
        self.b0= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b0)        
    
    def cb_Load1(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image1 = Tkinter.PhotoImage(file = filename)
        self.button_image1.configure(image = self.image1)
        self.b1= bytearray(Matrix)
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b1)
        
    def cb_Load2(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image2 = Tkinter.PhotoImage(file = filename)
        self.button_image2.configure(image = self.image2)
        self.b2= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b2)
    
    def cb_Load3(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image3 = Tkinter.PhotoImage(file = filename)
        self.button_image3.configure(image = self.image3)
        self.b3= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b3)
    
    def cb_Load4(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image4 = Tkinter.PhotoImage(file = filename)
        self.button_image4.configure(image = self.image4)
        self.b4= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b4)
    
    def cb_Load5(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image5 = Tkinter.PhotoImage(file = filename)
        self.button_image5.configure(image = self.image5)
        self.b5= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b5)
    
    def cb_Load6(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image6 = Tkinter.PhotoImage(file = filename)
        self.button_image6.configure(image = self.image6)
        self.b6= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b6)
    
    def cb_Load7(self):
        Matrix= bytearray()
        self.file_path = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        [filename,Matrix] = self.load_GIF_return_as_array()
        self.image7 = Tkinter.PhotoImage(file = filename)
        self.button_image7.configure(image = self.image7)
        self.b7= Matrix
        self.return_bigMatrix_from_bytearray(Matrix)
        self.update_BIGmatrix_buttons(Matrix)
        self.send_array_as_bin(self.b7)
        
    def cb_Color0(self):
        self.button_selected_color.configure(bg = self.color0)
        self.selected_color = self.color0

    def cb_Color1(self):
        self.button_selected_color.configure(bg = self.color1)
        self.selected_color = self.color1
        
    def cb_Color2(self):
        self.button_selected_color.configure(bg = self.color2)
        self.selected_color = self.color2
        
    def cb_Color3(self):
        self.button_selected_color.configure(bg = self.color3)
        self.selected_color = self.color3
        
    def cb_Color4(self):
        self.button_selected_color.configure(bg = self.color4)
        self.selected_color = self.color4
        
    def cb_Color5(self):
        self.button_selected_color.configure(bg = self.color5)
        self.selected_color = self.color5
        
    def cb_Color6(self):
        self.button_selected_color.configure(bg = self.color6)
        self.selected_color = self.color6
        
    def cb_Color7(self):
        self.button_selected_color.configure(bg = self.color7)
        self.selected_color = self.color7


    def cb_setColor0(self):
        self.button_Color0.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color0.configure(bg = hexstr)
          self.color0 = hexstr

    def cb_setColor1(self):
        self.button_Color1.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color1.configure(bg = hexstr)
          self.color1 = hexstr
                
    def cb_setColor2(self):
        self.button_Color2.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color2.configure(bg = hexstr)
          self.color2 = hexstr
                
    def cb_setColor3(self):
        self.button_Color3.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color3.configure(bg = hexstr)
          self.color3 = hexstr
                
    def cb_setColor4(self):
        self.button_Color4.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color4.configure(bg = hexstr)
          self.color4 = hexstr
                
    def cb_setColor5(self):
        self.button_Color5.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color5.configure(bg = hexstr)
          self.color5 = hexstr
                
    def cb_setColor6(self):
        self.button_Color6.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color6.configure(bg = hexstr)
          self.color6 = hexstr
                
    def cb_setColor7(self):
        self.button_Color7.configure(bg = 'white')
        (triple, hexstr) = askcolor()
        if hexstr:
          self.button_Color7.configure(bg = hexstr)
          self.color7 = hexstr



    def cb_led00(self):
        self.button_LED00.configure(bg = self.selected_color)
        self.bigMatrix [0][0] = self.selected_color
        setLED = "80As..0000%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led01(self):
        self.button_LED01.configure(bg = self.selected_color)
        self.bigMatrix [0][1] = self.selected_color
        setLED = "80As..0001%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led02(self):
        self.button_LED02.configure(bg = self.selected_color)
        self.bigMatrix [0][2] = self.selected_color
        setLED = "80As..0002%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led03(self):
        self.button_LED03.configure(bg = self.selected_color)
        self.bigMatrix [0][3] = self.selected_color
        setLED = "80As..0003%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led04(self):
        self.button_LED04.configure(bg = self.selected_color)
        self.bigMatrix [0][4] = self.selected_color
        setLED = "80As..0004%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led05(self):
        self.button_LED05.configure(bg = self.selected_color)
        self.bigMatrix [0][5] = self.selected_color
        setLED = "80As..0005%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led06(self):
        self.button_LED06.configure(bg = self.selected_color)
        self.bigMatrix [0][6] = self.selected_color
        setLED = "80As..0006%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led07(self):
        self.button_LED07.configure(bg = self.selected_color)
        self.bigMatrix [0][7] = self.selected_color
        setLED = "80As..0007%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_led10(self):
        self.button_LED10.configure(bg = self.selected_color)
        self.bigMatrix [1][0] = self.selected_color
        setLED = "80As..0100%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led11(self):
        self.button_LED11.configure(bg = self.selected_color)
        self.bigMatrix [1][1] = self.selected_color
        setLED = "80As..0101%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led12(self):
        self.button_LED12.configure(bg = self.selected_color)
        self.bigMatrix [1][2] = self.selected_color
        setLED = "80As..0102%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led13(self):
        self.button_LED13.configure(bg = self.selected_color)
        self.bigMatrix [1][3] = self.selected_color
        setLED = "80As..0103%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led14(self):
        self.button_LED14.configure(bg = self.selected_color)
        self.bigMatrix [1][4] = self.selected_color
        setLED = "80As..0104%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led15(self):
        self.button_LED15.configure(bg = self.selected_color)
        self.bigMatrix [1][5] = self.selected_color
        setLED = "80As..0105%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led16(self):
        self.button_LED16.configure(bg = self.selected_color)
        self.bigMatrix [1][6] = self.selected_color
        setLED = "80As..0106%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led17(self):
        self.button_LED17.configure(bg = self.selected_color)
        self.bigMatrix [1][7] = self.selected_color
        setLED = "80As..0107%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_led20(self):
        self.button_LED20.configure(bg = self.selected_color)
        self.bigMatrix [2][0] = self.selected_color
        setLED = "80As..0200%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led21(self):
        self.button_LED21.configure(bg = self.selected_color)
        self.bigMatrix [2][1] = self.selected_color
        setLED = "80As..0201%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led22(self):
        self.button_LED22.configure(bg = self.selected_color)
        self.bigMatrix [2][2] = self.selected_color
        setLED = "80As..0202%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led23(self):
        self.button_LED23.configure(bg = self.selected_color)
        self.bigMatrix [2][3] = self.selected_color
        setLED = "80As..0203%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led24(self):
        self.button_LED24.configure(bg = self.selected_color)
        self.bigMatrix [2][4] = self.selected_color
        setLED = "80As..0204%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led25(self):
        self.button_LED25.configure(bg = self.selected_color)
        self.bigMatrix [2][5] = self.selected_color
        setLED = "80As..0205%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led26(self):
        self.button_LED26.configure(bg = self.selected_color)
        self.bigMatrix [2][6] = self.selected_color
        setLED = "80As..0206%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led27(self):
        self.button_LED27.configure(bg = self.selected_color)
        self.bigMatrix [2][7] = self.selected_color
        setLED = "80As..0207%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_led30(self):
        self.button_LED30.configure(bg = self.selected_color)
        self.bigMatrix [3][0] = self.selected_color
        setLED = "80As..0300%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led31(self):
        self.button_LED31.configure(bg = self.selected_color)
        self.bigMatrix [3][1] = self.selected_color
        setLED = "80As..0301%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led32(self):
        self.button_LED32.configure(bg = self.selected_color)
        self.bigMatrix [3][2] = self.selected_color
        setLED = "80As..0302%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led33(self):
        self.button_LED33.configure(bg = self.selected_color)
        self.bigMatrix [3][3] = self.selected_color
        setLED = "80As..0303%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led34(self):
        self.button_LED34.configure(bg = self.selected_color)
        self.bigMatrix [3][4] = self.selected_color
        setLED = "80As..0304%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led35(self):
        self.button_LED35.configure(bg = self.selected_color)
        self.bigMatrix [3][5] = self.selected_color
        setLED = "80As..0305%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led36(self):
        self.button_LED36.configure(bg = self.selected_color)
        self.bigMatrix [3][6] = self.selected_color
        setLED = "80As..0306%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led37(self):
        self.button_LED37.configure(bg = self.selected_color)
        self.bigMatrix [3][7] = self.selected_color
        setLED = "80As..0307%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_led40(self):
        self.button_LED40.configure(bg = self.selected_color)
        self.bigMatrix [4][0] = self.selected_color
        setLED = "80As..0400%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led41(self):
        self.button_LED41.configure(bg = self.selected_color)
        self.bigMatrix [4][1] = self.selected_color
        setLED = "80As..0401%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led42(self):
        self.button_LED42.configure(bg = self.selected_color)
        self.bigMatrix [4][2] = self.selected_color
        setLED = "80As..0402%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led43(self):
        self.button_LED43.configure(bg = self.selected_color)
        self.bigMatrix [4][3] = self.selected_color
        setLED = "80As..0403%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led44(self):
        self.button_LED44.configure(bg = self.selected_color)
        self.bigMatrix [4][4] = self.selected_color
        setLED = "80As..0404%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led45(self):
        self.button_LED45.configure(bg = self.selected_color)
        self.bigMatrix [4][5] = self.selected_color
        setLED = "80As..0405%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led46(self):
        self.button_LED46.configure(bg = self.selected_color)
        self.bigMatrix [4][6] = self.selected_color
        setLED = "80As..0406%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led47(self):
        self.button_LED47.configure(bg = self.selected_color)
        self.bigMatrix [4][7] = self.selected_color
        setLED = "80As..0407%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_led50(self):
        self.button_LED50.configure(bg = self.selected_color)
        self.bigMatrix [5][0] = self.selected_color
        setLED = "80As..0500%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led51(self):
        self.button_LED51.configure(bg = self.selected_color)
        self.bigMatrix [5][1] = self.selected_color
        setLED = "80As..0501%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led52(self):
        self.button_LED52.configure(bg = self.selected_color)
        self.bigMatrix [5][2] = self.selected_color
        setLED = "80As..0502%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led53(self):
        self.button_LED53.configure(bg = self.selected_color)
        self.bigMatrix [5][3] = self.selected_color
        setLED = "80As..0503%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led54(self):
        self.button_LED54.configure(bg = self.selected_color)
        self.bigMatrix [5][4] = self.selected_color
        setLED = "80As..0504%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led55(self):
        self.button_LED55.configure(bg = self.selected_color)
        self.bigMatrix [5][5] = self.selected_color
        setLED = "80As..0505%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led56(self):
        self.button_LED56.configure(bg = self.selected_color)
        self.bigMatrix [5][6] = self.selected_color
        setLED = "80As..0506%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led57(self):
        self.button_LED57.configure(bg = self.selected_color)
        self.bigMatrix [5][7] = self.selected_color
        setLED = "80As..0507%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1

    def cb_led60(self):
        self.button_LED60.configure(bg = self.selected_color)
        self.bigMatrix [6][0] = self.selected_color
        setLED = "80As..0600%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led61(self):
        self.button_LED61.configure(bg = self.selected_color)
        self.bigMatrix [6][1] = self.selected_color
        setLED = "80As..0601%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led62(self):
        self.button_LED62.configure(bg = self.selected_color)
        self.bigMatrix [6][2] = self.selected_color
        setLED = "80As..0602%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led63(self):
        self.button_LED63.configure(bg = self.selected_color)
        self.bigMatrix [6][3] = self.selected_color
        setLED = "80As..0603%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led64(self):
        self.button_LED64.configure(bg = self.selected_color)
        self.bigMatrix [6][4] = self.selected_color
        setLED = "80As..0604%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led65(self):
        self.button_LED65.configure(bg = self.selected_color)
        self.bigMatrix [6][5] = self.selected_color
        setLED = "80As..0605%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led66(self):
        self.button_LED66.configure(bg = self.selected_color)
        self.bigMatrix [6][6] = self.selected_color
        setLED = "80As..0606%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led67(self):
        self.button_LED67.configure(bg = self.selected_color)
        self.bigMatrix [6][7] = self.selected_color
        setLED = "80As..0607%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1

    def cb_led70(self):
        self.button_LED70.configure(bg = self.selected_color)
        self.bigMatrix [7][0] = self.selected_color
        setLED = "80As..0700%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led71(self):
        self.button_LED71.configure(bg = self.selected_color)
        self.bigMatrix [7][1] = self.selected_color
        setLED = "80As..0701%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led72(self):
        self.button_LED72.configure(bg = self.selected_color)
        self.bigMatrix [7][2] = self.selected_color
        setLED = "80As..0702%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led73(self):
        self.button_LED73.configure(bg = self.selected_color)
        self.bigMatrix [7][3] = self.selected_color
        setLED = "80As..0703%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led74(self):
        self.button_LED74.configure(bg = self.selected_color)
        self.bigMatrix [7][4] = self.selected_color
        setLED = "80As..0704%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led75(self):
        self.button_LED75.configure(bg = self.selected_color)
        self.bigMatrix [7][5] = self.selected_color
        setLED = "80As..0705%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led76(self):
        self.button_LED76.configure(bg = self.selected_color)
        self.bigMatrix [7][6] = self.selected_color
        setLED = "80As..0706%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1
    def cb_led77(self):
        self.button_LED77.configure(bg = self.selected_color)
        self.bigMatrix [7][7] = self.selected_color
        setLED = "80As..0707%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q1.put(setLED) # write a string to the serial port via tx_queue1


    def cb_animate_loop(self):
      self.data_inp_1 =  self.enter_data_1.get()      # Fetch text from the box.
      print float(self.data_inp_1)
      for al in range(0,5):
        self.q1.put(self.b0)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b1)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b2)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b3)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b4)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b5)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b6)
        time.sleep(float(self.data_inp_1))
        self.q1.put(self.b7)
        time.sleep(float(self.data_inp_1))

    def cb_animate_canvas(self,CanvasName):   #TargetWidget_TargetObject.ShowObjectDict('TopCanvas')
        self.data_inp_1 =  self.enter_data_1.get()      # Fetch text from the box.
        print float(self.data_inp_1)
        if len(CanvasDnd.ObjectDict) > 0:
          for Name,Object in CanvasDnd.ObjectDict.items():
            print 'NAME: %s  ????: %s COORD %s GIF file: %s '%(Name,Object(0),Object(1),Object(2))
            #self.q1.put(load_GIF_return_as_array(self,Object(2))) ###########% load GIF 
            time.sleep(float(self.data_inp_1))
          else:
            print "    <empty>"
    
    def make_GIF_fromBigMatrix(self,filename):
        # make a gif from bigMatrix
        tempBuffer = bytearray()
        # create a empty 8 x 8 matrix
        img = Image.new('RGB',(100, 100))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 101,101), fill=(255,255,255))
        # fill in the 8x8 matrix
        for s in LED_TAB.box_coord_vh:
          #print"make_GIF_fromBigMatrix coord = %16s Y=%02i, X=%02i  bigMatrix= %s" % (str(s), (s[2]/12)-1, (s[3]/12)-1, str(self.bigMatrix[(s[2]/12)-1][(s[3]/12)-1]) )
          r = int(str(self.bigMatrix[(s[2]/12)-1][(s[3]/12)-1])[1:3],16) #print"r = %i\n"% (r) # get 1st byte
          g = int(str(self.bigMatrix[(s[2]/12)-1][(s[3]/12)-1])[3:5],16) #print"g = %i\n"% (g) # get 2nd byte
          b = int(str(self.bigMatrix[(s[2]/12)-1][(s[3]/12)-1])[5:7],16) #print"g = %i\n"% (b) # get 3rd byte
          tempBuffer.append(r)
          tempBuffer.append(g)
          tempBuffer.append(b)
          draw.rectangle( s , fill=self.bigMatrix[(s[3]/12)-1][(s[2]/12)-1] )
        # save the gif file
        img.save(filename, 'GIF', transparency=0)
        self.update_file_LED_DAT(filename,tempBuffer)
        return [filename,tempBuffer]
    
    def update_file_LED_DAT(self,filename,matrix):  
        new_filename = filename[:len(filename)-4:] + ".DAT"
        print("Writing DAT file %s \n" %(filename))
        Fdat = open(new_filename, "w+")
        Fdat.write(b"80Fd.."); #Ether Port 80 + Command to LED Display
        Fdat.write(matrix);
         #Close opened file
        Fdat.close()  
        return
    
    def get_bytes_from_file(self,filename):  
        tempBuffer = bytearray()
        try:
          #operation_that_can_throw_ioerror()
          f = open(filename, "rb");
          print"get_bytes_from_file: FOUND DAT FILE %s" % (filename)
          f.read(6); # read the first 6 bytes and throw away, port and cmd code
          data = f.read();
          print"the length of file is %i" % (len(data))
          for line in data:
            print line.encode('hex')
            tempBuffer.append(line)
          return tempBuffer
          
        except IOError:
        #handle_the_exception_somehow()
        # if the .dat file doesn't exist use .gif file as source 
          print"get_bytes_from_file: ERROR NO DAT FILE, using GIF"
          img = Image.open(filename.replace('.dat','.gif'))
          rgb_pix = img.convert('RGB')
          ledColorMatrix = [['#ffffff' for x in xrange(8)] for x in xrange(8)]
          for s in self.box_coord_vh:
            r,g,b = rgb_pix.getpixel((s[3]-4,s[2]-4)) # center of each box
            hexstring = ('#%02X%02X%02X'%(r,g,b))
            ledColorMatrix[(s[3]/12)-1][(s[2]/12)-1] =  hexstring
            tempBuffer.append(r)
            tempBuffer.append(g)
            tempBuffer.append(b)
          print"There was no .dat file so creating one";
          self.update_file_LED_DAT(filename,tempBuffer)
          #print"get_bytes_from_file: tempBuffer"
          #print tempBuffer
          return tempBuffer
        
        #else:
        # # we don't want to catch the IOError if it's raised
        # another_operation_that_can_throw_ioerror()
        #finally:
        # something_we_always_need_to_do()
        

    def load_GIF_return_as_array(self):
        tempBuffer = bytearray()
        img = Image.open(self.file_path)
        data_file_name = self.file_path.replace('.gif','.dat')
        print("Original File Path is: %s" % (self.file_path))
        print("Data     File Path is: %s" % (data_file_name))
        tempBuffer = self.get_bytes_from_file(data_file_name)
        #print"tempBuffer"
        #for i in tempBuffer:
        #  print i
        return [self.file_path,tempBuffer]
    
    def send_array_as_asc_each_pixel_rgb(self,array):
        # array is a buffer length 192 = 8x * 8y * 3 bytes
        #print"array"
        #print array
        for s in array[::3]:  # [start:stop:step]
          x = s % 3  # % is mod
          y = s % 12
          r = int(s+0)
          g = int(s+1)
          b = int(s+2)
          setLED = "80As..%02i%02i%03i%03i%03iz" % ( x,y,r,g,b )
          #print"send array coord = %16s X=%02i, Y=%02i  Array= #%02X%02X%02X  %s"% (str(s), x, y, r, g, b, setLED )
          self.q1.put(setLED) # write a string to the tx port via tx_queue1
    
    def send_array_as_bin(self,array):
        # array is a buffer length 192 = 8x * 8y * 3 bytes(RGB)
        print("send_array_as_bin: The array length is: %i"%( len(array)))
        msg = buffer(b"80Fd..") + array
        self.q1.put(msg) # send array
        
    def return_bigMatrix_from_bytearray(self,matrix):
        localBigMatrix = [['#000000' for x in xrange(8)] for x in xrange(8)]
        colorstrings = []
        color_index = 0
            
        for s in range(0,191,3):
          colorstrings.append('#%02X%02X%02X'%(matrix[s+0],matrix[s+1],matrix[s+2]))
          #print"return_bigMatrix_from_bytearray: %s" % ('#%02X%02X%02X'%(matrix[s+0],matrix[s+1],matrix[s+2] ))              
        
        for y in range(0,7):
          for x in range(0,7):
            localBigMatrix[y][x] =  colorstrings[color_index]
            #print "Y= %i, X= %i bigMatrix = %s" % (y,x,localBigMatrix[y][x])
            color_index += 1
        return localBigMatrix
    
    
    
    def update_BIGmatrix_buttons(self,matrix):
        ##             RC
        self.button_LED00.configure(bg = ('#%02X%02X%02X'%(matrix[ 0],matrix[ 1],matrix[ 2])))
        self.button_LED01.configure(bg = ('#%02X%02X%02X'%(matrix[24],matrix[25],matrix[26])))
        self.button_LED02.configure(bg = ('#%02X%02X%02X'%(matrix[48],matrix[49],matrix[50])))
        self.button_LED03.configure(bg = ('#%02X%02X%02X'%(matrix[72],matrix[73],matrix[74])))
        self.button_LED04.configure(bg = ('#%02X%02X%02X'%(matrix[ 96],matrix[ 97],matrix[ 98])))
        self.button_LED05.configure(bg = ('#%02X%02X%02X'%(matrix[120],matrix[121],matrix[122])))
        self.button_LED06.configure(bg = ('#%02X%02X%02X'%(matrix[144],matrix[145],matrix[146])))
        self.button_LED07.configure(bg = ('#%02X%02X%02X'%(matrix[168],matrix[169],matrix[170])))
                                         
        self.button_LED10.configure(bg = ('#%02X%02X%02X'%(matrix[ 3],matrix[ 4],matrix[ 5])))
        self.button_LED11.configure(bg = ('#%02X%02X%02X'%(matrix[27],matrix[28],matrix[29])))
        self.button_LED12.configure(bg = ('#%02X%02X%02X'%(matrix[51],matrix[52],matrix[53])))
        self.button_LED13.configure(bg = ('#%02X%02X%02X'%(matrix[75],matrix[76],matrix[77])))
        self.button_LED14.configure(bg = ('#%02X%02X%02X'%(matrix[ 99],matrix[100],matrix[101])))
        self.button_LED15.configure(bg = ('#%02X%02X%02X'%(matrix[123],matrix[124],matrix[125])))
        self.button_LED16.configure(bg = ('#%02X%02X%02X'%(matrix[147],matrix[148],matrix[149])))
        self.button_LED17.configure(bg = ('#%02X%02X%02X'%(matrix[171],matrix[172],matrix[173])))
                                         
        self.button_LED20.configure(bg = ('#%02X%02X%02X'%(matrix[ 6],matrix[ 7],matrix[ 8])))
        self.button_LED21.configure(bg = ('#%02X%02X%02X'%(matrix[30],matrix[31],matrix[32])))
        self.button_LED22.configure(bg = ('#%02X%02X%02X'%(matrix[54],matrix[55],matrix[56])))
        self.button_LED23.configure(bg = ('#%02X%02X%02X'%(matrix[78],matrix[79],matrix[80])))
        self.button_LED24.configure(bg = ('#%02X%02X%02X'%(matrix[102],matrix[103],matrix[104])))
        self.button_LED25.configure(bg = ('#%02X%02X%02X'%(matrix[126],matrix[127],matrix[128])))
        self.button_LED26.configure(bg = ('#%02X%02X%02X'%(matrix[150],matrix[151],matrix[152])))
        self.button_LED27.configure(bg = ('#%02X%02X%02X'%(matrix[174],matrix[175],matrix[176])))
                                         
        self.button_LED30.configure(bg = ('#%02X%02X%02X'%(matrix[ 9],matrix[10],matrix[11])))
        self.button_LED31.configure(bg = ('#%02X%02X%02X'%(matrix[33],matrix[34],matrix[35])))
        self.button_LED32.configure(bg = ('#%02X%02X%02X'%(matrix[57],matrix[58],matrix[59])))
        self.button_LED33.configure(bg = ('#%02X%02X%02X'%(matrix[81],matrix[82],matrix[83])))
        self.button_LED34.configure(bg = ('#%02X%02X%02X'%(matrix[105],matrix[106],matrix[107])))
        self.button_LED35.configure(bg = ('#%02X%02X%02X'%(matrix[129],matrix[130],matrix[131])))
        self.button_LED36.configure(bg = ('#%02X%02X%02X'%(matrix[153],matrix[154],matrix[155])))
        self.button_LED37.configure(bg = ('#%02X%02X%02X'%(matrix[177],matrix[178],matrix[179])))
        
        self.button_LED40.configure(bg = ('#%02X%02X%02X'%(matrix[12],matrix[13],matrix[14])))
        self.button_LED41.configure(bg = ('#%02X%02X%02X'%(matrix[36],matrix[37],matrix[38])))
        self.button_LED42.configure(bg = ('#%02X%02X%02X'%(matrix[60],matrix[61],matrix[62])))
        self.button_LED43.configure(bg = ('#%02X%02X%02X'%(matrix[84],matrix[85],matrix[86])))
        self.button_LED44.configure(bg = ('#%02X%02X%02X'%(matrix[108],matrix[109],matrix[110])))
        self.button_LED45.configure(bg = ('#%02X%02X%02X'%(matrix[132],matrix[133],matrix[134])))
        self.button_LED46.configure(bg = ('#%02X%02X%02X'%(matrix[156],matrix[157],matrix[158])))
        self.button_LED47.configure(bg = ('#%02X%02X%02X'%(matrix[180],matrix[181],matrix[182])))
                                         
        self.button_LED50.configure(bg = ('#%02X%02X%02X'%(matrix[15],matrix[16],matrix[17])))
        self.button_LED51.configure(bg = ('#%02X%02X%02X'%(matrix[39],matrix[40],matrix[41])))
        self.button_LED52.configure(bg = ('#%02X%02X%02X'%(matrix[63],matrix[64],matrix[65])))
        self.button_LED53.configure(bg = ('#%02X%02X%02X'%(matrix[87],matrix[88],matrix[89])))
        self.button_LED54.configure(bg = ('#%02X%02X%02X'%(matrix[111],matrix[112],matrix[113])))
        self.button_LED55.configure(bg = ('#%02X%02X%02X'%(matrix[135],matrix[136],matrix[137])))
        self.button_LED56.configure(bg = ('#%02X%02X%02X'%(matrix[159],matrix[160],matrix[161])))
        self.button_LED57.configure(bg = ('#%02X%02X%02X'%(matrix[183],matrix[184],matrix[185])))
                                         
        self.button_LED60.configure(bg = ('#%02X%02X%02X'%(matrix[18],matrix[19],matrix[20])))
        self.button_LED61.configure(bg = ('#%02X%02X%02X'%(matrix[42],matrix[43],matrix[44])))
        self.button_LED62.configure(bg = ('#%02X%02X%02X'%(matrix[66],matrix[67],matrix[68])))
        self.button_LED63.configure(bg = ('#%02X%02X%02X'%(matrix[90],matrix[91],matrix[92]))) 
        self.button_LED64.configure(bg = ('#%02X%02X%02X'%(matrix[114],matrix[115],matrix[116])))
        self.button_LED65.configure(bg = ('#%02X%02X%02X'%(matrix[138],matrix[139],matrix[140])))
        self.button_LED66.configure(bg = ('#%02X%02X%02X'%(matrix[162],matrix[163],matrix[164])))
        self.button_LED67.configure(bg = ('#%02X%02X%02X'%(matrix[186],matrix[187],matrix[188])))
                                         
        self.button_LED70.configure(bg = ('#%02X%02X%02X'%(matrix[21],matrix[22],matrix[23])))
        self.button_LED71.configure(bg = ('#%02X%02X%02X'%(matrix[45],matrix[46],matrix[47])))
        self.button_LED72.configure(bg = ('#%02X%02X%02X'%(matrix[69],matrix[70],matrix[71])))
        self.button_LED73.configure(bg = ('#%02X%02X%02X'%(matrix[93],matrix[94],matrix[95])))
        self.button_LED74.configure(bg = ('#%02X%02X%02X'%(matrix[117],matrix[118],matrix[119])))
        self.button_LED75.configure(bg = ('#%02X%02X%02X'%(matrix[141],matrix[142],matrix[143])))
        self.button_LED76.configure(bg = ('#%02X%02X%02X'%(matrix[165],matrix[166],matrix[167])))
        self.button_LED77.configure(bg = ('#%02X%02X%02X'%(matrix[189],matrix[190],matrix[191])))

    
    def clear_colorArray(self):
        # Creates a list holding a 8x8 matrix also initialized to 0
        emptyMatrix = [['#000000' for x in xrange(8)] for x in xrange(8)]
        return emptyMatrix