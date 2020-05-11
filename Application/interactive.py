import datetime as dt
import string

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
ser = serial.Serial('COM6')
ser.baudrate = 115200

def data2(): #1 minute worth of data
    return int(ser.readline().decode("utf-8"))

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = data2()

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

# Set up plot to call animate() function periodically
ser.write(bytes(b'g'))
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
plt.show()
ser.close()





