    def __init__(self, xerr_size=0.5, yerr_size=None,
                 marker_pad=0.3, numpoints=None, **kwargs):

        self._xerr_size = xerr_size
        self._yerr_size = yerr_size

        super().__init__(marker_pad=marker_pad, numpoints=numpoints, **kwargs)
