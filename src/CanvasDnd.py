"""
This code demonstrates a real-world drag and drop.
072614 replaced Label with button, now trying to add pic on button
081014 integrated with LED_app, not cleaned up but working
061015 broke CanvasDnd into it's own class
061215 removed self from ObjectDict, broken
"""

#Set Verbosity to control the display of information messages:
#    2 Displays all messages
#    1 Displays all but dnd_accept and dnd_motion messages
#    0 Displays no messages
Verbosity = 0

#When you drag an existing object on a canvas, we normally make the original
#    Button into an invisible phantom, and what you are ACTUALLY dragging is
#    a clone of the objects Button. If you set "LeavePhantomVisible" then you
#    will be able to see the phantom which persists until the object is
#    dropped. In real life you don't want the user to see the phantom, but
#    for demonstrating what is going on it is useful to see it. This topic
#    beaten to death in the comment string for Dragged.Press, below.
LeavePhantomVisible = 0
import pdb
from Tkinter import *
import Tkdnd
import Tkinter, tkFileDialog, Dialog
from PIL import Image, ImageDraw

def Blab(Level,Message):
    """
    Display Message if Verbosity says to.
    """
    if Verbosity > Level:
        print Message

        
def MouseInWidget(Widget,Event):
    """
    Figure out where the cursor is with respect to a widget.
    
    Both "Widget" and the widget which precipitated "Event" must be
        in the same root window for this routine to work.
        
    We call this routine as part of drawing a DraggedObject inside a
        TargetWidget, eg our Canvas. Since all the routines which need
        to draw a DraggedObject (dnd_motion and it's friends) receive
        an Event, and since an event object contain e.x and e.y values which say
        where the cursor is with respect to the widget you might wonder what all
        the fuss is about; why not just use e.x and e.y? Well it's never
        that simple. The event that gets passed to dnd_motion et al was an
        event against the InitiatingObject and hence what e.x and e.y say is 
        where the mouse is WITH RESPECT TO THE INITIATINGOBJECT. Since we want
        to know where the mouse is with respect to some other object, like the
        Canvas, e.x and e.y do us little good. You can find out where the cursor
        is with respect to the screen (w.winfo_pointerxy) and you can find out
        where it is with respect to an event's root window (e.*_root). So we
        have three locations for the cursor, none of which are what we want.
        Great. We solve this by using w.winfo_root* to find the upper left
        corner of "Widget" with respect to it's root window. Thus we now know
        where both "Widget" and the cursor (e.*_root) are with respect to their
        common root window (hence the restriction that they MUST share a root
        window). Subtracting the two gives us the position of the cursor within
        the widget. 
        
    Yes, yes, we could have said:
        return (Event.X_root-Widget.winfo_rootx(),Event.y_root-Widget.winfo_rooty())
    and done it all on one line, but this is DEMO code and the three line version
    below makes it rather more obvious what's going on. 
    """
    x = Event.x_root - Widget.winfo_rootx()
    y = Event.y_root - Widget.winfo_rooty()
    return (x,y)        
        

class CanvasDnd(Canvas):
    """
    A canvas to which we have added those methods necessary so it can
        act as both a TargetWidget and a TargetObject. 
        
    Use (or derive from) this drag-and-drop enabled canvas to create anything
        that needs to be able to receive a dragged object.    
    """    
    
    def __init__(self, Master, cnf={}, **kw):
          
        if cnf:
            kw.update(cnf)
        Canvas.__init__(self, Master,  kw)
        
        #self.ObjectDict is a dictionary of drag-able object which are currently on
        #    this canvas, either because they have been dropped there or because
        #    they are in mid-drag and are over this canvas.
        self.ObjectDict = {}

       
    #----- TargetWidget functionality -----
    
    def dnd_accept(self,Source,Event):
        #Tkdnd is asking us (the TargetWidget) if we want to tell it about a
        #    TargetObject. Since CanvasDnd is also acting as TargetObject we
        #    return 'self', saying that we are willing to be the TargetObject.
        Blab(2, "Canvas: dnd_accept")
        return self

    #----- TargetObject functionality -----

    def dnd_enter(self,Source,Event):
        #This is called when the mouse pointer goes from outside the
        #   Target Widget to inside the Target Widget.
        Blab(1, "Receptor: dnd_enter")
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,Event)
        #Since the mouse pointer is just now moving over us (the TargetWidget),
        #    we ask the DraggedObject to represent itself on us.
        #    "Source" is the DraggedObject.
        #    "self" is us, the CanvasDnd on which we want the DraggedObject to draw itself.
        #    "XY" is where (on CanvasDnd) that we want the DraggedObject to draw itself.
        Source.Appear(self,XY)
        ####################################3
        # reference the Dragged class
        # self.ObjectDict is a dictionary of drag-able object which are currently on
        #    this canvas, either because they have been dropped there or because
        #    they are in mid-drag and are over this canvas.
        self.ObjectDict[Source.Name] = (Source,XY)

          
    def dnd_motion(self,Source,Event): 
        #,my_image):
        #This is called when the mouse pointer moves within the TargetWidget.
        Blab(2, "Receptor: dnd_motion")
        #Figure out where the mouse is with respect to this widget
        XY = MouseInWidget(self,Event)
        Blab(0,"Receptor: dnd_motion XY = %s"% (str(XY)) )
        #Ask the DraggedObject to move it's representation of itself to the
        #    new mouse pointer location.
        Source.Move(XY)
        # update the coords
        self.ObjectDict[Source.Name] = (Source,XY)
          
        
    def dnd_leave(self,Source,Event):
        #This is called when the mouse pointer goes from inside the
        #    Target Widget to outside the Target Widget.
        Blab(1, "Receptor: dnd_leave")
        #Since the mouse pointer is just now leaving us (the TargetWidget), we
        #    ask the DraggedObject to remove the representation of itself that it
        #    had previously drawn on us.
        Source.Vanish()
        #Remove the DraggedObject from the dictionary of objects which are on 
        #    this canvas
        del self.ObjectDict[Source.Name]
        
    def dnd_commit(self,Source,Event):
        #This is called if the DraggedObject is being dropped on us.
        #This demo doesn't need to do anything here (the DraggedObject is
        #    already in self.ObjectDict) but a real application would
        #    likely want to do stuff here.
        Blab(1, "Receptor: dnd_commit; Object received= %s"%`Source`)

    #----- code added for demo purposes -----
    
    def ShowObjectDict(self,Comment):
        """
        Print Comment and then print the present content of our self.ObjectDict.
        """
        print Comment
        if len(self.ObjectDict) > 0:
            for Name,Object in self.ObjectDict.items():
                # print the image_filepath stored in the button object
                print '    %s %s  %s'%(Name,Object,Object[0].image_filepath)

        else:
            print "    <empty>" 

class TrashBin(CanvasDnd):
    """
    A canvas specifically for deleting dragged objects.
    """
    def __init__(self,Master,**kw):
        #Set default height/width if user didn't specify.
        if not kw.has_key('width'):
            kw['width'] =150
        if not kw.has_key('height'):
            kw['height'] = 25    
        CanvasDnd.__init__(self, Master, kw)
        #Put the text "trash" in the middle of the canvas
        X = kw['width'] / 2
        Y = kw['height'] /2
        self.create_text(X,Y,text='TRASH')
    
    def dnd_commit(self,Source,Event):
        """
        Accept an object dropped in the trash.
        
        Note that the dragged object's 'dnd_end' method is called AFTER this
            routine has returned. We call the dragged objects "Vanish(All=1)"
            routine to get rid of any Buttons it has on any canvas. Having done
            so, it will, at 'dnd_end' time, allow itself to evaporate. If you
            DON'T call "Vanish(All=1)" AND there is a phantom Button of the dragged
            object on an OriginalCanvas then the dragged object will think it 
            has been erroniously dropped in the middle of nowhere and it will 
            resurrect itself from the OriginalCanvas Button. Since we are trying 
            to trash it, we don't want this to happen.
        """
        Blab(1, "TrashBin: dnd_commit")
        #tell the dropped object to remove ALL Buttons of itself.
        Source.Vanish(All=1)
        #were a trash bin; don't keep objects dropped on us.
        self.ObjectDict.clear()             