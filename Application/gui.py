from tkinter import Tk
from tkinter import BOTH, BOTTOM, TOP, RIGHT,LEFT, X, Y, NW
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

root = Tk()
root.title("Heart Rate Monitor")

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
canvas = FigureCanvasTkAgg(figure=f,master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP,anchor=NW, fill=None, expand=False)

root.mainloop()

