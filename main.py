import serial

def data(): #1 minute worth of data
    ser.write(bytes(b'g'))
    for i in range(240):
        print(ser.read(6))

def bpm(): #bmp
    print("bpm")

def samp(): #sampling rate
    print("sampling rate")
ser = serial.Serial('COM6')
#ser.open()
#ser.timeout = 1
ser.baudrate = 115200
#ser.port = '/dev/ttyUSB0'
ser.xonxoff=True
print(ser)

data()

ser.close()

