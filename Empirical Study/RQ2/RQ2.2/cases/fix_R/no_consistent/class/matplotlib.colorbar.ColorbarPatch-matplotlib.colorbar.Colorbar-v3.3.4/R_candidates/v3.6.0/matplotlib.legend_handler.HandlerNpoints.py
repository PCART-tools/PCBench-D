class HandlerNpoints(HandlerBase):
    """
    A legend handler that shows *numpoints* points in the legend entry.
    """

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

    def get_numpoints(self, legend):
        if self._numpoints is None:
            return legend.numpoints
        else:
            return self._numpoints

    def get_xdata(self, legend, xdescent, ydescent, width, height, fontsize):
        numpoints = self.get_numpoints(legend)
        if numpoints > 1:
            # we put some pad here to compensate the size of the marker
            pad = self._marker_pad * fontsize
            xdata = np.linspace(-xdescent + pad,
                                -xdescent + width - pad,
                                numpoints)
            xdata_marker = xdata
        else:
            xdata = [-xdescent, -xdescent + width]
            xdata_marker = [-xdescent + 0.5 * width]
        return xdata, xdata_marker
