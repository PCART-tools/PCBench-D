    def __init__(self, canvas, num, frame):
        _log.debug("%s - __init__()", type(self))
        FigureManagerBase.__init__(self, canvas, num)
        self.frame = frame
        self.window = frame
