import time
import serial
import string
import Tkinter

from Tkinter import *
from tkColorChooser import askcolor


class led_color(Tkinter.Tk):

  def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

  def initialize(self):

    store0_image = PhotoImage(file = "./led_array_thumbnail.gif")
    color0 = '#ffffff'
    color1 = '#ffffff'
    color2 = '#ffffff'
    color3 = '#ffffff'
    color4 = '#ffffff'
    color5 = '#ffffff'
    color6 = '#ffffff'
    color7 = '#ffffff'
    selected_color = '#ffffff'
    
    button_selected_color = Button(self, text = "Selected Color", bg='white')
    button_selected_color.grid(row=0,column=5)
        
    button_Store0 =   Button(self, text = "Store 0", image = store0_image, command = self.cb_Store0, compound="left")
    button_Store0.grid(row=1, column=0)
    button_LED00  =   Button(self, height=2, bd=15, bg="Cornflowerblue",text="LED 0,0", command = self.cb_led00 )
    button_LED00.grid(row=1, column=1)
    button_LED01  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,1", command = self.cb_led01 )
    button_LED01.grid(row=1, column=2)
    button_LED02  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,2", command = self.cb_led02 )
    button_LED02.grid(row=1, column=3)
    button_LED03  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,3", command = self.cb_led03 )
    button_LED03.grid(row=1, column=4)
    button_LED04  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,4", command = self.cb_led04 )
    button_LED04.grid(row=1, column=5)
    button_LED05  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,5", command = self.cb_led05 )
    button_LED05.grid(row=1, column=6)
    button_LED06  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,6", command = self.cb_led06 )
    button_LED06.grid(row=1, column=7)
    button_LED07  =   Button(self, height=2, bd=15, bg='Cornflowerblue',text="LED 0,7", command = self.cb_led07 )
    button_LED07.grid(row=1, column=8)
    button_Color0 =  Button(self, bg='blue',text="Color0", command = self.cb_Color0 )
    button_Color0.grid(row=1, column=9)
    button_setColor0 =   Button(self, bg='white',text="setColor0", command = self.cb_setColor0 )
    button_setColor0.grid(row=1, column=10)

    
  def cb_Store0():
    button_Store0["bg"] = "green"
    button_Store0["text"] = "ACTIVE"
    button_Store0.flash()
    button_Store0["text"] = "Store0"
  

  def cb_Color0():
    global selected_color
    button_selected_color["bg"] = color0
    selected_color = color0
      
  

  def cb_setColor0():
    global color0
    button_Color0["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        button_Color0["bg"] = hexstr
        color0 = hexstr
    
  

  def cb_led00():
    #print"Somebody hit a button";
    global selected_color
    button_LED00["bg"] = selected_color
    ser.write("As0707000255000")

  def cb_led01():
    global selected_color
    button_LED01["bg"] = selected_color

  def cb_led02():
    global selected_color
    button_LED02["bg"] = selected_color

  def cb_led03():
    global selected_color
    button_LED03["bg"] = selected_color

  def cb_led04():
    global selected_color
    button_LED04["bg"] = selected_color

  def cb_led05():
    global selected_color
    button_LED05["bg"] = selected_color

  def cb_led06():
    global selected_color
    button_LED06["bg"] = selected_color

  def cb_led07():
    global selected_color
    button_LED07["bg"] = selected_color


  

    
if __name__ == "__main__":
    app = led_color(None)
    app.title('LED COLOR')

    ser = serial.Serial(
    port='com4',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
    ) 
    print ser.portstr       # check which port was really used
    
    out =''
    ser.write("As0707000255000")      # write a string
    #while 1 :

    print ser.inWaiting()
    if ser.inWaiting() > 0:
      out += ser.read(1)
      if out.endswith('\r\n'):
       print ">>" + out
       out = ''
    app.mainloop()

  #ser.close()             # close port
  #self.mainloop()

