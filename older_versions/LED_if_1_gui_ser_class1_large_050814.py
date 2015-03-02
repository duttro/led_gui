import time
import serial
import string
import Tkinter
import Tkinter, tkFileDialog
from tkColorChooser import askcolor
import threading
import Queue
from PIL import Image, ImageDraw


# Create the queue
tx_queue = Queue.Queue( )


class Serial:

    def __init__(self, tx_queue):
        
        print"class Serial started"

        self.out=''

        ser = serial.Serial(
            port='com10',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS
            ) 
        print ser.portstr       # check which port was really used


        while (1):
            
            while ser.inWaiting() > 0:
              self.out += ser.read(1)

            if self.out.endswith('\r\n'):
             print ">>" + self.out
             self.out = ''

            
            while tx_queue.qsize(  ):
              
              try:
                 #self.master = master
                 TXmsg = tx_queue.get( )
                 #print "sending msg %s" % (TXmsg)
                 for i in TXmsg:
                   ser.write(i)
                   ###print "echo " + i
                   # we send commands 1 char at time and wait for the echo of each char
                   while ser.inWaiting() == 0:
                     # wait for the char to echo back    
                     pass
                   ser.read(1) #read it
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass

              time.sleep(.01)



                


class GuiPart:

    def __init__(self,win, tx_queue):
        print"GUI init"
        self.image0 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image1 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image2 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image3 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image4 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image5 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image6 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        self.image7 = Tkinter.PhotoImage(file = "./led_array_empty.gif")
        
        self.color0 = '#ff0000'
        self.color1 = '#00ff00'
        self.color2 = '#0000ff'
        self.color3 = '#000000'
        self.color4 = '#ffffff'
        self.color5 = '#ffffff'
        self.color6 = '#ffffff'
        self.color7 = '#ffffff'
        self.selected_color = '#ffffff'
    
        self.q = tx_queue

        self.myFormats = [
          ('CompuServer GIF','*.gif'),
          ]

        # List of coordinates to draw squares in the GIF file
        self.box_coord = [[0 for x in xrange(7)] for x in xrange(7)]
        self.box_coord = [\
                         ( 4, 4,12,12),( 4,16,12,24),( 4,28,12,36),( 4,40,12,48),( 4,52,12,60),( 4,64,12,72),( 4,76,12,84),( 4,88,12,96),\
                         (16, 4,24,12),(16,16,24,24),(16,28,24,36),(16,40,24,48),(16,52,24,60),(16,64,24,72),(16,76,24,84),(16,88,24,96),\
                         (28, 4,36,12),(28,16,36,24),(28,28,36,36),(28,40,36,48),(28,52,36,60),(28,64,36,72),(28,76,36,84),(28,88,36,96),\
                         (40, 4,48,12),(40,16,48,24),(40,28,48,36),(40,40,48,48),(40,52,48,60),(40,64,48,72),(40,76,48,84),(40,88,48,96),\
                         (52, 4,60,12),(52,16,60,24),(52,28,60,36),(52,40,60,48),(52,52,60,60),(52,64,60,72),(52,76,60,84),(52,88,60,96),\
                         (64, 4,72,12),(64,16,72,24),(64,28,72,36),(64,40,72,48),(64,52,72,60),(64,64,72,72),(64,76,72,84),(64,88,72,96),\
                         (76, 4,84,12),(76,16,84,24),(76,28,84,36),(76,40,84,48),(76,52,84,60),(76,64,84,72),(76,76,84,84),(76,88,84,96),\
                         (88, 4,96,12),(88,16,96,24),(88,28,96,36),(88,40,96,48),(88,52,96,60),(88,64,96,72),(88,76,96,84),(88,88,96,96)]
        
        self.Matrix = self.clear_colorArray()
 
        

        # Set up the GUI
        self.button_selected_color = Tkinter.Button(win, text = "Selected Color", bg='white')
        self.button_selected_color.grid(row=0,column=7)
        
        self.button_clear_colors = Tkinter.Button(win, text = "Clear LEDs", bg='white', command = self.cb_clear_colors)
        self.button_clear_colors.grid(row=0,column=6)
        
        #######################################        
        self.button_Load0 = Tkinter.Button(win, text = "Load 0", command = self.cb_Load0, compound="left")
        self.button_Load0.grid(row=1, column=0)
        self.button_image0 = Tkinter.Button(win, image = self.image0)
        self.button_image0.grid(row=1, column=1)
        self.button_Store0 = Tkinter.Button(win, text = "Store 0", command = self.cb_Store0)
        self.button_Store0.grid(row=1, column=2)
      
    
        self.button_LED00  = Tkinter.Button(win, height=2, bd=15, bg="black",fg='red', text="LED 0,0", command = self.cb_led00 )
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
        self.button_image1 = Tkinter.Button(win, image = self.image1)
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
        self.button_image2 = Tkinter.Button(win, image = self.image2)
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
        self.button_image3 = Tkinter.Button(win, image = self.image3)
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
        self.button_image4 = Tkinter.Button(win, image = self.image4)
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
        self.button_image5 = Tkinter.Button(win, image = self.image5)
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
        self.button_image6 = Tkinter.Button(win, image = self.image6)
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
        self.button_image7 = Tkinter.Button(win, image = self.image7)
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
        self.Matrix = self.clear_colorArray()
        self.update_led_buttons(self.Matrix)

    
    def cb_Store0(self):
        self.button_Store0.configure(text = 'ACTIVE')
        self.button_Store0.configure(text = 'Store0')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image0 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image0.configure(image = self.image0)
        
    def cb_Store1(self):
        self.button_Store1.configure(text = 'ACTIVE')
        self.button_Store1.configure(text = 'Store1')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image1 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image1.configure(image = self.image1)
        
    def cb_Store2(self):
        self.button_Store2.configure(text = 'ACTIVE')
        self.button_Store2.configure(text = 'Store2')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image2 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image2.configure(image = self.image2)
        
    def cb_Store3(self):
        self.button_Store3.configure(text = 'ACTIVE')
        self.button_Store3.configure(text = 'Store3')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image3 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image3.configure(image = self.image3)
        
    def cb_Store4(self):
        self.button_Store4.configure(text = 'ACTIVE')
        self.button_Store4.configure(text = 'Store4')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image4 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image4.configure(image = self.image4)
        
    def cb_Store5(self):
        self.button_Store5.configure(text = 'ACTIVE')
        self.button_Store5.configure(text = 'Store5')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image5 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image5.configure(image = self.image5)
        
    def cb_Store6(self):
        self.button_Store6.configure(text = 'ACTIVE')
        self.button_Store6.configure(text = 'Store6')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image6 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image6.configure(image = self.image6)
        
    def cb_Store7(self):
        self.button_Store7.configure(text = 'ACTIVE')
        self.button_Store7.configure(text = 'Store7')
        save_filename = tkFileDialog.asksaveasfilename(filetypes=self.myFormats ,title="Save the image as...",initialfile='new.gif')
        self.make_GIF(save_filename)
        self.image7 = Tkinter.PhotoImage(file = save_filename) #load the newly saved image on the button 
        self.button_image7.configure(image = self.image7)

    def cb_Load0(self):
        filename = self.load_GIF()
        self.image0 = Tkinter.PhotoImage(file = filename)
        self.button_image0.configure(image = self.image0)
    def cb_Load1(self):
        filename = self.load_GIF()
        self.image1 = Tkinter.PhotoImage(file = filename)
        self.button_image1.configure(image = self.image1)
    def cb_Load2(self):
        filename = self.load_GIF()
        self.image2 = Tkinter.PhotoImage(file = filename)
        self.button_image2.configure(image = self.image2)
    def cb_Load3(self):
        filename = self.load_GIF()
        self.image3 = Tkinter.PhotoImage(file = filename)
        self.button_image3.configure(image = self.image3)
    def cb_Load4(self):
        filename = self.load_GIF()
        self.image4 = Tkinter.PhotoImage(file = filename)
        self.button_image4.configure(image = self.image4)
    def cb_Load5(self):
        filename = self.load_GIF()
        self.image5 = Tkinter.PhotoImage(file = filename)
        self.button_image5.configure(image = self.image5)
    def cb_Load6(self):
        filename = self.load_GIF()
        self.image6 = Tkinter.PhotoImage(file = filename)
        self.button_image6.configure(image = self.image6)
    def cb_Load7(self):
        filename = self.load_GIF()
        self.image7 = Tkinter.PhotoImage(file = filename)
        self.button_image7.configure(image = self.image7)
        
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
        self.Matrix [0][0] = self.selected_color
        setLED = "As0000%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led01(self):
        self.button_LED01.configure(bg = self.selected_color)
        self.Matrix [0][1] = self.selected_color
        setLED = "As0001%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led02(self):
        self.button_LED02.configure(bg = self.selected_color)
        self.Matrix [0][2] = self.selected_color
        setLED = "As0002%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led03(self):
        self.button_LED03.configure(bg = self.selected_color)
        self.Matrix [0][3] = self.selected_color
        setLED = "As0003%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led04(self):
        self.button_LED04.configure(bg = self.selected_color)
        self.Matrix [0][4] = self.selected_color
        setLED = "As0004%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led05(self):
        self.button_LED05.configure(bg = self.selected_color)
        self.Matrix [0][5] = self.selected_color
        setLED = "As0005%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led06(self):
        self.button_LED06.configure(bg = self.selected_color)
        self.Matrix [0][6] = self.selected_color
        setLED = "As0006%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led07(self):
        self.button_LED07.configure(bg = self.selected_color)
        self.Matrix [0][7] = self.selected_color
        setLED = "As0007%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue


    def cb_led10(self):
        self.button_LED10.configure(bg = self.selected_color)
        self.Matrix [1][0] = self.selected_color
        setLED = "As0100%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led11(self):
        self.button_LED11.configure(bg = self.selected_color)
        self.Matrix [1][1] = self.selected_color
        setLED = "As0101%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led12(self):
        self.button_LED12.configure(bg = self.selected_color)
        self.Matrix [1][2] = self.selected_color
        setLED = "As0102%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led13(self):
        self.button_LED13.configure(bg = self.selected_color)
        self.Matrix [1][3] = self.selected_color
        setLED = "As0103%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led14(self):
        self.button_LED14.configure(bg = self.selected_color)
        self.Matrix [1][4] = self.selected_color
        setLED = "As0104%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led15(self):
        self.button_LED15.configure(bg = self.selected_color)
        self.Matrix [1][5] = self.selected_color
        setLED = "As0105%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led16(self):
        self.button_LED16.configure(bg = self.selected_color)
        self.Matrix [1][6] = self.selected_color
        setLED = "As0106%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led17(self):
        self.button_LED17.configure(bg = self.selected_color)
        self.Matrix [1][7] = self.selected_color
        setLED = "As0107%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue


    def cb_led20(self):
        self.button_LED20.configure(bg = self.selected_color)
        self.Matrix [2][0] = self.selected_color
        setLED = "As0200%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led21(self):
        self.button_LED21.configure(bg = self.selected_color)
        self.Matrix [2][1] = self.selected_color
        setLED = "As0201%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led22(self):
        self.button_LED22.configure(bg = self.selected_color)
        self.Matrix [2][2] = self.selected_color
        setLED = "As0202%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led23(self):
        self.button_LED23.configure(bg = self.selected_color)
        self.Matrix [2][3] = self.selected_color
        setLED = "As0203%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led24(self):
        self.button_LED24.configure(bg = self.selected_color)
        self.Matrix [2][4] = self.selected_color
        setLED = "As0204%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led25(self):
        self.button_LED25.configure(bg = self.selected_color)
        self.Matrix [2][5] = self.selected_color
        setLED = "As0205%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led26(self):
        self.button_LED26.configure(bg = self.selected_color)
        self.Matrix [2][6] = self.selected_color
        setLED = "As0206%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led27(self):
        self.button_LED27.configure(bg = self.selected_color)
        self.Matrix [2][7] = self.selected_color
        setLED = "As0207%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue


    def cb_led30(self):
        self.button_LED30.configure(bg = self.selected_color)
        self.Matrix [3][0] = self.selected_color
        setLED = "As0300%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led31(self):
        self.button_LED31.configure(bg = self.selected_color)
        self.Matrix [3][1] = self.selected_color
        setLED = "As0301%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led32(self):
        self.button_LED32.configure(bg = self.selected_color)
        self.Matrix [3][2] = self.selected_color
        setLED = "As0302%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led33(self):
        self.button_LED33.configure(bg = self.selected_color)
        self.Matrix [3][3] = self.selected_color
        setLED = "As0303%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led34(self):
        self.button_LED34.configure(bg = self.selected_color)
        self.Matrix [3][4] = self.selected_color
        setLED = "As0304%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led35(self):
        self.button_LED35.configure(bg = self.selected_color)
        self.Matrix [3][5] = self.selected_color
        setLED = "As0305%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led36(self):
        self.button_LED36.configure(bg = self.selected_color)
        self.Matrix [3][6] = self.selected_color
        setLED = "As0306%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led37(self):
        self.button_LED37.configure(bg = self.selected_color)
        self.Matrix [3][7] = self.selected_color
        setLED = "As0307%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue


    def cb_led40(self):
        self.button_LED40.configure(bg = self.selected_color)
        self.Matrix [4][0] = self.selected_color
        setLED = "As0400%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led41(self):
        self.button_LED41.configure(bg = self.selected_color)
        self.Matrix [4][1] = self.selected_color
        setLED = "As0401%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led42(self):
        self.button_LED42.configure(bg = self.selected_color)
        self.Matrix [4][2] = self.selected_color
        setLED = "As0402%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led43(self):
        self.button_LED43.configure(bg = self.selected_color)
        self.Matrix [4][3] = self.selected_color
        setLED = "As0403%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led44(self):
        self.button_LED44.configure(bg = self.selected_color)
        self.Matrix [4][4] = self.selected_color
        setLED = "As0404%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led45(self):
        self.button_LED45.configure(bg = self.selected_color)
        self.Matrix [4][5] = self.selected_color
        setLED = "As0405%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led46(self):
        self.button_LED46.configure(bg = self.selected_color)
        self.Matrix [4][6] = self.selected_color
        setLED = "As0406%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led47(self):
        self.button_LED47.configure(bg = self.selected_color)
        self.Matrix [4][7] = self.selected_color
        setLED = "As0407%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue


    def cb_led50(self):
        self.button_LED50.configure(bg = self.selected_color)
        self.Matrix [5][0] = self.selected_color
        setLED = "As0500%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led51(self):
        self.button_LED51.configure(bg = self.selected_color)
        self.Matrix [5][1] = self.selected_color
        setLED = "As0501%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led52(self):
        self.button_LED52.configure(bg = self.selected_color)
        self.Matrix [5][2] = self.selected_color
        setLED = "As0502%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led53(self):
        self.button_LED53.configure(bg = self.selected_color)
        self.Matrix [5][3] = self.selected_color
        setLED = "As0503%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led54(self):
        self.button_LED54.configure(bg = self.selected_color)
        self.Matrix [5][4] = self.selected_color
        setLED = "As0504%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led55(self):
        self.button_LED55.configure(bg = self.selected_color)
        self.Matrix [5][5] = self.selected_color
        setLED = "As0505%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led56(self):
        self.button_LED56.configure(bg = self.selected_color)
        self.Matrix [5][6] = self.selected_color
        setLED = "As0506%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led57(self):
        self.button_LED57.configure(bg = self.selected_color)
        self.Matrix [5][7] = self.selected_color
        setLED = "As0507%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led60(self):
        self.button_LED60.configure(bg = self.selected_color)
        self.Matrix [6][0] = self.selected_color
        setLED = "As0600%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led61(self):
        self.button_LED61.configure(bg = self.selected_color)
        self.Matrix [6][1] = self.selected_color
        setLED = "As0601%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led62(self):
        self.button_LED62.configure(bg = self.selected_color)
        self.Matrix [6][2] = self.selected_color
        setLED = "As0602%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led63(self):
        self.button_LED63.configure(bg = self.selected_color)
        self.Matrix [6][3] = self.selected_color
        setLED = "As0603%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led64(self):
        self.button_LED64.configure(bg = self.selected_color)
        self.Matrix [6][4] = self.selected_color
        setLED = "As0604%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led65(self):
        self.button_LED65.configure(bg = self.selected_color)
        self.Matrix [6][5] = self.selected_color
        setLED = "As0605%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led66(self):
        self.button_LED66.configure(bg = self.selected_color)
        self.Matrix [6][6] = self.selected_color
        setLED = "As0606%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led67(self):
        self.button_LED67.configure(bg = self.selected_color)
        self.Matrix [6][7] = self.selected_color
        setLED = "As0607%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def cb_led70(self):
        self.button_LED70.configure(bg = self.selected_color)
        self.Matrix [7][0] = self.selected_color
        setLED = "As0700%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led71(self):
        self.button_LED71.configure(bg = self.selected_color)
        self.Matrix [7][1] = self.selected_color
        setLED = "As0701%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led72(self):
        self.button_LED72.configure(bg = self.selected_color)
        self.Matrix [7][2] = self.selected_color
        setLED = "As0702%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led73(self):
        self.button_LED73.configure(bg = self.selected_color)
        self.Matrix [7][3] = self.selected_color
        setLED = "As0703%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led74(self):
        self.button_LED74.configure(bg = self.selected_color)
        self.Matrix [7][4] = self.selected_color
        setLED = "As0704%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led75(self):
        self.button_LED75.configure(bg = self.selected_color)
        self.Matrix [7][5] = self.selected_color
        setLED = "As0705%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led76(self):
        self.button_LED76.configure(bg = self.selected_color)
        self.Matrix [7][6] = self.selected_color
        setLED = "As0706%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue
    def cb_led77(self):
        self.button_LED77.configure(bg = self.selected_color)
        self.Matrix [7][7] = self.selected_color
        setLED = "As0707%03i%03i%03iz" % ( int(self.selected_color[1:3],16), int(self.selected_color[3:5],16),  int(self.selected_color[5:7],16) )
        self.q.put(setLED) # write a string to the serial port via tx_queue

    def make_GIF(self,filename):
        img = Image.new('RGB',(100, 100))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 101,101), fill=(255,255,255))
        for s in self.box_coord:
            #print"coord = %16s X=%02i, Y=%02i  Matrix= %s" % (str(s), (s[3]/12)-1, (s[2]/12)-1, str(self.Matrix[(s[3]/12)-1][(s[2]/12)-1]) )
            draw.rectangle( s , fill=self.Matrix[(s[3]/12)-1][(s[2]/12)-1] )
        img.save(filename, 'GIF', transparency=0)

    def load_GIF(self):
        file_path = tkFileDialog.askopenfilename(filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        img = Image.open(file_path)
        rgb_pix = img.convert('RGB')
        #r,g,b = rgb_pix.getpixel((5,5))
        #print r,g,b
        gifMatrix = [['#ffffff' for x in xrange(8)] for x in xrange(8)]
        for s in self.box_coord:
            r,g,b = rgb_pix.getpixel((s[3]-4,s[2]-4)) # center of each box
            #print"load gif  coord = %16s X=%02i, Y=%02i  Matrix= #%02X%02X%02X" % (str(s), s[3]-4, s[2]-4, r,g,b )
            hexstring = ('#%02X%02X%02X'%(r,g,b))
            gifMatrix[(s[3]/12)-1][(s[2]/12)-1] =  hexstring
        self.update_led_buttons(gifMatrix)
        self.send_matrix(gifMatrix)
        return file_path

    def send_matrix(self,matrix):
        for s in self.box_coord:
            x = (s[3]/12)-1
            y = (s[2]/12)-1
            hexstring = matrix[x][y]
            r = int(hexstring[1:3],16)
            g = int(hexstring[3:5],16)
            b = int(hexstring[5:7],16)
            
            setLED = "As%02i%02i%03i%03i%03iz" % ( x,y,r,g,b )
            #print"send matrix coord = %16s X=%02i, Y=%02i  Matrix= #%02X%02X%02X  %s"% (str(s), x, y, r, g, b, setLED )
            self.q.put(setLED) # write a string to the serial port via tx_queue



    def update_led_buttons(self,matrix):
        self.button_LED00.configure(bg = matrix[0][0])
        self.button_LED01.configure(bg = matrix[0][1])
        self.button_LED02.configure(bg = matrix[0][2])
        self.button_LED03.configure(bg = matrix[0][3])
        self.button_LED04.configure(bg = matrix[0][4])
        self.button_LED05.configure(bg = matrix[0][5])
        self.button_LED06.configure(bg = matrix[0][6])
        self.button_LED07.configure(bg = matrix[0][7])

        self.button_LED10.configure(bg = matrix[1][0])
        self.button_LED11.configure(bg = matrix[1][1])
        self.button_LED12.configure(bg = matrix[1][2])
        self.button_LED13.configure(bg = matrix[1][3])
        self.button_LED14.configure(bg = matrix[1][4])
        self.button_LED15.configure(bg = matrix[1][5])
        self.button_LED16.configure(bg = matrix[1][6])
        self.button_LED17.configure(bg = matrix[1][7])

        self.button_LED20.configure(bg = matrix[2][0])
        self.button_LED21.configure(bg = matrix[2][1])
        self.button_LED22.configure(bg = matrix[2][2])
        self.button_LED23.configure(bg = matrix[2][3])
        self.button_LED24.configure(bg = matrix[2][4])
        self.button_LED25.configure(bg = matrix[2][5])
        self.button_LED26.configure(bg = matrix[2][6])
        self.button_LED27.configure(bg = matrix[2][7])

        self.button_LED30.configure(bg = matrix[3][0])
        self.button_LED31.configure(bg = matrix[3][1])
        self.button_LED32.configure(bg = matrix[3][2])
        self.button_LED33.configure(bg = matrix[3][3])
        self.button_LED34.configure(bg = matrix[3][4])
        self.button_LED35.configure(bg = matrix[3][5])
        self.button_LED36.configure(bg = matrix[3][6])
        self.button_LED37.configure(bg = matrix[3][7])

        self.button_LED40.configure(bg = matrix[4][0])
        self.button_LED41.configure(bg = matrix[4][1])
        self.button_LED42.configure(bg = matrix[4][2])
        self.button_LED43.configure(bg = matrix[4][3])
        self.button_LED44.configure(bg = matrix[4][4])
        self.button_LED45.configure(bg = matrix[4][5])
        self.button_LED46.configure(bg = matrix[4][6])
        self.button_LED47.configure(bg = matrix[4][7])

        self.button_LED50.configure(bg = matrix[5][0])
        self.button_LED51.configure(bg = matrix[5][1])
        self.button_LED52.configure(bg = matrix[5][2])
        self.button_LED53.configure(bg = matrix[5][3])
        self.button_LED54.configure(bg = matrix[5][4])
        self.button_LED55.configure(bg = matrix[5][5])
        self.button_LED56.configure(bg = matrix[5][6])
        self.button_LED57.configure(bg = matrix[5][7])

        self.button_LED60.configure(bg = matrix[6][0])
        self.button_LED61.configure(bg = matrix[6][1])
        self.button_LED62.configure(bg = matrix[6][2])
        self.button_LED63.configure(bg = matrix[6][3])
        self.button_LED64.configure(bg = matrix[6][4])
        self.button_LED65.configure(bg = matrix[6][5])
        self.button_LED66.configure(bg = matrix[6][6])
        self.button_LED67.configure(bg = matrix[6][7])

        self.button_LED70.configure(bg = matrix[7][0])
        self.button_LED71.configure(bg = matrix[7][1])
        self.button_LED72.configure(bg = matrix[7][2])
        self.button_LED73.configure(bg = matrix[7][3])
        self.button_LED74.configure(bg = matrix[7][4])
        self.button_LED75.configure(bg = matrix[7][5])
        self.button_LED76.configure(bg = matrix[7][6])
        self.button_LED77.configure(bg = matrix[7][7])

    
    def clear_colorArray(self):
        # Creates a list holding a 8x8 matrix lists, initialized to 0
        Matrix = [['#000000' for x in xrange(8)] for x in xrange(8)]
        return Matrix

def main():
    """ MAIN PROGRAM"""
    root = Tkinter.Tk(  )
    
    # Set up the GUI part
    gui = GuiPart(root,tx_queue)


    serThread1 = threading.Thread(target=Serial, args=(tx_queue,) )
    serThread1.start()

    root.mainloop()


if __name__ == "__main__":
    main()
    



