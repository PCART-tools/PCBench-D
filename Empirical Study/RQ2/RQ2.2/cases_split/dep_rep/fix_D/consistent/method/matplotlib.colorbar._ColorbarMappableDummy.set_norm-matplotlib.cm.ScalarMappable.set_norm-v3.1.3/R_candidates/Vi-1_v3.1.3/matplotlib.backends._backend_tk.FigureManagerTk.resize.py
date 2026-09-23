    def resize(self, width, height):
        self.canvas._tkcanvas.master.geometry("%dx%d" % (width, height))

        if self.toolbar is not None:
            self.toolbar.configure(width=width)
