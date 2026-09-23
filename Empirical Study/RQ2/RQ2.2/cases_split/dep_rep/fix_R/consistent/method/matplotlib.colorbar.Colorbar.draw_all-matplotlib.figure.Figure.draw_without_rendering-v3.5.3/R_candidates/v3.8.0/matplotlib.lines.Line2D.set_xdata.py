    def set_xdata(self, x):
        """
        Set the data array for x.

        Parameters
        ----------
        x : 1D array
        """
        if not np.iterable(x):
            # When deprecation cycle is completed
            # raise RuntimeError('x must be a sequence')
            _api.warn_deprecated(
                since="3.7",
                message="Setting data with a non sequence type "
                "is deprecated since %(since)s and will be "
                "remove %(removal)s")
            x = [x, ]
        self._xorig = copy.copy(x)
        self._invalidx = True
        self.stale = True
