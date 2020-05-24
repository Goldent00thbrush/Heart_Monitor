from tkinter import *
import serial
import serial.tools.list_ports
from random import randrange
from tkinter import Tk
from tkinter import Button
from tkinter import BOTH, BOTTOM, TOP, RIGHT,LEFT, X, Y, NW
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import datetime as dt
import string
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def popup_bonus():
    win = Toplevel()
    win.wm_title("Serial Connection")

    l = Label(win, text="Cannot connect to serial port")
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

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

def connect(s):
    try:
        global ser
        ser = serial.Serial(s)
        ser.baudrate = 115200
        getVal(variable_br.get())
    except serial.serialutil.SerialException:
        popup_bonus()


def data_ecg(): #1 minute worth of data
    global ser
    return int(ser.readline().decode("utf-8"))

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global ani_flag
    # Read temperature (Celsius) from TMP102
    temp_c =data_ecg()

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(temp_c)

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

def button_ecg():
    global ser
    global fig, xs, ys, canvas
    global master
    if (ser == None):
        popup_bonus()
        return
    ser.write(bytes(b'g'))
    ser.write(bytes(b'g'))
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10, frames=241, repeat=False)
    canvas.draw()
    master.mainloop()

def ok():
   connect(variable_p.get())

def bpm_button():
    global master
    global ser, label
    if (ser == None):
        popup_bonus()
        return
    ser.write(bytes(b'h'))
    var = ser.readline().decode("utf-8")
    label.configure(text=var)

OPTIONS_BAUDRATES = [ "256000","128000", "115200","57600", "56000", "38400", "19200", "14400", "9600" , "4800", "2400", "1200"]
OPTIONS_PORTS = [p.device for p in list(serial.tools.list_ports.comports())]
master = Tk()
master.title("Heart Rate Monitor")
ser = None
var = '0'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

frame_left = Frame(master)
frame_left.grid(row=0, column=0,sticky='N')
frame_center = Frame(master)
frame_center.grid(row=0, column =1,sticky='N', padx=(10,0))


variable_br = StringVar(master)
variable_br.set(OPTIONS_BAUDRATES[2]) # default value
variable_p = StringVar(master)
variable_p.set(OPTIONS_PORTS[0]) # default value

title = Label(frame_left, text= "Serial Connection")
title.grid(row=0, column =0)

ser_br = OptionMenu(frame_left, variable_br, *OPTIONS_BAUDRATES)
ser_br.grid(row=1, column=0)

ser_p = OptionMenu(frame_left, variable_p, *OPTIONS_PORTS)
ser_p.grid(row=2, column=0)

ser_ok = Button(frame_left, text="OK", command=ok)
ser_ok.grid(row=3, column=0)

h_view = Button(frame_left, text="measure", command=button_ecg)
h_view.grid(row=7, column=0)

bpm = Button(frame_left, text="bpm", command=bpm_button)
bpm.grid(row=5, column=1)

label = Label(frame_left, text=var)
label.grid(row=5, column=0)

title2 = Label(frame_left,text="Measure bpm")
title2.grid(row=4, column=0, pady=(20,0))

title3 = Label(frame_left,text="Graph ECG")
title3.grid(row=6, column=0, pady=(20,0))

canvas = FigureCanvasTkAgg(figure=fig, master=frame_center)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0)#.pack(side=TOP, anchor=NW, fill=None, expand=False)


master.mainloop()