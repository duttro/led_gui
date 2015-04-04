## 032815 initial file, loads and sends wave files
## 040115 can transmit to arduino but sound shudders, it was the parsePacket routine on the arduino side
## 040315 adding open file name and play commands
## 040315 Sf sound filename working
## 040315 Sp sound play working 



import pdb
import time
from time import sleep
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
## my imported classes
from Timeline_TAB import *


class SOUND_TAB:
          
    def __init__(self,win, tx_queue):
        ##############################################################3
        print"SOUND TAB GUI init"
        self.q = tx_queue
        
        #######################################
        # Set up the GUI                      #
        #######################################
        # TOP row of buttons
        self.button_Load0 = Tkinter.Button(win, text = "Wave 0", command = self.cb_Load0, compound="left")
        self.button_Load0.grid(row=0, column=0)
        
        self.button_Play0 = Tkinter.Button(win, text = "Play 0", command = self.cb_Play0, compound="left")
        self.button_Play0.grid(row=0, column=1)
  
    def cb_Load0(self):  

          file_path = tkFileDialog.askopenfilename(initialdir=('../sound_files/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          arduino_path = windows_path[path_depth-1] + '\0';
          f = open(file_path, "rb").read();
          
          print"SOUND_TAB: windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: the length of file is %i" % (len(f))
          print"SOUND_TAB: arduino_path: %s" % (arduino_path)
          
          msg = buffer(b"Sf") + arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q.put(msg); # send array
    
    def cb_Play0(self):  
          msg = buffer(b"Sp"); 
          self.q.put(msg); # send array    
          

