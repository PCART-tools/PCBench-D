    def resize(self, width, height=None):
        # before 09-12-22, the resize method takes a single *event*
        # parameter. On the other hand, the resize method of other
        # FigureManager class takes *width* and *height* parameter,
        # which is used to change the size of the window. For the
        # Figure.set_size_inches with forward=True work with Tk
        # backend, I changed the function signature but tried to keep
        # it backward compatible. -JJL

        # when a single parameter is given, consider it as a event
        if height is None:
            width = width.width
        else:
            self.canvas._tkcanvas.master.geometry("%dx%d" % (width, height))

        if self.toolbar is not None:
            self.toolbar.configure(width=width)
