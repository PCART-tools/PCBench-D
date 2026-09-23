class LocationEvent(Event):
    """
    An event that has a screen location.

    A LocationEvent has a number of special attributes in addition to those
    defined by the parent `Event` class.

    Attributes
    ----------
    x, y : int or None
        Event location in pixels from bottom left of canvas.
    inaxes : `~.axes.Axes` or None
        The `~.axes.Axes` instance over which the mouse is, if any.
    xdata, ydata : float or None
        Data coordinates of the mouse within *inaxes*, or *None* if the mouse
        is not over an Axes.
    """

    lastevent = None  # The last event processed so far.

    def __init__(self, name, canvas, x, y, guiEvent=None):
        super().__init__(name, canvas, guiEvent=guiEvent)
        # x position - pixels from left of canvas
        self.x = int(x) if x is not None else x
        # y position - pixels from right of canvas
        self.y = int(y) if y is not None else y
        self.inaxes = None  # the Axes instance the mouse is over
        self.xdata = None   # x coord of mouse in data coords
        self.ydata = None   # y coord of mouse in data coords

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
