## 021715 class Assembly_TAB moved to it's own file Assembly_TAB.py
## 021915 added def   for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_middle_canvas for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_bottom_canvas for transmitting sending all object on canvas
## 021915 new defs in Assemblt_TAB not working yet
## 030715 assembly_tab animate canvas 1 works
## 031814 changed class name to TIMELINE
## 062915 Timeline_TAB.py added a incrementing cursor that sweeps across canvas 1
## 063015 added dictionary object position cmp to cursor_1
## 072815 added a second Q
## 072915 working on sorting the dictionary, not working yet
## 080915 working around line 159, grouping buttons on a canvas
## 081115 trying to make the the ip addresses readable from outside Timeline_TAB, not working



import Tkdnd
from Tkinter import *
import Tkinter
import Tkinter, tkFileDialog, Dialog
import Queue
import operator # to sort the dictionary
import time
import string # to support StringVar()

##############
## my classes
from DraggedDnd import *
from CanvasDnd import *
from LED_TAB import *

class Timeline_TAB(object):
    
    
    def __init__(self,win, tx_queue1a, tx_queue1b, tx_queue2a, tx_queue2b):    
      
      
      def on_dnd_start(Event):
        """
        This is invoked by InitiationObject to start the drag and drop process
        """
        #Create an object to be dragged
        ThingToDrag = Dragged(self.selected_button_image_filepath)
        #print"... the ThingToDrag is";
        #print ThingToDrag
        #print("PASSING image file path to CANVAS DND = %s"%(CanvasDnd.image_filepath))
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

      def animate_canvas():
        
        y_top    = 0;
        y_bottom = 110;
        
        TargetWidget_TargetObject1a.create_line( 0, y_top , 0, y_bottom , fill ="red", tags="cursor_1" );
        TargetWidget_TargetObject1a.tag_raise("cursor_1")
        TargetWidget_TargetObject1a.update()
        TargetWidget_TargetObject1b.create_line( 0, y_top , 0, y_bottom , fill ="red", tags="cursor_1" );
        TargetWidget_TargetObject1b.tag_raise("cursor_1")
        TargetWidget_TargetObject1b.update()
        
        TargetWidget_TargetObject2a.create_line( 0, y_top , 0, y_bottom , fill ="red", tags="cursor_2" );
        TargetWidget_TargetObject2a.tag_raise("cursor_2")
        TargetWidget_TargetObject2a.update()
        TargetWidget_TargetObject2b.create_line( 0, y_top , 0, y_bottom , fill ="red", tags="cursor_2" );
        TargetWidget_TargetObject2b.tag_raise("cursor_2")
        TargetWidget_TargetObject2b.update()
        
        # scan through objects on canvas and activate each one as the cursor touches it
        for cursor1_x in range(0 , 499): # sweep cursor range
          #print cursor1_x
          TargetWidget_TargetObject1a.coords("cursor_1",(cursor1_x,y_top,cursor1_x,y_bottom))
          TargetWidget_TargetObject1a.tag_raise("cursor_1")
          TargetWidget_TargetObject1a.update()
          
          TargetWidget_TargetObject1b.coords("cursor_1",(cursor1_x,y_top,cursor1_x,y_bottom))
          TargetWidget_TargetObject1b.tag_raise("cursor_1")
          TargetWidget_TargetObject1b.update()
          
          TargetWidget_TargetObject2a.coords("cursor_2",(cursor1_x,y_top,cursor1_x,y_bottom))
          TargetWidget_TargetObject2a.tag_raise("cursor_2")
          TargetWidget_TargetObject2a.update()
          
          TargetWidget_TargetObject2b.coords("cursor_2",(cursor1_x,y_top,cursor1_x,y_bottom))
          TargetWidget_TargetObject2b.tag_raise("cursor_2")
          TargetWidget_TargetObject2b.update()
          
          time.sleep(0.025)
          
          if len(TargetWidget_TargetObject1a.ObjectDict) > 0:
            for Name, Object in TargetWidget_TargetObject1a.ObjectDict.iteritems():
               if Object[1][0] == cursor1_x:
                 # the cursor is at current objects position
                 print("animate canvas1a %s , %s" % (Object[1],Object[0].image_filepath));
                 msg = Object[0].dat_array
                 print len(msg)
                 #print msg
                 self.E1a_q.put(msg) # send array
          
          if len(TargetWidget_TargetObject1b.ObjectDict) > 0:
            for Name, Object in TargetWidget_TargetObject1b.ObjectDict.iteritems():
               if Object[1][0] == cursor1_x:
                 # the cursor is at current objects position
                 print("animate canvas1b %s , %s" % (Object[1],Object[0].image_filepath));
                 msg = Object[0].dat_array
                 print len(msg)
                 #print msg
                 self.E1b_q.put(msg) # send array
          
          if len(TargetWidget_TargetObject2a.ObjectDict) > 0:        
            for Name2,Object2 in TargetWidget_TargetObject2a.ObjectDict.iteritems():
               if Object2[1][0] == cursor1_x:
                 # the cursor is at current objects position
                 print("animate canvas2a %s , %s" % (Object2[1],Object2[0].image_filepath));
                 msg2 = Object2[0].dat_array
                 print len(msg2)
                 #print msg2
                 self.E2a_q.put(msg2) # send array
          
          if len(TargetWidget_TargetObject2b.ObjectDict) > 0:        
            for Name2,Object2 in TargetWidget_TargetObject2b.ObjectDict.iteritems():
               if Object2[1][0] == cursor1_x:
                 # the cursor is at current objects position
                 print("animate canvas2b %s , %s" % (Object2[1],Object2[0].image_filepath));
                 msg2 = Object2[0].dat_array
                 print len(msg2)
                 #print msg2
                 self.E2b_q.put(msg2) # send array
      

      def ShowObjectDicts_top_canvas():
        ## list object on the top canvas listed in the dictionary             
        sorted_ObjectDict1a = sorted(TargetWidget_TargetObject1a.ObjectDict.iteritems(), key=lambda (name,object): object[1]) # sort by x position
        sorted_ObjectDict1b = sorted(TargetWidget_TargetObject1b.ObjectDict.iteritems(), key=lambda (name,object): object[1]) # sort by x position
        print""
        print"Printing the sorted TOP dictionary"
        print"----------------------------------"
        
        if len(sorted_ObjectDict1a) > 0:
            for Name,Object in sorted_ObjectDict1a:
                print"%s %s %s" % (Name,Object[1],Object[0].image_filepath)
        else:
            print "    <1a empty>" 
        
        if len(sorted_ObjectDict1b) > 0:
            for Name,Object in sorted_ObjectDict1b:
                print"%s %s %s" % (Name,Object[1],Object[0].image_filepath)
        else:
            print "    <1b empty>"
        
      def ShowObjectDicts_middle_canvas():
        ## list object on the top canvas listed in the dictionary
        sorted_ObjectDict2a = sorted(TargetWidget_TargetObject2a.ObjectDict.iteritems(), key=lambda (name,object): object[1]) # sort by x position
        sorted_ObjectDict2b = sorted(TargetWidget_TargetObject2b.ObjectDict.iteritems(), key=lambda (name,object): object[1]) # sort by x position
        print""
        print"Printing the sorted TOP dictionary"
        print"----------------------------------"
        
        if len(sorted_ObjectDict2a) > 0:
            for Name,Object in sorted_ObjectDict2a:
                print"%s %s %s" % (Name,Object[1],Object[0].image_filepath)
        else:
            print "    <2a empty>" 
        
        if len(sorted_ObjectDict2b) > 0:
            for Name,Object in sorted_ObjectDict2b:
                print"%s %s %s" % (Name,Object[1],Object[0].image_filepath)
        else:
            print "    <2b empty>" 
      
      #def ShowObjectDicts_bottom_canvas():
      #  ## list object on the top canvas listed in the dictionary
      #  TargetWidget_TargetObject.ShowObjectDict('BottomCanvas')
      #      print '----------'
      
      def ShowObjectDicts():
        """
        Some demo code to let the user see what objects we think are
            on each of the three canvases.
        """
        ShowObjectDicts_top_canvas()
        ShowObjectDicts_middle_canvas()
        #ShowObjectDicts_bottom_canvas()
        Trash.ShowObjectDict('Trash bin')
        print '----------'
    
      def get_image_filepath():
        self.selected_button_image_filepath = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        
   
      def get_bytes_from_file(self,filename):  
        tempBuffer = bytearray()
        try:
          #operation_that_can_throw_ioerror()
          f = open(filename.lower().replace('.gif','.DAT'), "rb").read()
          print"get_bytes_from_file: FOUND DAT FILE %s" % (filename.lower().replace('.gif','.DAT'))
          print"the length of file is %i" % (len(f))
          for line in f:
            #print line.encode('hex')
            tempBuffer.append(line)
          return tempBuffer
        except IOError:
        #handle_the_exception_somehow()
        # if the .dat file doesn't exist use .gif file as source 
          print"get_bytes_from_file: ERROR NO DAT FILE, using GIF"
          img = Image.open(filename)
          rgb_pix = img.convert('RGB')
          ledColorMatrix = [['#ffffff' for x in xrange(8)] for x in xrange(8)]
          for s in self.box_coord_vh:
            r,g,b = rgb_pix.getpixel((s[3]-4,s[2]-4)) # center of each box
            hexstring = ('#%02X%02X%02X'%(r,g,b))
            ledColorMatrix[(s[3]/12)-1][(s[2]/12)-1] =  hexstring
            tempBuffer.append(r)
            tempBuffer.append(g)
            tempBuffer.append(b)
          #print"get_bytes_from_file: tempBuffer"
          #print tempBuffer
          return tempBuffer 
        
        #else:
        # # we don't want to catch the IOError if it's raised
        # another_operation_that_can_throw_ioerror()
        #finally:
        # something_we_always_need_to_do()
      
      def send_array_as_bin(self,array):
        # array is a buffer length 192 = 8x * 8y * 3 bytes
        print("send_array_as_bin: The array length is: %i"%( len(array)))
        msg = buffer(b"Fd") + array
        self.E1a_q.put(msg) # send array
        
      ############################################################################################## 
      self.selected_button_image_filepath = None
      self.E1a_q = tx_queue1a
      self.E1b_q = tx_queue1b
      self.E2a_q = tx_queue2a
      self.E2b_q = tx_queue2b
      
      self.E1a_v = StringVar()
      self.E1a_v.set("192.168.1.170")
      self.E1b_v = StringVar()
      self.E1b_v.set("192.168.1.171")
      self.E2a_v = StringVar()
      self.E2a_v.set("192.168.1.180")
      self.E2b_v = StringVar()
      self.E2b_v.set("192.168.1.181")
      
      #Create a button to "select button image" file 
      #############################################################################################
      ImageObject = Tkinter.Button(win,text='Select Button Image', command=get_image_filepath).grid(row=0, column = 0) 
      #Create a button to act as the InitiationObject and bind it to <ButtonPress> so
      #    we start drag and drop when the user clicks on it.
      #The only reason we display the content of the trash bin is to show that it
      #    has no objects, even after some have been dropped on it.
      #############################################################################################
      InitiationObject = Tkinter.Button(win,text='InitiationObject')
      InitiationObject.bind('<ButtonPress>',on_dnd_start)
      InitiationObject.grid(row = 1, column = 0)
      # Create canvases to act as the Target Widgets for the drag and drop. Note that
      # these canvases will act as both the TargetWidget AND the TargetObject.
      #############################################################################################
      self.transmit_CanvasButtons1 = Tkinter.Button(win,text='Animate Canvas 1',command=animate_canvas).grid(row = 2, column = 0)
      
      self.L1a = Label(win, text="8x8 LED\nIP Address").grid(row = 3, column = 0)
      self.E1a = Entry(win, bd =5, textvariable=self.E1a_v).grid(row = 3, column = 1)
      TargetWidget_TargetObject1a = CanvasDnd(win, width=500, height=110, borderwidth=5, background='white', relief=RAISED,bd=2)
      TargetWidget_TargetObject1a.grid(row = 3, column = 2)
      print TargetWidget_TargetObject1a
      
      self.L1b = Label(win, text="Sound\nIP Address").grid(row = 4, column = 0)
      self.E1b = Entry(win, bd =5, textvariable=self.E1b_v).grid(row = 4, column = 1)      
      TargetWidget_TargetObject1b = CanvasDnd(win, width=500, height=110, borderwidth=5, background='white', relief=RAISED,bd=2)
      TargetWidget_TargetObject1b.grid(row = 4, column = 2)
      #############################################################################################
      self.transmit_CanvasButtons2 = Tkinter.Button(win,text='Animate Canvas 2',command=ShowObjectDicts_middle_canvas).grid(row = 6, column = 0);
      
      self.L2a = Label(win, text="8x8 LED\nIP Address").grid(row = 7, column = 0)
      self.E2a = Entry(win, bd =5, textvariable=self.E2a_v).grid(row = 7, column = 1)
      TargetWidget_TargetObject2a = CanvasDnd(win, width=500, height=110, borderwidth=5, background='white', relief=RAISED,bd=2)
      TargetWidget_TargetObject2a.grid(row = 7, column = 2)
      
      self.L2b = Label(win, text="Sound\nIP Address").grid(row = 8, column = 0)
      self.E2b = Entry(win, bd =5, textvariable=self.E2b_v).grid(row = 8, column = 1)
      TargetWidget_TargetObject2b = CanvasDnd(win, width=500, height=110, borderwidth=5, background='white', relief=RAISED,bd=2)
      TargetWidget_TargetObject2b.grid(row = 8, column = 2) 
      #############################################################################################
      #############################################################################################
      # Create an instance of a trash can so we can get rid of dragged objects
      # if so desired.
      Trash = TrashBin(win, relief=RAISED,bd=2)
      Trash.grid(row = 12)
      #############################################################################################
      #Create a "show canvas" button we can press to display the current content of the
      #    canvases ObjectDictionaries.
      showCanvasButton = Tkinter.Button(win,text='Show canvas ObjectDicts',command=ShowObjectDicts)
      showCanvasButton.grid(row = 13)