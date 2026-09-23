    def set_markeredgewidth(self, ew):
        """
        Set the marker edge width in points.

        Parameters
        ----------
        ew : float
        """
        if ew is None:
            ew = rcParams['lines.markeredgewidth']
        if self._markeredgewidth != ew:
            self.stale = True
        self._markeredgewidth = ew
