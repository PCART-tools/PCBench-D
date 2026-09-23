    def __init__(self, canvas, num, frame):
        _log.debug("%s - __init__()", type(self))
        self.frame = self.window = frame
        self._initializing = True
        super().__init__(canvas, num)
        self._initializing = False
