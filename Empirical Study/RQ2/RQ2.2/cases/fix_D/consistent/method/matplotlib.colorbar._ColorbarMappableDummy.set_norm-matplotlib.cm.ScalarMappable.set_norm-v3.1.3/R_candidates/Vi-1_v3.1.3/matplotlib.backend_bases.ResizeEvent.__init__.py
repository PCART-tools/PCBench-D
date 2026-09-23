    def __init__(self, name, canvas):
        Event.__init__(self, name, canvas)
        self.width, self.height = canvas.get_width_height()
