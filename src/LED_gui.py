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
## 012915 added heartbeat to serial class
## 013115 tempBuffer now and array of int values RGB for each pixel
## 020515 updated make_GIF_fromBigMatrix
## 020615 working on updating load save buttons
## 021415 load, store and orientation fixed
## 021715 class Assembly_TAB moved into it's own file Assembly_TAB.py
## 021715 class LED_TAB moved into it's own file LED_TAB.py
## 021915 new defs in Assemblt_TAB not working yet
## 022515 worked on ShowObjectDicts_top_canvas(): in Assembly_TAB, not workin yet
## 030115 changed file name to led_GUI.py
## 030115 testing git update
## 030715 working on seq out
## 030715 happy to report assembly_tab anaimate canvase1 works
## 031814 changed class name to TIMELINE
## 032815 added SOUND_TAB to access wav files
## 062415 fixed dnd in DraggedDnd.py
## 062615 Now the file path is now stored in the object, it can be access by using the object identifier
## 062615 the object variables and listed in the DraggedDnd.py file
## 062615 The dictionary now only stores a name and the xy coord of the object
## 062615 Everything is working
## 072815 added second Q and renamed Q=Q1; Q1=animate canvas1; Q2=animate canvas2;
## 072915 canvas1 transmits to 192.168.1.177 and canvas2 transmits to 192.168.1.178
## 080715 now commands/data is now sent to a separate UDP port stored in the DAT file for each display type
## 080715 all commands are a uniform size (4) in characters, if unused pad with decimal pts
## 081415 each device now has a unique IP address now stored in Timeline_TAB class
## 081615 problem with multiple units attached; when multiple units attached each device must have a unique MAX address
## 082515 long file names now work for sound


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
from DraggedDnd import *
from CanvasDnd import *
from LED_TAB import *
from SOUND_TAB import *
from Timeline_TAB import *

# Create the queue
tx_queue1a = Queue.Queue()
tx_queue2a = Queue.Queue()
tx_queue1b = Queue.Queue()
tx_queue2b = Queue.Queue()

class Serial:
     
    def __init__(self, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b, timeline_class):
        ############################################################
        self._go_attribute = 1
        print"Commands sent over ether...";
        print("Always using port 80 for all COMS");
        print("Using address %s\n" % (timeline_class.E1a_v.get()));
        print("Using address %s\n" % (timeline_class.E1b_v.get()));
        print("Using address %s\n" % (timeline_class.E2a_v.get()));
        print("Using address %s\n" % (timeline_class.E2b_v.get()));
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
        
        idle_counter = 0
        heartbeat_count = 0
        print"idle counter set to 0"
        
        while (self.go_attribute):   
            #####################################################################
            while tx_queue1a.qsize(  ):
              try:
                 TXmsg1a = tx_queue1a.get( )
                 print ("LED_GUI: %s ; port= %s CMD= %s sending msg1a \n"%(timeline_class.E1a_v.get(),"80",TXmsg1a[2:6]));
                 sock.sendto(TXmsg1a[2:], (timeline_class.E1a_v.get(), 80 ))
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass
            ######################################################################
            while tx_queue1b.qsize(  ):
              try:
                 TXmsg1b = tx_queue1b.get( )
                 print ("LED_GUI: %s ; port= %s CMD= %s sending msg1b \n"%(timeline_class.E1b_v.get(),"80",TXmsg1b[2:6]));
                 sock.sendto(TXmsg1b[2:], (timeline_class.E1b_v.get(), 80 ))
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass
            ######################################################################
            while tx_queue2a.qsize(  ):
              try:
                 TXmsg2a = tx_queue2a.get( )
                 print ("LED_GUI: %s ; port= %s CMD= %s sending msg2a \n"%(timeline_class.E2a_v.get(),"80",TXmsg2a[2:6]));
                 sock.sendto(TXmsg2a[2:], (timeline_class.E2a_v.get(), 80 ))
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass
            ######################################################################
            while tx_queue2b.qsize(  ):
              try:
                 TXmsg2b = tx_queue2b.get( )
                 print ("LED_GUI: %s ; port= %s CMD= %s sending msg2b \n"%(timeline_class.E2b_v.get(),"80",TXmsg2b[2:6]));
                 sock.sendto(TXmsg2b[2:], (timeline_class.E2b_v.get(), 80 ))
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass
            ######################################################################     
            time.sleep(.01)
            if idle_counter < 2000:
               idle_counter = idle_counter +1
            else:
               idle_counter = 0
               
               # transmit the heartbeat counter
               if heartbeat_count == 99:
                  heartbeat_count = 00
               else:   
                  heartbeat_count = heartbeat_count +1
                  
               # TX message
               HBmsg80 = '80Hb'+'{:02d}'.format(heartbeat_count);
               # IP address Q1a
               # IP address Q1b
               # IP address Q2a
               # IP address Q2b
               print ("LED_GUI: %s %s %s %s; port= %s CMD= %s  \n"%(timeline_class.E1a_v.get(),timeline_class.E1b_v.get(),timeline_class.E2a_v.get(),timeline_class.E2b_v.get(),HBmsg80[0:2],HBmsg80[2:6]));
               sock.sendto(HBmsg80[2:], (timeline_class.E1a_v.get(), int(HBmsg80[0:2])));
               sock.sendto(HBmsg80[2:], (timeline_class.E1b_v.get(), int(HBmsg80[0:2])));
               sock.sendto(HBmsg80[2:], (timeline_class.E2a_v.get(), int(HBmsg80[0:2])));
               sock.sendto(HBmsg80[2:], (timeline_class.E2b_v.get(), int(HBmsg80[0:2])));

              
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
        
        root = Tkinter.Tk()
        # use width x height + x_offset + y_offset (no spaces!)
        #root.geometry("%dx%d+%d+%d" % (300, 200, 100, 50))
        root.title('Top View of the ttk.Notebook')
        
        nb = ttk.Notebook(root)
        nb.pack(fill='both', expand='yes')
        
        # create a child frame for each page
        f1 = Tkinter.Frame()
        f2 = Tkinter.Frame()
        f3 = Tkinter.Frame()
        
        # create the pages
        nb.add(f1, text='TIMELINE')
        nb.add(f2, text='LED MATRIX')
        nb.add(f3, text='SOUND')
        
        # draw the tabbed pages
        timeline_tab = Timeline_TAB(f1, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b)
        led_tab      =      LED_TAB(f2, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b)
        sound_tab    =    SOUND_TAB(f3, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b)
        
        # start the queue thread
        serThread1 = threading.Thread(target=Serial, args=(tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b, timeline_tab,))
        serThread1.start()
        
        
        root.mainloop()

if __name__ == "__main__":
    main()   



