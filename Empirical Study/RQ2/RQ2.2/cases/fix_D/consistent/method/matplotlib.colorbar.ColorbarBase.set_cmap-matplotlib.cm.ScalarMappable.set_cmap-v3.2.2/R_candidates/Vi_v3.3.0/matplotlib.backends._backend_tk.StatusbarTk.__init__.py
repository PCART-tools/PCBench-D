    def __init__(self, window, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        xmin, xmax = self.toolmanager.canvas.figure.bbox.intervalx
        height, width = 50, xmax - xmin
        tk.Frame.__init__(self, master=window,
                          width=int(width), height=int(height),
                          borderwidth=2)
        self._message = tk.StringVar(master=self)
        self._message_label = tk.Label(master=self, textvariable=self._message)
        self._message_label.pack(side=tk.RIGHT)
        self.pack(side=tk.TOP, fill=tk.X)
