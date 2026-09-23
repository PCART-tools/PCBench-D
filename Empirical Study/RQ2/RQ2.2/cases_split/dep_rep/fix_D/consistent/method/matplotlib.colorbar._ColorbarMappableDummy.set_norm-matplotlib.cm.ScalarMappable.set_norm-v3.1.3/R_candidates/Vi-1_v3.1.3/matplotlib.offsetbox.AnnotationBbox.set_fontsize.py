    def set_fontsize(self, s=None):
        """
        set fontsize in points
        """
        if s is None:
            s = rcParams["legend.fontsize"]

        self.prop = FontProperties(size=s)
        self.stale = True
