    def __init__(self, toolmanager, window):
        ToolContainerBase.__init__(self, toolmanager)
        xmin, xmax = self.toolmanager.canvas.figure.bbox.intervalx
        height, width = 50, xmax - xmin
        Tk.Frame.__init__(self, master=window,
                          width=int(width), height=int(height),
                          borderwidth=2)
        self._toolitems = {}
        self.pack(side=Tk.TOP, fill=Tk.X)
        self._groups = {}
