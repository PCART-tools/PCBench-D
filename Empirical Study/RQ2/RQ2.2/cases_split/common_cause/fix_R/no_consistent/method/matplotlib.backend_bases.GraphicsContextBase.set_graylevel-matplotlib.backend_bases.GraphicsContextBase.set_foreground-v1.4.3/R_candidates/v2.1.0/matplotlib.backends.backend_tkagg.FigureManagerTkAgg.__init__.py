    def __init__(self, canvas, num, window):
        FigureManagerBase.__init__(self, canvas, num)
        self.window = window
        self.window.withdraw()
        self.set_window_title("Figure %d" % num)
        self.canvas = canvas
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self._num = num

        self.toolmanager = self._get_toolmanager()
        self.toolbar = self._get_toolbar()
        self.statusbar = None

        if self.toolmanager:
            backend_tools.add_tools_to_manager(self.toolmanager)
            if self.toolbar:
                backend_tools.add_tools_to_container(self.toolbar)
                self.statusbar = StatusbarTk(self.window, self.toolmanager)

        self._shown = False

        def notify_axes_change(fig):
            'this will be called whenever the current axes is changed'
            if self.toolmanager is not None:
                pass
            elif self.toolbar is not None:
                self.toolbar.update()
        self.canvas.figure.add_axobserver(notify_axes_change)
