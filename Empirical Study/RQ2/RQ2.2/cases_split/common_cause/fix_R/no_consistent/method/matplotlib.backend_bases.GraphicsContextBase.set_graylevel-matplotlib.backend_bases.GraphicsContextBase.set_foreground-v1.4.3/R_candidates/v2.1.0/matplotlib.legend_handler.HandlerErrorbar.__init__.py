    def __init__(self, xerr_size=0.5, yerr_size=None,
                 marker_pad=0.3, numpoints=None, **kw):

        self._xerr_size = xerr_size
        self._yerr_size = yerr_size

        HandlerLine2D.__init__(self, marker_pad=marker_pad, numpoints=numpoints,
                               **kw)
