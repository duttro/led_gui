import time
import serial
from Tkinter import *
from tkColorChooser import askcolor


ser = serial.Serial(
    port='com4',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
    ) 
print ser.portstr       # check which port was really used

ser.write("As0707000255000")      # write a string

root = Tk()
root.title("Grid Geometry Manager")
while 1 :
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

 def cb_Store0():
    button_Store0["bg"] = "green"
    button_Store0["text"] = "ACTIVE"
    button_Store0.flash()
    button_Store0["text"] = "Store0"
 def cb_Store1():
    button_Store1["bg"] = "green"
    button_Store1["text"] = "ACTIVE"
    button_Store1.flash()
    button_Store1["text"] = "Store1"
 def cb_Store2():
    button_Store2["bg"] = "green"
    button_Store2["text"] = "ACTIVE"
    button_Store2.flash()
    button_Store2["text"] = "Store2"
 def cb_Store3():
    button_Store3["bg"] = "green"
    button_Store3["text"] = "ACTIVE"
    button_Store3.flash()
    button_Store3["text"] = "Store3"
 def cb_Store4():
    button_Store4["bg"] = "green"
    button_Store4["text"] = "ACTIVE"
    button_Store4.flash()
    button_Store4["text"] = "Store4"
 def cb_Store5():
    button_Store5["bg"] = "green"
    button_Store5["text"] = "ACTIVE"
    button_Store5.flash()
    button_Store5["text"] = "Store5"
 def cb_Store6():
    button_Store6["bg"] = "green"
    button_Store6["text"] = "ACTIVE"
    button_Store6.flash()
    button_Store6["text"] = "Store6"
 def cb_Store7():
    button_Store7["bg"] = "green"
    button_Store7["text"] = "ACTIVE"
    button_Store7.flash()
    button_Store7["text"] = "Store7"

 def cb_Color0():
    global selected_color
    button_selected_color["bg"] = color0
    selected_color = color0
      
 def cb_Color1():
    global selected_color
    button_selected_color["bg"] = color1
    selected_color = color1
    
 def cb_Color2():
    global selected_color
    button_selected_color["bg"] = color2
    selected_color = color2
    
 def cb_Color3():
    global selected_color
    button_selected_color["bg"] = color3
    selected_color = color3
    
 def cb_Color4():
    global selected_color
    button_selected_color["bg"] = color4
    selected_color = color4
    
 def cb_Color5():
    global selected_color
    button_selected_color["bg"] = color5
    selected_color = color5
    
 def cb_Color6():
    global selected_color
    button_selected_color["bg"] = color6
    selected_color = color6
    
 def cb_Color7():
    global selected_color
    button_selected_color["bg"] = color7
    selected_color = color7

 def cb_setColor0():
    global color0
    button_Color0["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        button_Color0["bg"] = hexstr
        color0 = hexstr
    
 def cb_setColor1():
    global color1
    button_Color1["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color1["bg"] = hexstr
        color1 = hexstr
        
 def cb_setColor2():
    global color2
    button_Color2["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color2["bg"] = hexstr
        color2 = hexstr
        
 def cb_setColor3():
    global color3
    button_Color3["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color3["bg"] = hexstr
        color3 = hexstr
        
 def cb_setColor4():
    global color4
    button_Color4["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color4["bg"] = hexstr
        color4 = hexstr
        
 def cb_setColor5():
    global color5
    button_Color5["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color5["bg"] = hexstr
        color5 = hexstr
        
 def cb_setColor6():
    global color6
    button_Color6["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color6["bg"] = hexstr
        color6 = hexstr
        
 def cb_setColor7():
    global color7
    button_Color7["bg"] = 'white'
    (triple, hexstr) = askcolor()
    if hexstr:
        print hexstr
        button_Color7["bg"] = hexstr
        color7 = hexstr


 def cb_led00():
    print"Somebody hit a button";
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


 def cb_led10():
    global selected_color
    button_LED10["bg"] = selected_color
 def cb_led11():
    global selected_color
    button_LED11["bg"] = selected_color
 def cb_led12():
    global selected_color
    button_LED12["bg"] = selected_color
 def cb_led13():
    global selected_color
    button_LED13["bg"] = selected_color
 def cb_led14():
    global selected_color
    button_LED14["bg"] = selected_color
 def cb_led15():
    global selected_color
    button_LED15["bg"] =selected_color
 def cb_led16():
    global selected_color
    button_LED16["bg"] = selected_color
 def cb_led17():
    global selected_color
    button_LED17["bg"] = selected_color


 def cb_led20():
    global selected_color
    button_LED20["bg"] = selected_color
 def cb_led21():
    global selected_color
    button_LED21["bg"] = selected_color
 def cb_led22():
    global selected_color
    button_LED22["bg"] = selected_color
 def cb_led23():
    global selected_color
    button_LED23["bg"] = selected_color
 def cb_led24():
    global selected_color
    button_LED24["bg"] = selected_color
 def cb_led25():
    global selected_color
    button_LED25["bg"] = selected_color
 def cb_led26():
    global selected_color
    button_LED26["bg"] = selected_color
 def cb_led27():
    global selected_color
    button_LED27["bg"] = selected_color


 def cb_led30():
    global selected_color
    button_LED30["bg"] = selected_color
 def cb_led31():
    global selected_color
    button_LED31["bg"] = selected_color
 def cb_led32():
    global selected_color
    button_LED32["bg"] = selected_color
 def cb_led33():
    global selected_color
    button_LED33["bg"] = selected_color
 def cb_led34():
    global selected_color
    button_LED34["bg"] = selected_color
 def cb_led35():
    global selected_color
    button_LED35["bg"] = selected_color
 def cb_led36():
    global selected_color
    button_LED36["bg"] = selected_color
 def cb_led37():
    global selected_color
    button_LED37["bg"] = selected_color


 def cb_led40():
    global selected_color
    button_LED40["bg"] = selected_color
 def cb_led41():
    global selected_color
    button_LED41["bg"] = selected_color
 def cb_led42():
    global selected_color
    button_LED42["bg"] = selected_color
 def cb_led43():
    global selected_color
    button_LED43["bg"] = selected_color
 def cb_led44():
    global selected_color
    button_LED44["bg"] = selected_color
 def cb_led45():
    global selected_color
    button_LED45["bg"] = selected_color
 def cb_led46():
    global selected_color
    button_LED46["bg"] = selected_color
 def cb_led47():
    global selected_color
    button_LED47["bg"] = selected_color


 def cb_led50():
    global selected_color
    button_LED50["bg"] = selected_color
 def cb_led51():
    global selected_color
    button_LED51["bg"] = selected_color
 def cb_led52():
    global selected_color
    button_LED52["bg"] = selected_color
 def cb_led53():
    global selected_color
    button_LED53["bg"] = selected_color
 def cb_led54():
    global selected_color
    button_LED54["bg"] = selected_color
 def cb_led55():
    global selected_color
    button_LED55["bg"] = selected_color
 def cb_led56():
    global selected_color
    button_LED56["bg"] = selected_color
 def cb_led57():
    global selected_color
    button_LED57["bg"] = selected_color

 def cb_led60():
    global selected_color
    button_LED60["bg"] = selected_color
 def cb_led61():
    global selected_color
    button_LED61["bg"] = selected_color
 def cb_led62():
    global selected_color
    button_LED62["bg"] = selected_color
 def cb_led63():
    global selected_color
    button_LED63["bg"] = selected_color
 def cb_led64():
    global selected_color
    button_LED64["bg"] = selected_color
 def cb_led65():
    global selected_color
    button_LED65["bg"] = selected_color
 def cb_led66():
    global selected_color
    button_LED66["bg"] = selected_color
 def cb_led67():
    global selected_color
    button_LED67["bg"] = selected_color

 def cb_led70():
    global selected_color
    button_LED70["bg"] = selected_color
 def cb_led71():
    global selected_color
    button_LED71["bg"] = selected_color
 def cb_led72():
    global selected_color
    button_LED72["bg"] = selected_color
 def cb_led73():
    global selected_color
    button_LED73["bg"] = selected_color
 def cb_led74():
    global selected_color
    button_LED74["bg"] = selected_color
 def cb_led75():
    global selected_color
    button_LED75["bg"] = selected_color
 def cb_led76():
    global selected_color
    button_LED76["bg"] = selected_color
 def cb_led77():
    global selected_color
    button_LED77["bg"] = selected_color


#input=1

    
	button_selected_color = Button(root, text = "Selected Color", bg='white')
	button_selected_color.grid(row=0,column=5)
		
	button_Store0 =   Button(root, text = "Store 0", image = store0_image, command = cb_Store0, compound="left")
	button_Store0.grid(row=1, column=0)
	button_LED00  =   Button(root, height=2, bd=15, bg="Cornflowerblue",text="LED 0,0", command = cb_led00)
	button_LED00.grid(row=1, column=1)
	button_LED01  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,1", command = cb_led01)
	button_LED01.grid(row=1, column=2)
	button_LED02  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,2", command = cb_led02)
	button_LED02.grid(row=1, column=3)
	button_LED03  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,3", command = cb_led03)
	button_LED03.grid(row=1, column=4)
	button_LED04  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,4", command = cb_led04)
	button_LED04.grid(row=1, column=5)
	button_LED05  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,5", command = cb_led05)
	button_LED05.grid(row=1, column=6)
	button_LED06  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,6", command = cb_led06)
	button_LED06.grid(row=1, column=7)
	button_LED07  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 0,7", command = cb_led07)
	button_LED07.grid(row=1, column=8)
	button_Color0 =  Button(root, bg='blue',text="Color0", command = cb_Color0 )
	button_Color0.grid(row=1, column=9)
	button_setColor0 =   Button(root, bg='white',text="setColor0", command = cb_setColor0 )
	button_setColor0.grid(row=1, column=10)

	button_Store1 =   Button(root, text = "Store 1", image = store0_image, command = cb_Store1, compound="left")
	button_Store1.grid(row=2, column=0)
	button_LED10  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,0", command = cb_led10)
	button_LED10.grid(row=2, column=1)
	button_LED11  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,1", command = cb_led11)
	button_LED11.grid(row=2, column=2)
	button_LED12  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,2", command = cb_led12)
	button_LED12.grid(row=2, column=3)
	button_LED13  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,3", command = cb_led13)
	button_LED13.grid(row=2, column=4)
	button_LED14  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,4", command = cb_led14)
	button_LED14.grid(row=2, column=5)
	button_LED15  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,5", command = cb_led15)
	button_LED15.grid(row=2, column=6)
	button_LED16  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,6", command = cb_led16)
	button_LED16.grid(row=2, column=7)
	button_LED17  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 1,7", command = cb_led17)
	button_LED17.grid(row=2, column=8)
	button_Color1 =   Button(root, bg='blue',text="Color1", command = cb_Color1 )
	button_Color1.grid(row=2, column=9)
	button_setColor1 =   Button(root, bg='white',text="setColor1", command = cb_setColor1 )
	button_setColor1.grid(row=2, column=10)

	button_Store2 =   Button(root, text = "Store 2", image = store0_image, command = cb_Store2, compound="left")
	button_Store2.grid(row=3, column=0)
	button_LED20  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,0", command = cb_led20)
	button_LED20.grid(row=3, column=1)
	button_LED21  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,1", command = cb_led21)
	button_LED21.grid(row=3, column=2)
	button_LED22  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,2", command = cb_led22)
	button_LED22.grid(row=3, column=3)
	button_LED23  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,3", command = cb_led23)
	button_LED23.grid(row=3, column=4)
	button_LED24  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,4", command = cb_led24)
	button_LED24.grid(row=3, column=5)
	button_LED25  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,5", command = cb_led25)
	button_LED25.grid(row=3, column=6)
	button_LED26  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,6", command = cb_led26)
	button_LED26.grid(row=3, column=7)
	button_LED27  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 2,7", command = cb_led27)
	button_LED27.grid(row=3, column=8)
	button_Color2 =   Button(root, bg='blue',text="Color2", command = cb_Color2 )
	button_Color2.grid(row=3, column=9)
	button_setColor2 =   Button(root, bg='white',text="setColor2", command = cb_setColor2 )
	button_setColor2.grid(row=3, column=10)

	button_Store3 =   Button(root, text = "Store 3", image = store0_image, command = cb_Store3, compound="left")
	button_Store3.grid(row=4, column=0)
	button_LED30  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,0", command = cb_led30)
	button_LED30.grid(row=4, column=1)
	button_LED31  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,1", command = cb_led31)
	button_LED31.grid(row=4, column=2)
	button_LED32  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,2", command = cb_led32)
	button_LED32.grid(row=4, column=3)
	button_LED33  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,3", command = cb_led33)
	button_LED33.grid(row=4, column=4)
	button_LED34  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,4", command = cb_led34)
	button_LED34.grid(row=4, column=5)
	button_LED35  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,5", command = cb_led35)
	button_LED35.grid(row=4, column=6)
	button_LED36  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,6", command = cb_led36)
	button_LED36.grid(row=4, column=7)
	button_LED37  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 3,7", command = cb_led37)
	button_LED37.grid(row=4, column=8)
	button_Color3 =   Button(root, bg='blue',text="Color3", command = cb_Color3 )
	button_Color3.grid(row=4, column=9)
	button_setColor3 =   Button(root, bg='white',text="setColor3", command = cb_setColor3 )
	button_setColor3.grid(row=4, column=10)

	button_Store4 =   Button(root, text = "Store 4", image = store0_image, command = cb_Store4, compound="left")
	button_Store4.grid(row=5, column=0)
	button_LED40  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,0", command = cb_led40)
	button_LED40.grid(row=5, column=1)
	button_LED41  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,1", command = cb_led41)
	button_LED41.grid(row=5, column=2)
	button_LED42  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,2", command = cb_led42)
	button_LED42.grid(row=5, column=3)
	button_LED43  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,3", command = cb_led43)
	button_LED43.grid(row=5, column=4)
	button_LED44  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,4", command = cb_led44)
	button_LED44.grid(row=5, column=5)
	button_LED45  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,5", command = cb_led45)
	button_LED45.grid(row=5, column=6)
	button_LED46  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,6", command = cb_led46)
	button_LED46.grid(row=5, column=7)
	button_LED47  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 4,7", command = cb_led47)
	button_LED47.grid(row=5, column=8)
	button_Color4 =   Button(root, bg='blue',text="Color4", command = cb_Color4 )
	button_Color4.grid(row=5, column=9)
	button_setColor4 =   Button(root, bg='white',text="setColor4", command = cb_setColor4 )
	button_setColor4.grid(row=5, column=10)

	button_Store5 =   Button(root, text = "Store 5", image = store0_image, command = cb_Store5, compound="left")
	button_Store5.grid(row=6, column=0)
	button_LED50  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,0", command = cb_led50)
	button_LED50.grid(row=6, column=1)
	button_LED51  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,1", command = cb_led51)
	button_LED51.grid(row=6, column=2)
	button_LED52  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,2", command = cb_led52)
	button_LED52.grid(row=6, column=3)
	button_LED53  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,3", command = cb_led53)
	button_LED53.grid(row=6, column=4)
	button_LED54  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,4", command = cb_led54)
	button_LED54.grid(row=6, column=5)
	button_LED55  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,5", command = cb_led55)
	button_LED55.grid(row=6, column=6)
	button_LED56  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,6", command = cb_led56)
	button_LED56.grid(row=6, column=7)
	button_LED57  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 5,7", command = cb_led57)
	button_LED57.grid(row=6, column=8)
	button_Color5 =   Button(root, bg='blue',text="Color5", command = cb_Color5 )
	button_Color5.grid(row=6, column=9)
	button_setColor5 =   Button(root, bg='white',text="setColor5", command = cb_setColor5 )
	button_setColor5.grid(row=6, column=10)

	button_Store6 =   Button(root, text = "Store 6", image = store0_image, command = cb_Store6, compound="left")
	button_Store6.grid(row=7, column=0)
	button_LED60  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,0", command = cb_led60)
	button_LED60.grid(row=7, column=1)
	button_LED61  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,1", command = cb_led61)
	button_LED61.grid(row=7, column=2)
	button_LED62  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,2", command = cb_led62)
	button_LED62.grid(row=7, column=3)
	button_LED63  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,3", command = cb_led63)
	button_LED63.grid(row=7, column=4)
	button_LED64  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,4", command = cb_led64)
	button_LED64.grid(row=7, column=5)
	button_LED65  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,5", command = cb_led65)
	button_LED65.grid(row=7, column=6)
	button_LED66  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,6", command = cb_led66)
	button_LED66.grid(row=7, column=7)
	button_LED67  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 6,7", command = cb_led67)
	button_LED67.grid(row=7, column=8)
	button_Color6 =   Button(root, bg='blue',text="Color6", command = cb_Color6 )
	button_Color6.grid(row=7, column=9)
	button_setColor6 =   Button(root, bg='white',text="setColor6", command = cb_setColor6 )
	button_setColor6.grid(row=7, column=10)

	button_Store7 =   Button(root, text = "Store 7", image = store0_image, command = cb_Store7, compound="left")
	button_Store7.grid(row=8, column=0)
	button_LED70  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,0", command = cb_led70)
	button_LED70.grid(row=8, column=1)
	button_LED71  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,1", command = cb_led71)
	button_LED71.grid(row=8, column=2)
	button_LED72  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,2", command = cb_led72)
	button_LED72.grid(row=8, column=3)
	button_LED73  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,3", command = cb_led73)
	button_LED73.grid(row=8, column=4)
	button_LED74  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,4", command = cb_led74)
	button_LED74.grid(row=8, column=5)
	button_LED75  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,5", command = cb_led75)
	button_LED75.grid(row=8, column=6)
	button_LED76  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,6", command = cb_led76)
	button_LED76.grid(row=8, column=7)
	button_LED77  =   Button(root, height=2, bd=15, bg='Cornflowerblue',text="LED 7,7", command = cb_led77)
	button_LED77.grid(row=8, column=8)
	button_Color7 =   Button(root, bg='blue',text="Color7", command = cb_Color7 )
	button_Color7.grid(row=8, column=9)
	button_setColor7 =   Button(root, bg='white',text="setColor7", command = cb_setColor7 )
	button_setColor7.grid(row=8, column=10)







 endcap="\r\n";
 if ser.inWaiting() > 0:
  out += ser.read(1)
  if out.endsWidth(endcap):
     print ">>" + out
     out = ''


#ser.close()             # close port
root.mainloop()

