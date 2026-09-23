    def __init__(self, canvas, window):
        self.win = window
        GObject.GObject.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self.ctx = None
