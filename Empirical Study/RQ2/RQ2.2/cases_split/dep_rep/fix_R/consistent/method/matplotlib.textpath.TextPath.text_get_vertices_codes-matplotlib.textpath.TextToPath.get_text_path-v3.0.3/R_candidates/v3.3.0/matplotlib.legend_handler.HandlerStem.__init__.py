    def __init__(self, marker_pad=0.3, numpoints=None,
                 bottom=None, yoffsets=None, **kw):
        """
        Parameters
        ----------
        marker_pad : float, default: 0.3
            Padding between points in legend entry.

        numpoints : int, optional
            Number of points to show in legend entry.

        bottom : float, optional

        yoffsets : array of floats, optional
            Length *numpoints* list of y offsets for each point in
            legend entry.

        Notes
        -----
        Any other keyword arguments are given to `HandlerNpointsYoffsets`.
        """

        HandlerNpointsYoffsets.__init__(self, marker_pad=marker_pad,
                                        numpoints=numpoints,
                                        yoffsets=yoffsets,
                                        **kw)
        self._bottom = bottom
