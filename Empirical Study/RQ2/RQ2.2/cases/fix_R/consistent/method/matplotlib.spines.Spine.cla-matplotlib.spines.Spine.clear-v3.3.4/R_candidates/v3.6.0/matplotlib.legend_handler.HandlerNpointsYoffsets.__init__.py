    def __init__(self, numpoints=None, yoffsets=None, **kwargs):
        """
        Parameters
        ----------
        numpoints : int
            Number of points to show in legend entry.
        yoffsets : array of floats
            Length *numpoints* list of y offsets for each point in
            legend entry.
        **kwargs
            Keyword arguments forwarded to `.HandlerNpoints`.
        """
        super().__init__(numpoints=numpoints, **kwargs)
        self._yoffsets = yoffsets
