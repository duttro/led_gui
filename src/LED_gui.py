############################################################################################
## 061014 adding drawPixelMessage, sends the whole array at once, testing is the next step
## 061214 testing the full page tx mode
## 061414 testing the full image recv, working
##        must add load matrix on store, done
##        add file name box
##        added animation button to cycle through all image tiles, working
##        add application exit
## 061614 added an entry box for delay between animation loop switching
## 061814 working on killing app, not working yet
## 061914 adding thread stop, not working, can close the app window now
## 062414 modifying code to kill the serial thread, seems to work on the esc key but not the other methods yet
## 070314 adding 3 tabs
## 081014 merging the dnd function as external file, my first time, merged
## 100214 image file path not getting passed so button image doesn't show up right now,fixed
## 100314 now the button's image name is stored in the dictionary as well
##        added def cb_animate_canvas but not done
## 112614 changed name to LED_gui.py
## 112814 added update_file_LED_DAT to create a data file for each buttons gif
## 112814 added function send_array_as_asc_each_pixel_rgb to transmit byte array
## 112914 load_GIF_return_as_array needs to be modified to load the .dat file into matrix
## 011715 many updates
## 012915 added heartbeat to seraial class
## 013115 tempBuffer now and array of int values rgb for each pixel
## 020515 updated make_GIF_fromBigMatrix
## 020615 working on updating load save buttons
## 021415 load, store and orientation fixed
## 021715 class Assembly_TAB moved into it's own file Assembly_TAB.py
## 021715 class LED_TAB moved into it's own file LED_TAB.py
## 021915 new defs in Assemblt_TAB not working yet
## 022515 worked on ShowObjectDicts_top_canvas(): in Assembly_TAB, not workin yet
## 030115 changed file name to led_GUI.py
## 030115 testing git update

import pdb
import time
import serial
import socket
import string
import threading
import Queue
from PIL import Image, ImageDraw
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
from dnd import *
from LED_TAB import *
from Assembly_TAB import *





# Create the queue
tx_queue = Queue.Queue( )

class Serial:
     
    def __init__(self,tx_queue):
        ############################################################
        self._go_attribute = 1
        print"Commands sent over ether...";
        UDP_IP = "192.168.1.177"
        UDP_PORT = 88
        print "UDP target IP:", UDP_IP
        print "UDP target port:", UDP_PORT
        sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
        idle_counter = 0
        heartbeat_count = 0
        print"idle counter set to 0"
        
        while (self.go_attribute):   

            while tx_queue.qsize(  ):
              
              try:
                 #self.master = master
                 TXmsg = tx_queue.get( )
                 #print "sending msg %s" % (TXmsg)

                 sock.sendto(TXmsg, (UDP_IP, UDP_PORT))
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass

            time.sleep(.01)
            if idle_counter < 2000:
               idle_counter = idle_counter +1
            else:
               idle_counter = 0

            if idle_counter == 2000:
               heartbeat_count = heartbeat_count +1
               TXmsg = "Hb"
               print"sending HeartBeat message " + TXmsg
               sock.sendto(TXmsg, (UDP_IP, UDP_PORT))


              
    @property
    # the go attribute is used to shut the serial class down
    def go_attribute(self):
            #print "accessed the go attribute"
            return self._go_attribute

    @go_attribute.setter
    def go_attribute(self,value):
            print "modified the go attribute"
            self._go_attribute = value


        


def main():
        def kill_it_all(self,win):
            print"executing kill all"
            Serial.go_attribute = 0
            win.destroy()
        
    # start the queue thread
        serThread1 = threading.Thread(target=Serial, args=(tx_queue,))
        serThread1.start()

        root = Tkinter.Tk()
        # use width x height + x_offset + y_offset (no spaces!)
        #root.geometry("%dx%d+%d+%d" % (300, 200, 100, 50))
        root.title('Top View of the ttk.Notebook')

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

##        # create a Text widget with a Scrollbar attached
##        txt = ScrolledText(win, undo=True)
##        txt['font'] = ('consolas', '12')
##        image_filepath=''
        
        nb = ttk.Notebook(root)
        nb.pack(fill='both', expand='yes')
        
        # create a child frame for each page
        f1 = Tkinter.Frame()
        f2 = Tkinter.Frame()
        f3 = Tkinter.Frame()
        
        # create the pages
        nb.add(f1, text='LED MATRIX')
        nb.add(f2, text='ASSEMBLY')
        nb.add(f3, text='page3')
        
        # draw the pages
        LED_TAB(f1,tx_queue)
        Assembly_TAB(f2, tx_queue)
        
        root.mainloop()

if __name__ == "__main__":
    main()   



