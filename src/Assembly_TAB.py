## 021715 class Assembly_TAB moved to it's own file Assembly_TAB.py
## 021915 added def ShowObjectDicts_top_canvas for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_middle_canvas for transmitting sending all object on canvas
## 021915 added def ShowObjectDicts_bottom_canvas for transmitting sending all object on canvas
## 021915 new defs in Assemblt_TAB not working yet



import Tkdnd
from Tkinter import *
import Tkinter
import Tkinter, tkFileDialog, Dialog

##############
## my classes
from dnd import *
from LED_TAB import *

class Assembly_TAB:
    
    def __init__(self,win, tx_queue):    
      self.selected_button_image_filepath = None
      
      def on_dnd_start(Event):
        """
        This is invoked by InitiationObject to start the drag and drop process
        """
        #Create an object to be dragged
        ThingToDrag = Dragged()
        #print("PASSING image file path to CANVAS DND = %s"%(CanvasDnd.image_filepath))
        #Pass the object to be dragged and the event to Tkdnd
        Tkdnd.dnd_start(ThingToDrag,Event)

      def ShowObjectDicts_top_canvas():
        ##TargetWidget_TargetObject.ShowObjectDict('TopCanvas')
        ## list object on the top canvas listed in the dictionary     
        array = []
        if len(TargetWidget_TargetObject.ObjectDict) > 0:
            for Name,Object in TargetWidget_TargetObject.ObjectDict.items():
                #for obj in Object:
                print Object[2]
                array = LED_TAB.get_bytes_from_file(self,filename)
                LED_TAB.send_array_as_bin(self,array)
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
        self.selected_button_image_filepath = tkFileDialog.askopenfilename(filetypes=[("Image Files","*.gif"),("GIF",'*.gif')] )
        Dragged.image_filepath   = self.selected_button_image_filepath
        CanvasDnd.image_filepath = self.selected_button_image_filepath
        print("ASSEMBLY_TAB sent Dragged   image file path = %s"%(Dragged.image_filepath))
        print("ASSEMBLY_TAB sent CanvasDnd image file path = %s"%(CanvasDnd.image_filepath))
        
        
      #Create a button to "select buttons image" file 
      ImageObject = Tkinter.Button(win,text='Select Button Image', command=get_image_filepath)
      ImageObject.grid(row = 0, column = 0) 
    
      #Create a button to act as the InitiationObject and bind it to <ButtonPress> so
      #    we start drag and drop when the user clicks on it.
      #The only reason we display the content of the trash bin is to show that it
      #    has no objects, even after some have been dropped on it.
      InitiationObject = Tkinter.Button(win,text='InitiationObject')
      InitiationObject.grid(row = 1, column = 0)
      InitiationObject.bind('<ButtonPress>',on_dnd_start)
    
      #Create two canvases to act as the Target Widgets for the drag and drop. Note that
      #    these canvases will act as both the TargetWidget AND the TargetObject.
      TargetWidget_TargetObject = CanvasDnd(win,relief=RAISED,bd=2)
      #TargetWidget_TargetObject.pack(expand=YES,fill=BOTH)
      TargetWidget_TargetObject.grid(row = 2, column = 0)
      transmit_CanvasButtons = Tkinter.Button(win,text='animate canvas1',command=ShowObjectDicts_top_canvas)
      transmit_CanvasButtons.grid(row = 2, column = 1)
    
      TargetWidget_TargetObject2 = CanvasDnd(win,relief=RAISED,bd=2)
      #TargetWidget_TargetObject2.pack(expand=YES,fill=BOTH)
      TargetWidget_TargetObject2.grid(row = 3, column = 0)
      transmit_CanvasButtons = Tkinter.Button(win,text='animate canvas2',command=ShowObjectDicts_middle_canvas)
      transmit_CanvasButtons.grid(row = 3, column = 1)
      
      TargetWidget_TargetObject3 = CanvasDnd(win,relief=RAISED,bd=2)
      #TargetWidget_TargetObject3.pack(expand=YES,fill=BOTH)
      TargetWidget_TargetObject3.grid(row = 4, column = 0)
      transmit_CanvasButtons = Tkinter.Button(win,text='animate canvas3',command=ShowObjectDicts_bottom_canvas)
      transmit_CanvasButtons.grid(row = 4, column = 1)
      
      #Create an instance of a trash can so we can get rid of dragged objects
      #    if so desired.
      Trash = TrashBin(win, relief=RAISED,bd=2)
      #Trash.pack(expand=NO)
      Trash.grid(row = 5, column = 0)
    
      #Create a "show canvas" button we can press to display the current content of the
      #    canvases ObjectDictionaries.
      showCanvasButton = Tkinter.Button(win,text='Show canvas ObjectDicts',command=ShowObjectDicts)
      showCanvasButton.grid(row = 6, column = 0)  
