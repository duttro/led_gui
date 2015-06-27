## 021715 class Assembly_TAB moved to it's own file Assembly_TAB.py
## 021915 added def ShowObjectDicts_top_canvas for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_middle_canvas for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_bottom_canvas for transmitting sending all object on canvas
## 021915 new defs in Assemblt_TAB not working yet
## 030715 assembly_tab animate canvas 1 works
## 031814 changed class name to TIMELINE



import Tkdnd
from Tkinter import *
import Tkinter
import Tkinter, tkFileDialog, Dialog
import Queue
import operator # to sort the dictionary

##############
## my classes
from DraggedDnd import *
from CanvasDnd import *
from LED_TAB import *

class Timeline_TAB:
    
    def __init__(self,win, tx_queue):    
      self.selected_button_image_filepath = None
      self.q = tx_queue
      
      def on_dnd_start(Event):
        """
        This is invoked by InitiationObject to start the drag and drop process
        """
        #Create an object to be dragged
        ThingToDrag = Dragged(self.selected_button_image_filepath)
        print"... the ThingToDrag is";
        print ThingToDrag
        #print("PASSING image file path to CANVAS DND = %s"%(CanvasDnd.image_filepath))
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

      def ShowObjectDicts_top_canvas():
        ##TargetWidget_TargetObject.ShowObjectDict('TopCanvas')
        ## list object on the top canvas listed in the dictionary     
        array = []
        
        print""
        print"Printing the un-sorted dictionary"
        print TargetWidget_TargetObject.ObjectDict.items()
        print""
        
        sorted_ObjectDict = sorted(TargetWidget_TargetObject.ObjectDict.items(), key=operator.itemgetter(1))
        
        print""
        print"Printing the sorted dictionary"
        print sorted_ObjectDict
        print""
        
        if len(sorted_ObjectDict) > 0:
            for Name,Object in sorted_ObjectDict:
                #for obj in Object:
                print Object[0].image_filepath
                array = get_bytes_from_file(self,Object[0].image_filepath)
                send_array_as_bin(self,array)
        else:
            print "    <empty>" 
        
      def ShowObjectDicts_middle_canvas():
        ## list object on the top canvas listed in the dictionary
        TargetWidget_TargetObject.ShowObjectDict('MiddleCanvas')
        print '----------'
      def ShowObjectDicts_bottom_canvas():
        ## list object on the top canvas listed in the dictionary
        TargetWidget_TargetObject.ShowObjectDict('BottomCanvas')
        print '----------'
      
      def ShowObjectDicts():
        """
        Some demo code to let the user see what objects we think are
            on each of the three canvases.
        """
        TargetWidget_TargetObject.ShowObjectDict('TopCanvas')
        TargetWidget_TargetObject2.ShowObjectDict('MiddleCanvas')
        TargetWidget_TargetObject3.ShowObjectDict('BottomCanvas')
        Trash.ShowObjectDict('Trash bin')
        print '----------'
    
      def get_image_filepath():
        self.selected_button_image_filepath = tkFileDialog.askopenfilename(initialdir=('../led_data_files/'),filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        
        
      #Create a button to "select buttons image" file 
      ImageObject = Tkinter.Button(win,text='Select Button Image', command=get_image_filepath)
      ImageObject.pack() 
    
      #Create a button to act as the InitiationObject and bind it to <ButtonPress> so
      #    we start drag and drop when the user clicks on it.
      #The only reason we display the content of the trash bin is to show that it
      #    has no objects, even after some have been dropped on it.
      InitiationObject = Tkinter.Button(win,text='InitiationObject')
      InitiationObject.pack()  #InitiationObject.grid(row = 1, column = 0)
      InitiationObject.bind('<ButtonPress>',on_dnd_start)
    
      #Create canvases to act as the Target Widgets for the drag and drop. Note that
      #    these canvases will act as both the TargetWidget AND the TargetObject.
      #############################################################################################
      transmit_CanvasButtons = Tkinter.Button(win,text='Animate Canvas 1',command=ShowObjectDicts_top_canvas)
      transmit_CanvasButtons.pack()
      ##
      TargetWidget_TargetObject = CanvasDnd(win,relief=RAISED,bd=2) 
      TargetWidget_TargetObject.pack(fill = X)
      #############################################################################################
      transmit_CanvasButtons = Tkinter.Button(win,text='Animate Canvas 2',command=ShowObjectDicts_middle_canvas)
      transmit_CanvasButtons.pack()
      ##
      TargetWidget_TargetObject2 = CanvasDnd(win,relief=RAISED,bd=2)
      TargetWidget_TargetObject2.pack(fill = X)   
      #############################################################################################
      transmit_CanvasButtons = Tkinter.Button(win,text='Animate Canvas 3',command=ShowObjectDicts_bottom_canvas)
      transmit_CanvasButtons.pack()
      TargetWidget_TargetObject3 = CanvasDnd(win,relief=RAISED,bd=2)
      TargetWidget_TargetObject3.pack(fill = X)
      ##############################################################################################
      #Create an instance of a trash can so we can get rid of dragged objects
      #    if so desired.
      Trash = TrashBin(win, relief=RAISED,bd=2)
      Trash.pack(side = LEFT)
    
      #Create a "show canvas" button we can press to display the current content of the
      #    canvases ObjectDictionaries.
      showCanvasButton = Tkinter.Button(win,text='Show canvas ObjectDicts',command=ShowObjectDicts)
      showCanvasButton.pack(side = LEFT)  
   
   
      def get_bytes_from_file(self,filename):  
        tempBuffer = bytearray()
        try:
          #operation_that_can_throw_ioerror()
          f = open(filename.replace('.gif','.dat'), "rb").read()
          print"get_bytes_from_file: FOUND DAT FILE %s" % (filename)
          print"the length of file is %i" % (len(f))
          for line in f:
            #print line.encode('hex')
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
        self.q.put(msg) # send array
        #msg = buffer(b"Fp") + array
        #self.q.put(msg) # send array
        #print msg.encode('hex')