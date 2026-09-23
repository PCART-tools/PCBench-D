class AxesWidget(Widget):
    """
    Widget connected to a single `~matplotlib.axes.Axes`.

    To guarantee that the widget remains responsive and not garbage-collected,
    a reference to the object should be maintained by the user.

    This is necessary because the callback registry
    maintains only weak-refs to the functions, which are member
    functions of the widget.  If there are no references to the widget
    object it may be garbage collected which will disconnect the callbacks.

    Attributes
    ----------
    ax : `~matplotlib.axes.Axes`
        The parent axes for the widget.
    canvas : `~matplotlib.backend_bases.FigureCanvasBase`
        The parent figure canvas for the widget.
    active : bool
        If False, the widget does not respond to events.
    """

    cids = _api.deprecated("3.4")(property(lambda self: self._cids))

    def __init__(self, ax):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self._cids = []

    def connect_event(self, event, callback):
        """
        Connect a callback function with an event.

        This should be used in lieu of ``figure.canvas.mpl_connect`` since this
        function stores callback ids for later clean up.
        """
        cid = self.canvas.mpl_connect(event, callback)
        self._cids.append(cid)

    def disconnect_events(self):
        """Disconnect all events created by this widget."""
        for c in self._cids:
            self.canvas.mpl_disconnect(c)
