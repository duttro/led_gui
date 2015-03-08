# rdutt 081014 added the coords of the object to the dictionary, so they can be sorted buy their position
# rdutt 082614 adding the button image name to the dictionary

"""
This code demonstrates a real-world drag and drop.
072614 replaced Label with button, now trying to add pic on button
081014 integrated with LED_app, not cleaned up but working
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

def Blab(Level,Message):
    """
    Display Message if Verbosity says to.
    """
    if Verbosity > Level:
        print Message
    
class Dragged:
    """
    This is a prototype thing to be dragged and dropped.
    
    Derive from (or mixin) this class to create real drag able objects.
    """
    #We use this to assign a unique number to each instance of Dragged.
    #    This isn't a necessity; we do it so that during the demo you can
    #    tell one instance from another.
    NextNumber = 0

    def __init__(self):
        Blab(1, "An instance of Dragged has been created")
        #When created we are not on any canvas
        self._image_filepath = None
        self.Canvas = None
        self.OriginalCanvas = None
        #This sets where the mouse cursor will be with respect to our Button
        self.OffsetX = 20
        self.OffsetY = 10
        #Assign ourselves a unique number
                
        self.Number = Dragged.NextNumber
        Dragged.NextNumber += 1
        #Use the number to build our name
        self.Name = 'DragObj-%s'%self.Number
    @property
    def image_filepath(self):
            #print "accessed the image_filepath attribute"
            return self._image_filepath

    @image_filepath.setter
    def image_filepath(self,value):
            #print "modified the image_filepath attribute"
            self._image_filepath = value
            #print("DRAGGED image file path = %s"%(self._image_filepath))

            
    def dnd_end(self,Target,Event):
        #this gets called when we are dropped
        Blab(1, "%s has been dropped; Target=%s"%(self.Name,`Target`))
        if self.Canvas==None and self.OriginalCanvas==None:
            #We were created and then dropped in the middle of nowhere, or
            #    we have been told to self destruct. In either case
            #    nothing needs to be done and we will evaporate shortly.
            return
        if self.Canvas==None and self.OriginalCanvas<>None:
            #We previously lived on OriginalCanvas and the user has
            #   dragged and dropped us in the middle of nowhere. What you do
            #   here rather depends on your own personal taste. There are 2 choices:
            #   1) Do nothing. The dragged object will simply evaporate. In effect
            #      you are saying "dropping an existing object in the middle
            #      of nowhere deletes it".  Personally I don't like this option because
            #      it means that if the user, while dragging an important object, 
            #      twitches their mouse finger as the object is in the middle of
            #      nowhere then the object gets immediately deleted. Oops.
            #   2) Resurrect the original Button (which has been there but invisible)
            #      thus saying "dropping an existing dragged object in the middle of
            #      nowhere is as if no drag had taken place". Thats what the code that
            #      follows does.
            self.Canvas = self.OriginalCanvas
            self.ID = self.OriginalID
            self.Button = self.OriginalButton
            self.Button['text'] = self.OriginalText
            self.Button['relief'] = RAISED
            self.Button['image'] = PhotoImage(file = self.image_filepath)
            #We call the canvases "dnd_enter" method here to keep its ObjectDict up
            #    to date. We know that we had been dragged off the canvas, so before
            #    we call "dnd_enter" the canvases ObjectDict says we are not on the
            #    canvas. The call to "dnd_enter" will tell the canvas that we are,
            #    in effect, entering the canvas. Note that "dnd_enter" will in turn
            #    call our "Appear" method, but "Appear" is smart enough to realize
            #    that we already have a Button on self.Canvas, so it quietly does
            #    does nothing,
            self.Canvas.dnd_enter(self,Event)
            return
        #At this point we know that self.Canvas is not None, which means we have an
        #    Button of ourself on that canvas. Bind <ButtonPress> to that Button so the
        #    the user can pick us up again if and when desired.            
        self.Button.bind('<ButtonPress>',self.Press)
        #If self.OriginalCanvas exists then we were an existing object and our
        #    original Button is still around although hidden. We no longer need
        #    it so we delete it.
        if self.OriginalCanvas:
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            self.OriginalID = None
            self.OriginalButton = None

    def Appear(self, Canvas, XY):
        """
        Put an Button representing this Dragged instance on Canvas.
        
        XY says where the mouse pointer is. We don't, however, necessarily want
            to draw our upper left corner at XY. Why not? Because if the user
            pressed over an existing Button AND the mouse wasn't exactly over the
            upper left of the Button (which is pretty likely) then we would like
            to keep the mouse pointer at the same relative position inside the
            Button. We therefore adjust X and Y by self.OffsetX and self.OffseY
            thus moving our upper left corner up and/or left by the specified
            amounts. These offsets are set to a nominal value when an instance
            of Dragged is created (where it matters rather less), and to a useful
            value by our "Press" routine when the user clicks on an existing
            instance of us.
        """
        if self.Canvas:
            #we are already on a canvas; do nothing
            return
        self.X, self.Y = XY    
        #Create a Button which identifies us, including our unique number
        self.image = Tkinter.PhotoImage(file = self.image_filepath) #load the newly saved image on the button 
        self.Button = Button(Canvas,text=self.Name,borderwidth=2, relief=RAISED, image=self.image)
        #Display the Button on a window on the canvas. We need the ID returned by
        #    the canvas so we can move the Button around as the mouse moves.
        self.ID = Canvas.create_window(self.X-self.OffsetX, self.Y-self.OffsetY, window=self.Button, anchor="nw")
        #Note the canvas on which we drew the Button.
        self.Canvas = Canvas

    def Vanish(self,All=0):
        """
        If there is a Button representing us on a canvas, make it go away.
        
        if self.Canvas is not None, that implies that "Appear" had previously
            put a Button representing us on the canvas and we delete it.
            
        if "All" is true then we check self.OriginalCanvas and if it not None
            we delete from it the Button which represents us.
        """
        if self.Canvas:
            #we have a Button on a canvas; delete it
            self.Canvas.delete(self.ID)
            #flag that we are not represented on the canvas
            self.Canvas = None
            #Since ID and Button are no longer meaningful, get rid of them lest they
            #confuse the situation later on. Not necessary, but tidy.
            del self.ID
            del self.Button
        
        if All and self.OriginalCanvas:
            #Delete Button representing us from self.OriginalCanvas
            self.OriginalCanvas.delete(self.OriginalID)
            self.OriginalCanvas = None
            del self.OriginalID
            del self.OriginalButton

    def Move(self,XY):
        """
        If we have a Button a canvas, then move it to the specified location. 
        
        XY is with respect to the upper left corner of the canvas
        """    
        assert self.Canvas, "Can't move because we are not on a canvas"
        self.X, self.Y = XY
        self.Canvas.coords(self.ID,self.X-self.OffsetX,self.Y-self.OffsetY)

    def Press(self,Event):
        """
        User has clicked on a Button representing us. Initiate drag and drop.
        There is a problem, er, opportunity here. In this case we would like to
            act as both the InitiationObject (because the user clicked on us
            and it't up to us to start the drag and drop) but we also want to
            act as the dragged object (because it's us the user wants to drag
            around). If we simply pass ourself to "Tkdnd" as the dragged object
            it won't work because the entire drag and drop process is moved
            along by <motion> events as a result of a binding by the widget
            on which the user clicked. That widget is the Button which represents
            us and it get moved around by our "move" method. It also gets
            DELETED by our "vanish" method if the user moves it off the current
            canvas, which is a perfectly legal thing from them to do. If the
            widget which is driving the process gets deleted, the whole drag and
            drop grinds to a real quick halt. We use a little sleight of hand to
            get around this:
            1) From the Button which is currently representing us (self.Button) 
               we take the text and save it in self.OriginalText. This will allow 
               us to resurrect the Button at a later time if so desired. (It turns 
               out we so desire if the user tries to drop us in the middle of 
               nowhere, but that's a different story; see "dnd_end", above).
            2) We take the Button which is currently representing us (self.Button)
               and we make it into an invisible phantom by setting its text to ''
               and settings its relief to FLAT. It is now, so to speak, a polar
               bear in a snowstorm. It's still there, but it blends in with the
               rest of then canvas on which it sits. 
            3) We move all the information about the phantom Button (Canvas, ID
               and Button) into variables which store information about the 
               previous Button (PreviousCanvas, PreviousID and PreviousButton)
            4) We set self.Canvas and friends to None, which indicates that we 
               don't have a Button representing us on the canvas. This is a bit
               of a lie (the phantom is technically on the canvas) but it does no
               harm.
            5) We call "self.Appear" which, noting that don't have a Button
               representing us on the canvas, promptly draws one for us, which
               gets saved as self.Canvas etc.
            We went to all this trouble so that:
            a) The original widget on which the user clicked (now the phantom)
               could hang around driving the drag and drop until it is done, and
            b) The user has a Button (the one just created by Appear) which they 
               can drag around, from canvas to canvas as desired, until they 
               drop it. THIS one can get deleted from the current canvas and
               redrawn on another canvas without Anything Bad happening.           
            From the users viewpoint the whole thing is seamless: they think
                the ARE dragging around the original Button, but they are not. To 
                make it really clear what is happening, go to the top of the
                code and set "LeavePhantomVisible" to 1. Then when you drag an 
                existing object, you will see the phantom.
            The phantom is resolved by routine "dnd_end" above. If the user 
                drops us on a canvas, then we take up residence on the canvas and
                the phantom Button, no longer needed, is deleted. If the user tries
                to drop us in the middle of nowhere, then there will be no
                'current' Button for us (because we are in the middle of nowhere)
                and thus we resurrect the phantom Button which in this case
                continues to represent us.    
            Note that this whole deal happens ONLY when the user clicks on an
                EXISTING instance of us. In the case where the user clicks over
                the button marked "InitiationObject" then it it that button that
                IS the initiation object, it creates a copy of us and the whole
                opportunity never happens, since the "InitiationObject" button 
                is never in any danger of being deleted.
        """
        Blab(1, "Dragged.press")
        #Save our current Button as the Original Button
        self.OriginalID = self.ID
        self.OriginalButton = self.Button
        self.OriginalText = self.OriginalButton['text']
        self.OriginalCanvas = self.Canvas
        self.OriginalImage = self.image
        #Made the phantom invisible (unless the user asked to see it)
        if LeavePhantomVisible:
            self.OriginalButton['text'] = '<phantom>'
            self.OriginalButton['relief']=RAISED
        else:
            self.OriginalButton['text'] = ''
            self.OriginalButton['relief']=FLAT
        #Say we have no current Button    
        self.ID = None
        self.Canvas = None
        self.Button = None
        #Ask Tkdnd to start the drag operation
        if Tkdnd.dnd_start(self,Event):
            #Save where the mouse pointer was in the Button so it stays in the
            #    same relative position as we drag it around
            self.OffsetX, self.OffsetY = MouseInWidget(self.OriginalButton,Event)
            #Draw a Button of ourself for the user to drag around
            XY = MouseInWidget(self.OriginalCanvas,Event)
            self.Appear(self.OriginalCanvas,XY)
    
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
        #ObjectDict is a dictionary of drag-able object which are currently on
        #    this canvas, either because they have been dropped there or because
        #    they are in mid-drag and are over this canvas.
        self.ObjectDict = {}
        
        self._image_filepath = None
        
        ### Assign button image here
        #print("DRAGGED image file path = %s"%(self.image_filepath))
        #filename = PhotoImage(file = self.image_filepath)
               
    @property
    def image_filepath(self):
            #print "CanvasDnd accessed the image_filepath attribute"
            return self._image_filepath

    @image_filepath.setter
    def image_filepath(self,value):
            #print "CanvasDnd modified the image_filepath attribute"
            self._image_filepath = value
            #print("CanvasDnd image file path = %s"%(self._image_filepath))
        
        
        
        
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
        #Add the DraggedObject to the dictionary of objects which are on this canvas.
        Blab(0, "$$$CanvasDnd:dnd_enter: Image    %s"%(self.image_filepath) )
        self.ObjectDict[Source.Name] = (Source,XY,self.image_filepath)
        #pdb.set_trace()
        
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
        Blab(0, "dnd_motion: my_image    %s"%(self.image_filepath)   )
        self.ObjectDict[Source.Name] = (Source,XY,self.image_filepath)
        
    def dnd_commit(self,Source,Event):
        #This is called if the DraggedObject is being dropped on us.
        #This demo doesn't need to do anything here (the DraggedObject is
        #    already in self.ObjectDict) but a real application would
        #    likely want to do stuff here.
        Blab(0, "dnd_commit: my_image    %s"%(self.image_filepath)  )
        Blab(1, "Receptor: dnd_commit; Object received= %s"%`Source`)

    #----- code added for demo purposes -----
    
    def ShowObjectDict(self,Comment):
        """
        Print Comment and then print the present content of our ObjectDict.
        """
        print Comment
        if len(self.ObjectDict) > 0:
            for Name,Object in self.ObjectDict.items():
                print '    %s %s '%(Name,Object)
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


