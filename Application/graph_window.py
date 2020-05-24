def graph_window():


    root = tk.Tk()
    root.wm_title("Graph window")

    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)


    def animate(i):
        c = app.cursor
        c.execute("SELECT time, windspeed FROM data")
        fetch = c.fetchall()

        Xaxes = [x for (x, y) in fetch]
        Yaxes = [y for (x, y) in fetch]


        #test3 = np.array(test)
        pltYaxes = np.array(Yaxes)
        pltXaxes = np.array(Xaxes)

        a.clear()
        a.plot(pltXaxes,pltYaxes)

    canvas = FigureCanvasTkAgg(f, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    root.ani = animation.FuncAnimation(f,animate, interval=5000)


    tk.mainloop()

AirVelocity = tk.Button(self, text="Air Velocity", command=graph_window)

AirVelocity.grid(row=4, column=0)