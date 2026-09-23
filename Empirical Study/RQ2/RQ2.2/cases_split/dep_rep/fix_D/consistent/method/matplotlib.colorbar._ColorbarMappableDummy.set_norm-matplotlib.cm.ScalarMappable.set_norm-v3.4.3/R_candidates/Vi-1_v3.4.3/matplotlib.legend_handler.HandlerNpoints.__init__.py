    def __init__(self, marker_pad=0.3, numpoints=None, **kw):
        """
        Parameters
        ----------
        marker_pad : float
            Padding between points in legend entry.

        numpoints : int
            Number of points to show in legend entry.

        Notes
        -----
        Any other keyword arguments are given to `HandlerBase`.
        """
        super().__init__(**kw)

        self._numpoints = numpoints
        self._marker_pad = marker_pad
