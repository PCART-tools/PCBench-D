    def set_ydata(self, y):
        """
        Set the data array for y.

        Parameters
        ----------
        y : 1D array

        See Also
        --------
        set_data
        set_xdata
        """
        if not np.iterable(y):
            raise RuntimeError('y must be a sequence')
        self._yorig = copy.copy(y)
        self._invalidy = True
        self.stale = True
