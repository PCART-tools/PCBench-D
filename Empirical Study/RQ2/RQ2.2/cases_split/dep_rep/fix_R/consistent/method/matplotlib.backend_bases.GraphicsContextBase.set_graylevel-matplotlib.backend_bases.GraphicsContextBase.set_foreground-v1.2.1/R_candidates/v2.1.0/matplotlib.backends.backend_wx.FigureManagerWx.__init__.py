    def __init__(self, canvas, num, frame):
        DEBUG_MSG("__init__()", 1, self)
        FigureManagerBase.__init__(self, canvas, num)
        self.frame = frame
        self.window = frame

        self.tb = frame.GetToolBar()
        self.toolbar = self.tb  # consistent with other backends

        def notify_axes_change(fig):
            'this will be called whenever the current axes is changed'
            if self.tb is not None:
                self.tb.update()
        self.canvas.figure.add_axobserver(notify_axes_change)
