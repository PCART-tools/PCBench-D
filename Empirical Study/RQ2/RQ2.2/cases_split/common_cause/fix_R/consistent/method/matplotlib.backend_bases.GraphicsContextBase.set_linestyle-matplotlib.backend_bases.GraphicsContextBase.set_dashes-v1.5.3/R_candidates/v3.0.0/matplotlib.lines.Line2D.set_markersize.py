    def set_markersize(self, sz):
        """
        Set the marker size in points.

        Parameters
        ----------
        sz : float
        """
        sz = float(sz)
        if self._markersize != sz:
            self.stale = True
        self._markersize = sz
