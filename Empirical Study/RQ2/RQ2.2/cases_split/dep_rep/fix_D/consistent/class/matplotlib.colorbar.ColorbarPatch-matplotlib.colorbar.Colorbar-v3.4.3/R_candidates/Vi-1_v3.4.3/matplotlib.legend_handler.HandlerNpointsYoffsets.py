class HandlerNpointsYoffsets(HandlerNpoints):
    """
    A legend handler that shows *numpoints* in the legend, and allows them to
    be individually offset in the y-direction.
    """
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
        super().__init__(numpoints=numpoints, **kw)
        self._yoffsets = yoffsets

    def get_ydata(self, legend, xdescent, ydescent, width, height, fontsize):
        if self._yoffsets is None:
            ydata = height * legend._scatteryoffsets
        else:
            ydata = height * np.asarray(self._yoffsets)

        return ydata
