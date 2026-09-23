    def __init__(self, toolmanager, window=None):
        ToolContainerBase.__init__(self, toolmanager)
        if window is None:
            window = self.toolmanager.canvas.get_tk_widget().master
        xmin, xmax = self.toolmanager.canvas.figure.bbox.intervalx
        height, width = 50, xmax - xmin
        tk.Frame.__init__(self, master=window,
                          width=int(width), height=int(height),
                          borderwidth=2)
        self._label_font = tkinter.font.Font(size=10)
        # This filler item ensures the toolbar is always at least two text
        # lines high. Otherwise the canvas gets redrawn as the mouse hovers
        # over images because those use two-line messages which resize the
        # toolbar.
        label = tk.Label(master=self, font=self._label_font,
                         text='\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}')
        label.pack(side=tk.RIGHT)
        self._message = tk.StringVar(master=self)
        self._message_label = tk.Label(master=self, font=self._label_font,
                                       textvariable=self._message)
        self._message_label.pack(side=tk.RIGHT)
        self._toolitems = {}
        self.pack(side=tk.TOP, fill=tk.X)
        self._groups = {}
