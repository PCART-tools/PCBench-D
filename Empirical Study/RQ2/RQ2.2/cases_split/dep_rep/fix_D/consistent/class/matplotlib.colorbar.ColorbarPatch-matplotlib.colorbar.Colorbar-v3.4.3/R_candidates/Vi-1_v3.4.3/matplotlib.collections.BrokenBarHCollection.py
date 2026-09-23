class BrokenBarHCollection(PolyCollection):
    """
    A collection of horizontal bars spanning *yrange* with a sequence of
    *xranges*.
    """
    def __init__(self, xranges, yrange, **kwargs):
        """
        Parameters
        ----------
        xranges : list of (float, float)
            The sequence of (left-edge-position, width) pairs for each bar.
        yrange : (float, float)
            The (lower-edge, height) common to all bars.
        **kwargs
            Forwarded to `.Collection`.
        """
        ymin, ywidth = yrange
        ymax = ymin + ywidth
        verts = [[(xmin, ymin),
                  (xmin, ymax),
                  (xmin + xwidth, ymax),
                  (xmin + xwidth, ymin),
                  (xmin, ymin)] for xmin, xwidth in xranges]
        super().__init__(verts, **kwargs)

    @classmethod
    def span_where(cls, x, ymin, ymax, where, **kwargs):
        """
        Return a `.BrokenBarHCollection` that plots horizontal bars from
        over the regions in *x* where *where* is True.  The bars range
        on the y-axis from *ymin* to *ymax*

        *kwargs* are passed on to the collection.
        """
        xranges = []
        for ind0, ind1 in cbook.contiguous_regions(where):
            xslice = x[ind0:ind1]
            if not len(xslice):
                continue
            xranges.append((xslice[0], xslice[-1] - xslice[0]))
        return cls(xranges, [ymin, ymax - ymin], **kwargs)
