    def __init__(self, canvas, num, frame):
        _log.debug("%s - __init__()", type(self))
        self.frame = self.window = frame
        super().__init__(canvas, num)
