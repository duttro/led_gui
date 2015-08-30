from Tkinter import *

class Interface(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=0, height=0, **kwargs)
        self.pack(fill=BOTH)

        self.textA = StringVar()
        self.textE = Entry(self, textvariable=self.textA, width=30)
        self.textE.pack()
        self.getT = self.textA.get()

        self.newWindow = Toplevel(fenetre)
        self.app = Interface2(self.newWindow, self.textA)    # note extra StringVariable argument passed to Interface2 constructor

class Interface2(Frame):
    def __init__(self, fenetre, textA, **kwargs):    # note extra StringVariable parameter "textA"
        Frame.__init__(self, fenetre, width=0, height=0, **kwargs)
        self.pack(fill=BOTH)
        fenetre.geometry("700x700")

        self.textInRealTime = Label(self, textvariable=textA)    # note textvariable set to StringVariable
        self.textInRealTime.pack()

fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()