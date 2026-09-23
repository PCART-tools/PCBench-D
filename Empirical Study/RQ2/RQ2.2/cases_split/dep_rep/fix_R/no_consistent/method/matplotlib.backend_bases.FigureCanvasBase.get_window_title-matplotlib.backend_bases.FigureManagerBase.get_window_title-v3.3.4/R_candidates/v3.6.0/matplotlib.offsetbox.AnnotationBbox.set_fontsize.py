    def set_fontsize(self, s=None):
        """
        Set the fontsize in points.

        If *s* is not given, reset to :rc:`legend.fontsize`.
        """
        if s is None:
            s = mpl.rcParams["legend.fontsize"]

        self.prop = FontProperties(size=s)
        self.stale = True
