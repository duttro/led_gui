## 032815 initial file, loads and sends wave files
## 040115 can transmit to arduino but sound shudders, it was the parsePacket routine on the arduino side
## 040315 adding open file name and play commands
## 040315 Sf sound filename working
## 040315 Sp sound play working 
## 060315 changing the way the sounds are handled, just playing wave files
## 060813 added load and play buttons, 
## 060813 added creation of sound.GIF files for dnd on timeline
## 062515 improved makeGif, now file name is in the box
## 070715 creates a .dat file containing the CMD and short file name, also sends to arduino
## 072815 added second Queue
## 080115 sound commands will use ether port 81
## 081915 the wav files must be formatted as 16,000kHz, mono; (stereo OR will sound slow)
## 082515 now the long filename is sent to the arduino

import os
import shutil
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
font = ImageFont.truetype("arial.ttf", 10)



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
          
    def __init__(self,win, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b):
        ##############################################################3
        print"SOUND TAB GUI init"
        self.q1 = tx_queue2a
        self.q1 = tx_queue2b
        
        #######################################
        # Set up the GUI                      #
        #######################################
        # TOP row of buttons
        self.button_Load0 = Tkinter.Button(win, text = "Load 0", command = self.cb_S_L0, compound="left")
        self.button_Load0.grid(row=0, column=0)
        
        ######################################
        self.button_Play0 = Tkinter.Button(win, text = "Play 0", command = self.cb_S_P0, compound="left")
        self.button_Play0.grid(row=1, column=0)
        
        #######################################
    
    def cb_S_L0(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] ,title="Save the image as...",initialfile='new.gif')
          file_path_pieces = file_path.split('/');
          path_depth = len(file_path_pieces); 
          arduino_path = file_path_pieces[path_depth-2] + "/" + file_path_pieces[path_depth-1];
          arduino_path_wav = arduino_path.replace('.gif','.wav');
          self.make_GIF_fromSoundPath(file_path)
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File file_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0));
          print"SOUND_TAB: Sound:File arduino_path_wav: %s" % (arduino_path_wav);
          
          msg = buffer(b"80SoL0") + arduino_path_wav.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q1.put(msg); # send array
          
          print("Writing SDAT file in %s \n" %(file_path.replace('.wav','.dat')))
          Sdat = open(file_path.replace('.wav','.dat'), "w+");
          Sdat.write(msg);
          #Close opened file
          Sdat.close()

          # copy the file to its short name
          #assert not os.path.isabs(file_path)
          try:
            shutil.copy(file_path, short_file_path) # may not be needed
          except :
            # just on general principles, although we don't
            # expect this branch to be taken in this case
            pass
    
    
    
    
    def cb_S_L1(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"80SoL1") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q1.put(msg); # send array
    
    def cb_S_L2(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"80SoL2") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q1.put(msg); # send array
          
    def cb_S_L3(self):  ##Sound Load0
          file_path = tkFileDialog.askopenfilename(initialdir=('../sounds/'),filetypes=[("Sound Files","*.wav"),("WAV",'*.wav')] )
          windows_path = file_path.split('/');
          path_depth = len(windows_path);
          self.arduino_path = "/sounds/" + windows_path[path_depth-1];
          
          f0 = open(file_path, "rb").read();
          print"SOUND_TAB: Sound:File windows_path: FOUND DAT FILE %s" % (file_path);
          print"SOUND_TAB: Sound:File the length of file is %i" % (len(f0))
          print"SOUND_TAB: Sound:File arduino_path: %s" % (self.arduino_path)
          
          msg = buffer(b"80SoL3") + self.arduino_path.encode('ascii', 'ignore'); # convert from 16bit to 8bit ascii
          self.q1.put(msg); # send array
    

    
    
    def cb_S_P0(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"80SpP0");
          self.q1.put(msg); # send array    
    
    def cb_S_P1(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"80SpP1");
          self.q1.put(msg); # send array

    def cb_S_P2(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"80SpP2");
          self.q1.put(msg); # send array

    def cb_S_P3(self):  ## Sound Play0
          print"SOUND_TAB: Sound:Play %s" % (self.arduino_path)
          msg = buffer(b"80SpP3");
          self.q1.put(msg); # send array          
    
    def make_GIF_fromSoundPath(self,filename):
        print filename
        filename_split = filename.split('/');
        depth = len(filename_split);
        label = "/sounds/" + filename_split[depth-1];
        
        # create a empty box 100 x 100
        MAX_W, MAX_H = 100, 100
        img = Image.new('RGB',(MAX_W, MAX_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
