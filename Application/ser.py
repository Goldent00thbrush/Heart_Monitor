##Serial Haert Monitor ECG Python Application
#imports
from tkinter import *
import serial
import serial.tools.list_ports
from tkinter import Tk
from tkinter import Button
from tkinter import BOTH, BOTTOM, TOP, RIGHT,LEFT, X, Y, NW
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import datetime as dt
import string
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
#defs string literals
MSG_SER="Cannot connect to serial port"
MSG_FRQ = "Invalid number! \n" \
          "It  has to be between 1.525Hz to 100KHz"
# warning pop for serial connection
def popup_bonus(x):
    win = Toplevel() #new top level window
    #styling
    win.wm_title("Serial Connection")
    win.iconbitmap('hnet.com-image.ico')
    win.configure(background="white")
    win.resizable(False, False)

    #text to display
    l = Label(win, text=x, background = "white", fg = "red", font=("Ink Free", 12, "bold"))
    l.grid(row=0, column=0)

    #button to close window
    b = Button(win, text="Okay", command=win.destroy, background = "red",  activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
    b.grid(row=1, column=0)

#function to return baud rate value based on selected
def getVal(s):
    global ser
    if (s == "115200"):
        ser.write(bytes(b'u'))
        ser.baudrate = 115200
    elif (s == "128000"):
        ser.write(bytes(b'v'))
        ser.baudrate = 128000
    elif (s == "256000"):
        ser.write(bytes(b'1'))
        ser.baudrate = 256000
    elif (s == "1200"):
        ser.write(bytes(b'o'))
        ser.baudrate = 1200
    elif (s == "57600"):
        ser.write(bytes(b'2'))
        ser.baudrate = 57600
    elif (s == "56000"):
        ser.write(bytes(b'3'))
        ser.baudrate = 56000
    elif (s == "38400"):
        ser.write(bytes(b'4'))
        ser.baudrate = 38400
    elif (s == "19200"):
        ser.write(bytes(b'5'))
        ser.baudrate = 19200
    elif (s == "14400"):
        ser.write(bytes(b'6'))
        ser.baudrate = 14400
    elif (s ==  "9600"):
        ser.write(bytes(b'7'))
        ser.baudrate = 9600
    elif (s == "4800"):
        ser.write(bytes(b'8'))
        ser.baudrate = 4800
    elif (s == "2400"):
        ser.write(bytes(b'g'))
        ser.baudrate = 2400

#function to intially connect the port with serial rate
def connect(s):
    try:
        global ser
        ser = serial.Serial(s) #create serial port with pyserial
        ser.baudrate = 115200 #set baud rate
        getVal(variable_br.get()) #change baudrate if needed
    except serial.serialutil.SerialException:
        popup_bonus(MSG_SER) #warning if cannot connect


#function to serially connect the data for graph
def data_ecg():
    global ser, ani_flag, first_read
    while (ser.inWaiting() <= 0):
        var = 0
    x = ser.readline().decode("utf-8")
    if(x=="-\n"and not first_read):
        ani_flag= False
        return 0
    elif(first_read and x=="-\n"):
        first_read = False
        return 0
    return int(x) #gives read value

# This function is called periodically from FuncAnimation to animate the graph
def animate(i, xs, ys):
    # Read serial data
    ser_d =data_ecg()
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(ser_d)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Heart Beat')
    plt.ylabel('ECG (V)')
#for the frames to be used in animation
def gen_function():
    global ani_flag
    i = 0
    while ani_flag:
        i += 1
        yield i

#method for button to graph
def button_ecg():
    global ser, ani_flag, first_read
    global fig, xs, ys, canvas
    global master
    if (ser == None): #checks if serial port is connected
        popup_bonus(MSG_SER)
        return
    ser.write(bytes(b'g')) #requests data from port
    ser.write(bytes(b'g'))
    ani_flag=True
    #first_read = True
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10, frames=gen_function, repeat=False) #animate graph
    canvas.draw() #updates canvas
    master.mainloop()

#method for ok button for serial connection
def ok():
   global ser
   if (variable_p.get() == "COM3"): #does not connect to COM3
       popup_bonus(MSG_SER)
   elif (ser != None and ser.name == variable_p.get()): #change baud rate
       getVal(variable_br.get())
   else:
    connect(variable_p.get()) #chage serial port

#read and present bpm
def bpm_button():
    global master
    global ser, label
    if (ser == None): #check if connection exists
        popup_bonus(MSG_SER)
        return
    ser.write(bytes(b'h')) #send request
    while(ser.inWaiting()<=0):
        var =0
    var = ser.readline().decode("utf-8")
    label.configure(text=var)

#to check for values
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

#sampling rate button
def button_sample():
    #valid
    global master
    global ser, stext
    if (ser == None):  # check if connection exists
        popup_bonus(MSG_SER)
        return
    s =stext.get()
    if(not isfloat(s) or float(s)<1.525 or float(s)>100000):
        popup_bonus(MSG_FRQ)
        return
    ser.write(bytes(b'f'))  # send request
    ser.write(bytes(b'f'))
    ser.write((s+'-').encode())

#baud rate options
OPTIONS_BAUDRATES = [ "256000","128000", "115200","57600", "56000", "38400", "19200", "14400", "9600" , "4800", "2400", "1200"]
OPTIONS_PORTS = [p.device for p in list(serial.tools.list_ports.comports())]
#creating window
master = Tk()
master.title("Heart Rate Monitor")
#global variables
ani_flag= True
first_read = True
ser = None
var = '0'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

#frames for overall layout
frame_left = Frame(master)
frame_left.grid(row=0, column=0,sticky='N')
frame_center = Frame(master)
frame_center.grid(row=0, column =1,sticky='N', padx=(10,10), pady=(10,10))

#option menus
variable_br = StringVar(master)
variable_br.set(OPTIONS_BAUDRATES[2]) # default value
variable_p = StringVar(master)
variable_p.set(OPTIONS_PORTS[0]) # default value

ser_br = OptionMenu(frame_left, variable_br, *OPTIONS_BAUDRATES)
#styling
ser_br.configure(background = "red", activebackground = "red", fg = "white",relief=GROOVE, font=("Ink Free", 12, "bold") )
ser_br["menu"].configure(bg="red", activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
ser_br["highlightthickness"]=0
ser_br.grid(row=1, column=0, pady=(10,2))

ser_p = OptionMenu(frame_left, variable_p, *OPTIONS_PORTS)
#styling
ser_p.configure(background = "red", activebackground = "red", fg = "white", relief=GROOVE, font=("Ink Free", 12, "bold"))
ser_p["menu"].configure(bg="red", activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
ser_p["highlightthickness"]=0
ser_p.grid(row=2, column=0, pady =(0,2))
#button for serial connection
ser_ok = Button(frame_left, text="OK", command=ok, background = "red",  activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
ser_ok.grid(row=3, column=0)
#button for graph
h_view = Button(frame_left, text="measure", command=button_ecg, background = "red",  activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
h_view.grid(row=9, column=0)
#button for sampling rate
s_view = Button(frame_left, text="change", command=button_sample, background = "red",  activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
s_view.grid(row=8, column=2, padx=(10,0))
#button for measuring bpm
bpm = Button(frame_left, text="bpm", command=bpm_button, background = "red",  activebackground = "red", fg = "white", font=("Ink Free", 12, "bold"))
bpm.grid(row=6, column=0)
#bpm label for value
label = Label(frame_left, text=var, background = "white", fg = "red", font=("Ink Free", 11) )
label.grid(row=5, column=0)
#sampling rate entry
stext = Entry(frame_left, width =10)
stext.insert(0 , "4")
stext.configure(fg = "red",font=("Ink Free", 12))
stext.grid(row=8, column=0)
#section titles
title = Label(frame_left, text= "Serial Connection", background = "white", fg = "red", font=("Ink Free", 12, "bold"))
title.grid(row=0, column =0)

title2 = Label(frame_left,text="Measure bpm", background = "white", fg = "red", font=("Ink Free", 12, "bold"))
title2.grid(row=4, column=0, pady=(20,0))

title3 = Label(frame_left,text="Graph ECG", background = "white", fg = "red", font=("Ink Free", 12, "bold"))
title3.grid(row=7, column=0, pady=(20,0))

label2 = Label(frame_left,text="Hz", background = "white", fg = "red", font=("Ink Free", 12 ))
label2.grid(row=8, column=1)
#canvas to hold graph
canvas = FigureCanvasTkAgg(figure=fig, master=frame_center)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0)#.pack(side=TOP, anchor=NW, fill=None, expand=False)
#styling window
frame_left.configure(background = "white")
frame_center.configure(background = "white")
master.configure(background = "white")
master.iconbitmap('hnet.com-image.ico')
master.resizable(False, False)
master.mainloop()