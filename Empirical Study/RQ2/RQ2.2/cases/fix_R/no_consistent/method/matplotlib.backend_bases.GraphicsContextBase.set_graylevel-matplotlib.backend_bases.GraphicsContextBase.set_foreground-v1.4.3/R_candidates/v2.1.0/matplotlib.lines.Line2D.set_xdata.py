    def set_xdata(self, x):
        """
        Set the data np.array for x

        ACCEPTS: 1D array
        """
        self._xorig = x
        self._invalidx = True
        self.stale = True
