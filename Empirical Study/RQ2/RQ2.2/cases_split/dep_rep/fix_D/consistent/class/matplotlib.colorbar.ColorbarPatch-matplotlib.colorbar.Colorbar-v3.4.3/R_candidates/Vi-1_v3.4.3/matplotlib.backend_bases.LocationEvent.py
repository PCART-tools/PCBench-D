class LocationEvent(Event):
    """
    An event that has a screen location.

    The following additional attributes are defined and shown with
    their default values.

    In addition to the `Event` attributes, the following
    event attributes are defined:

    Attributes
    ----------
    x : int
        x position - pixels from left of canvas.
    y : int
        y position - pixels from bottom of canvas.
    inaxes : `~.axes.Axes` or None
        The `~.axes.Axes` instance over which the mouse is, if any.
    xdata : float or None
        x data coordinate of the mouse.
    ydata : float or None
        y data coordinate of the mouse.
    """

    lastevent = None  # the last event that was triggered before this one

    def __init__(self, name, canvas, x, y, guiEvent=None):
        """
        (*x*, *y*) in figure coords ((0, 0) = bottom left).
        """
        super().__init__(name, canvas, guiEvent=guiEvent)
        # x position - pixels from left of canvas
        self.x = int(x) if x is not None else x
        # y position - pixels from right of canvas
        self.y = int(y) if y is not None else y
        self.inaxes = None  # the Axes instance if mouse us over axes
        self.xdata = None   # x coord of mouse in data coords
        self.ydata = None   # y coord of mouse in data coords

        if x is None or y is None:
            # cannot check if event was in axes if no (x, y) info
            self._update_enter_leave()
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

        self._update_enter_leave()

    def _update_enter_leave(self):
        """Process the figure/axes enter leave events."""
        if LocationEvent.lastevent is not None:
            last = LocationEvent.lastevent
            if last.inaxes != self.inaxes:
                # process axes enter/leave events
                try:
                    if last.inaxes is not None:
                        last.canvas.callbacks.process('axes_leave_event', last)
                except Exception:
                    pass
                    # See ticket 2901582.
                    # I think this is a valid exception to the rule
                    # against catching all exceptions; if anything goes
                    # wrong, we simply want to move on and process the
                    # current event.
                if self.inaxes is not None:
                    self.canvas.callbacks.process('axes_enter_event', self)

        else:
            # process a figure enter event
            if self.inaxes is not None:
                self.canvas.callbacks.process('axes_enter_event', self)

        LocationEvent.lastevent = self
