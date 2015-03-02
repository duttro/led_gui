import time
import serial
import string
import Tkinter
from tkColorChooser import askcolor
import threading
import random
import Queue



# Create the queue
tx_queue = Queue.Queue( )


class Serial:

    def __init__(self, tx_queue):
        print"class Serial started"

        self.out=''

        ser = serial.Serial(
            port='com4',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS
            ) 
        print ser.portstr       # check which port was really used


        while (1):
            
            while ser.inWaiting() > 0:
              self.out += ser.read(1)

            if self.out.endswith('\r\n'):
              print ">>" + self.out
              self.out = ''

            #print "ser tx_q = %d"  %(tx_queue.qsize(  ))
            while tx_queue.qsize(  ):
              print "ser tx_q = %d"  %(tx_queue.qsize(  ))
              try:
                 #self.master = master
                 TXmsg = tx_queue.get( )
                 print "sending msg %s" % (TXmsg)
                 ser.write(TXmsg)
              except Queue.Empty:
                 # just on general principles, although we don't
                 # expect this branch to be taken in this case
                 pass
            time.sleep(.5)  


class GuiPart:

    def __init__(self,win, tx_queue):
        
        print"GUI init"
        self.q = tx_queue

        # Set up the GUI
        print"GUI initialize"
        #console = Tkinter.Button(win, text='Done')
        #console.grid(row=1, column=1)       
##
        self.button_LED00 = Tkinter.Button(win, height=2, bd=15, bg="Cornflowerblue",text="LED 0,0", command = self.cb_led00)
        self.button_LED00.grid(row=1, column=2)

    def cb_led00(self):
        self.q.put("As0707000255000\r\n") # write a string to the serial port via tx_queue
        print self.q.qsize(  )
        print"Somebody hit a button %d" % (tx_queue.qsize(  ))
        self.button_LED00.configure(bg = 'green')


def main():
    """ MAIN PROGRAM"""
    root = Tkinter.Tk(  )
    
    # Set up the GUI part
    gui = GuiPart(root,tx_queue)


    serThread1 = threading.Thread(target=Serial, args=(tx_queue,) )
    serThread1.start()

    root.mainloop()


if __name__ == "__main__":
    main()
    



