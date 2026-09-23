    def set_xdata(self, x):
        """
        Set the data array for x.

        Parameters
        ----------
        x : 1D array

        See Also
        --------
        set_data
        set_ydata
        """
        if not np.iterable(x):
            raise RuntimeError('x must be a sequence')
        self._xorig = copy.copy(x)
        self._invalidx = True
        self.stale = True
