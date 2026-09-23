    def set_markersize(self, sz):
        """
        Set the marker size in points.

        Parameters
        ----------
        sz : float
             Marker size, in points.
        """
        sz = float(sz)
        if self._markersize != sz:
            self.stale = True
        self._markersize = sz
