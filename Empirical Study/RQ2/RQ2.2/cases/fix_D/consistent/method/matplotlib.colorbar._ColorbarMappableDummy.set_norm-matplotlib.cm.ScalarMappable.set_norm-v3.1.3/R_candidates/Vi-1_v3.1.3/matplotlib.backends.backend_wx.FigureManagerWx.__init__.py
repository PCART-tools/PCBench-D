    def __init__(self, canvas, num, frame):
        DEBUG_MSG("__init__()", 1, self)
        FigureManagerBase.__init__(self, canvas, num)
        self.frame = frame
        self.window = frame

        self.toolmanager = getattr(frame, "toolmanager", None)
        self.toolbar = frame.GetToolBar()
