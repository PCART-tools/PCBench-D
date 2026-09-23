    def set_markeredgecolor(self, ec):
        """
        Set the marker edge color.

        Parameters
        ----------
        ec : color
        """
        if ec is None:
            ec = 'auto'
        if (self._markeredgecolor is None
                or np.any(self._markeredgecolor != ec)):
            self.stale = True
        self._markeredgecolor = ec
