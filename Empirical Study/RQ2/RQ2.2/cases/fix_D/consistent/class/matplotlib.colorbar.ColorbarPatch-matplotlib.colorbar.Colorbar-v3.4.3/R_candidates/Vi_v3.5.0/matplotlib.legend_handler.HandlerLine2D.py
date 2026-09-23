class HandlerLine2D(HandlerNpoints):
    """
    Handler for `.Line2D` instances.

    See Also
    --------
    HandlerLine2DCompound : An earlier handler implementation, which used one
                            artist for the line and another for the marker(s).
    """

    def __init__(self, marker_pad=0.3, numpoints=None, **kw):
        """
        Parameters
        ----------
        marker_pad : float
            Padding between points in legend entry.
        numpoints : int
            Number of points to show in legend entry.
        **kwargs
            Keyword arguments forwarded to `.HandlerNpoints`.
        """
        HandlerNpoints.__init__(self, marker_pad=marker_pad,
                                numpoints=numpoints, **kw)

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        markevery = None
        if self.get_numpoints(legend) == 1:
            # Special case: one wants a single marker in the center
            # and a line that extends on both sides. One will use a
            # 3 points line, but only mark the #1 (i.e. middle) point.
            xdata = np.linspace(xdata[0], xdata[-1], 3)
            markevery = [1]

        ydata = np.full_like(xdata, (height - ydescent) / 2)
        legline = Line2D(xdata, ydata, markevery=markevery)

        self.update_prop(legline, orig_handle, legend)

        if legend.markerscale != 1:
            newsz = legline.get_markersize() * legend.markerscale
            legline.set_markersize(newsz)

        legline.set_transform(trans)

        return _Line2DHandleList(legline)
