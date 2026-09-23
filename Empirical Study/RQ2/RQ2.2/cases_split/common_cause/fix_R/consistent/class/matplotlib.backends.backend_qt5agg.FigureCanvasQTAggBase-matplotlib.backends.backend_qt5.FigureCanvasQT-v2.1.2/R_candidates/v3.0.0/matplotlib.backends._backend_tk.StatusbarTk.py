class StatusbarTk(StatusbarBase, Tk.Frame):
    def __init__(self, window, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        xmin, xmax = self.toolmanager.canvas.figure.bbox.intervalx
        height, width = 50, xmax - xmin
        Tk.Frame.__init__(self, master=window,
                          width=int(width), height=int(height),
                          borderwidth=2)
        self._message = Tk.StringVar(master=self)
        self._message_label = Tk.Label(master=self, textvariable=self._message)
        self._message_label.pack(side=Tk.RIGHT)
        self.pack(side=Tk.TOP, fill=Tk.X)

    def set_message(self, s):
        self._message.set(s)
