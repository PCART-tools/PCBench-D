    def __init__(self, numpoints=None, yoffsets=None, **kw):
        """
        Parameters
        ----------
        numpoints : int
            Number of points to show in legend entry.

        yoffsets : array of floats
            Length *numpoints* list of y offsets for each point in
            legend entry.

        Notes
        -----
        Any other keyword arguments are given to `HandlerNpoints`.
        """
        HandlerNpoints.__init__(self, numpoints=numpoints, **kw)
        self._yoffsets = yoffsets
