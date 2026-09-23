    def __init__(self, canvas, window):
        self.canvas = canvas
        # Avoid using self.window (prefer self.canvas.get_tk_widget().master),
        # so that Tool implementations can reuse the methods.
        self.window = window
        NavigationToolbar2.__init__(self, canvas)
