    def __init__(self, name, canvas, x, y, guiEvent=None, *, modifiers=None):
        super().__init__(name, canvas, guiEvent=guiEvent)
        # x position - pixels from left of canvas
        self.x = int(x) if x is not None else x
        # y position - pixels from right of canvas
        self.y = int(y) if y is not None else y
        self.inaxes = None  # the Axes instance the mouse is over
        self.xdata = None   # x coord of mouse in data coords
        self.ydata = None   # y coord of mouse in data coords
        self.modifiers = frozenset(modifiers if modifiers is not None else [])

        if x is None or y is None:
            # cannot check if event was in Axes if no (x, y) info
            return

        if self.canvas.mouse_grabber is None:
            self.inaxes = self.canvas.inaxes((x, y))
        else:
            self.inaxes = self.canvas.mouse_grabber

        if self.inaxes is not None:
            try:
                trans = self.inaxes.transData.inverted()
                xdata, ydata = trans.transform((x, y))
            except ValueError:
                pass
            else:
                self.xdata = xdata
                self.ydata = ydata
