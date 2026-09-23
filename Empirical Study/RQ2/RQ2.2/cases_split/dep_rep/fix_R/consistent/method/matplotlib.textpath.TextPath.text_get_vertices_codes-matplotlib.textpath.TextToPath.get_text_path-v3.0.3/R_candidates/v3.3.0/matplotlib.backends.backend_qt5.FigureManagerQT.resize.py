    def resize(self, width, height):
        # these are Qt methods so they return sizes in 'virtual' pixels
        # so we do not need to worry about dpi scaling here.
        extra_width = self.window.width() - self.canvas.width()
        extra_height = self.window.height() - self.canvas.height()
        self.canvas.resize(width, height)
        self.window.resize(width + extra_width, height + extra_height)
