    def __init__(self, marker_pad=0.3, numpoints=None, **kwargs):
        """
        Parameters
        ----------
        marker_pad : float
            Padding between points in legend entry.
        numpoints : int
            Number of points to show in legend entry.
        **kwargs
            Keyword arguments forwarded to `.HandlerBase`.
        """
        super().__init__(**kwargs)

        self._numpoints = numpoints
        self._marker_pad = marker_pad
