    def set_ydata(self, y):
        """
        Set the data array for y.

        Parameters
        ----------
        y : 1D array
        """
        self._yorig = copy.copy(y)
        self._invalidy = True
        self.stale = True
