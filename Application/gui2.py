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
import serial

def data_ecg(): #1 minute worth of data
    return int(ser.readline().decode("utf-8"))

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

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
    ser.write(bytes(b'g'))
    canvas = FigureCanvasTkAgg(figure=fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, anchor=NW, fill=None, expand=False)
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
    root.mainloop()

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
ser = serial.Serial('COM6')
ser.baudrate = 115200

root = Tk()
root.title("Heart Rate Monitor")

# Set up plot to call animate() function periodically
B = Button(root, text ="View", command = button_ecg)
B.pack()
root.mainloop()

ser.close()