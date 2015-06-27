## 032815 initial file, loads and sends wave files
## 040115 can transmit to arduino but sound shudders, it was the parsePacket routine on the arduino side
## 040315 adding open file name and play commands
## 040315 Sf sound filename working
## 040315 Sp sound play working 
## 060315 changing the way the sounds are handled, just playing wave files
## 060813 added load and play buttons, 
## 060813 added creation of sound.GIF files for dnd on timeline
## 062515 improved makeGif, now file name is in the box

import os.path
import struct
import array
import math
import winsound

import pdb
import time
from time import sleep
import serial
import socket
import string
import threading
import Queue

from PIL import Image, ImageDraw, ImageFont
import textwrap
#font = ImageFont.load("arial.pil")
font = ImageFont.truetype("arial.ttf", 15)



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
        self.button_Load0 = Tkinter.Button(win, text = "Load 0", command = self.cb_S_L0, compound="left")
        self.button_Load0.grid(row=0, column=0)
        
        self.button_Load1 = Tkinter.Button(win, text = "Load 1", command = self.cb_S_L1, compound="left")
        self.button_Load1.grid(row=0, column=1)
        
        self.button_Load2 = Tkinter.Button(win, text = "Load 2", command = self.cb_S_L2, compound="left")
        self.button_Load2.grid(row=0, column=2)
        
        self.button_Load3 = Tkinter.Button(win, text = "Load 3", command = self.cb_S_L3, compound="left")
        self.button_Load3.grid(row=0, column=3)
        ######################################
        self.button_Play0 = Tkinter.Button(win, text = "Play 0", command = self.cb_S_P0, compound="left")
        self.button_Play0.grid(row=1, column=0)
        
        self.button_Play1 = Tkinter.Button(win, text = "Play 1", command = self.cb_S_P1, compound="left")
        self.button_Play1.grid(row=1, column=1)
        
        self.button_Play2 = Tkinter.Button(win, text = "Play 2", command = self.cb_S_P2, compound="left")
        self.button_Play2.grid(row=1, column=2)
        
        self.button_Play3 = Tkinter.Button(win, text = "Play 3", command = self.cb_S_P3, compound="left")
        self.button_Play3.grid(row=1, column=3)
        #######################################
    def cb_S_l(self):  ## Sound Play Length
          print"SOUND_TAB: Sound:Play Length %s" % (self.arduino_path)
          msg = buffer(b"Sl") + "2000";
          self.q.put(msg); # send array
          
    def cb_S_s(self):  ## Sound Seek
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"Ss") + "2048";
          self.q.put(msg); # send array
          
          
    
    
    
    
    def cb_S_L0(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] ,title="Save the image as...",initialfile='new.gif')
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          self.make_GIF_fromSoundPath(file_path)
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"SoL0") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q.put(msg); # send array
    
    def cb_S_L1(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"SoL1") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q.put(msg); # send array
    
    def cb_S_L2(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"SoL2") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q.put(msg); # send array
          
    def cb_S_L3(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"SoL3") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q.put(msg); # send array
    

    
    
    def cb_S_P0(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"SpP0");
          self.q.put(msg); # send array    
    
    def cb_S_P1(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"SpP1");
          self.q.put(msg); # send array

    def cb_S_P2(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"SpP2");
          self.q.put(msg); # send array

    def cb_S_P3(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"SpP3");
          self.q.put(msg); # send array          
    
    def make_GIF_fromSoundPath(self,filename):
        print filename
        filename_split = filename.split('/');
        depth = len(filename_split);
        label = "/sounds/" + filename_split[depth-1];
        
        # create a empty box 100 x 100
        MAX_W, MAX_H = 100, 100
        img = Image.new('RGB',(MAX_W, MAX_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        #draw.rectangle((0, 0, 101,101), fill=(255,255,255))
        
        # write the sound filename in the box
        #draw.text ( (10,10), para, font=font, fill="red" )
        para = textwrap.wrap(label, width=10)
        current_h, pad = 00, 10
        for line in para:
          w, h = draw.textsize(line, font=font)
          draw.text(((MAX_W - w) / 2, current_h), line, font=font)
          current_h += h + pad

        # save the gif file
        img.save(filename.replace('.wav', '.GIF'), 'GIF', transparency=0)
        return 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
