    def __init__(self, canvas, window):
        self.canvas = canvas
        self.window = window
        self._idle = True
        NavigationToolbar2.__init__(self, canvas)
