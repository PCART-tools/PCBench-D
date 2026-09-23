    def __init__(self, canvas, num, window):
        FigureManagerBase.__init__(self, canvas, num)
        self.window = window
        self.window.withdraw()
        self.set_window_title("Figure %d" % num)
        # packing toolbar first, because if space is getting low, last packed
        # widget is getting shrunk first (-> the canvas)
        self.toolbar = self._get_toolbar()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)

        self._shown = False
