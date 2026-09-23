    def set_xdata(self, x):
        """
        Set the data array for x.

        Parameters
        ----------
        x : 1D array
        """
        self._xorig = copy.copy(x)
        self._invalidx = True
        self.stale = True
