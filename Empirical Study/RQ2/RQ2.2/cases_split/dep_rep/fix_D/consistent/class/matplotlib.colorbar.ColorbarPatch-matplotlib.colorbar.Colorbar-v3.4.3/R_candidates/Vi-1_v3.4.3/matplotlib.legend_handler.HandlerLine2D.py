class HandlerLine2D(HandlerNpoints):
    """
    Handler for `.Line2D` instances.
    """
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
        Any other keyword arguments are given to `HandlerNpoints`.
        """
        super().__init__(marker_pad=marker_pad, numpoints=numpoints, **kw)

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        ydata = np.full_like(xdata, ((height - ydescent) / 2))
        legline = Line2D(xdata, ydata)

        self.update_prop(legline, orig_handle, legend)
        legline.set_drawstyle('default')
        legline.set_marker("")

        legline_marker = Line2D(xdata_marker, ydata[:len(xdata_marker)])
        self.update_prop(legline_marker, orig_handle, legend)
        legline_marker.set_linestyle('None')
        if legend.markerscale != 1:
            newsz = legline_marker.get_markersize() * legend.markerscale
            legline_marker.set_markersize(newsz)
        # we don't want to add this to the return list because
        # the texts and handles are assumed to be in one-to-one
        # correspondence.
        legline._legmarker = legline_marker

        legline.set_transform(trans)
        legline_marker.set_transform(trans)

        return [legline, legline_marker]
