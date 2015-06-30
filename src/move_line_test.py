import Tkinter as tk; import time
from math import cos,sin,pi
import sys

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.size=300

        self.title("Clock")
        self.w = tk.Canvas(self, width=320, height=320, bg="#456", relief= "sunken", border=10)
        self.w.pack()

        self.w.create_line(0,0,0,0, fill="#ffc", tags="hour")
        self.w.create_line(0,0,0,0, fill="red", tags="minute")
        self.w.create_line(0,0,0,0, fill="black", tags="second")

        uzr1 = tk.Label(self, text="12", bg="#456" )
        uzr1.place(x=160, y=13)
        uzr2 = tk.Label(self, text="6", bg="#456" )
        uzr2.place(x=160, y=303)
        uzr3 = tk.Label(self, text="3", bg="#456" )
        uzr3.place(x=310, y=160)
        uzr4 = tk.Label(self, text="9", bg="#456" )
        uzr4.place(x=11, y=160)

        e = tk.Button(self,text="Quit", command=self.Quit)
        e.pack()

        self.update_clock()

    def update_clock(self):

        s=time.localtime()[5]
        m=time.localtime()[4]
        h=time.localtime()[3]

        degrees = 6*s
        angle = degrees*pi*2/360
        ox = 165
        oy = 165
        x = ox + self.size*sin(angle)*0.45
        y = oy - self.size*cos(angle)*0.45
        self.w.coords("hour", (ox,oy,x,y))

        degrees1 = 6*m
        angle1 = degrees1*pi*2/360
        ox1 = 165
        oy1 = 165
        x1 = ox1 + self.size*sin(angle1)*0.4
        y1 = oy1 - self.size*cos(angle1)*0.4
        self.w.coords("minute", (ox1,oy1,x1,y1))

        degrees2 = 30*h
        angle2 = degrees2*pi*2/360
        ox2 = 165
        oy2 = 165
        x2 = ox2 + self.size*sin(angle2)*0.2
        y2 = oy2 - self.size*cos(angle2)*0.2
        self.w.coords("second",(ox2,oy2,x2,y2))

        self.after(1000, self.update_clock)

    def Quit(self):
        self.after(700,self.destroy())

app = MyApp()
app.mainloop()
