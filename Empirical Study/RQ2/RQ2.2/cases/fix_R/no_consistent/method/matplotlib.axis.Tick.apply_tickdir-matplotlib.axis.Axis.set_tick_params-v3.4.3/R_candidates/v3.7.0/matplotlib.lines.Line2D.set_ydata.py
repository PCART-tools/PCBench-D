    def set_ydata(self, y):
        """
        Set the data array for y.

        Parameters
        ----------
        y : 1D array
        """
        if not np.iterable(y):
            # When deprecation cycle is completed
            # raise RuntimeError('y must be a sequence')
            _api.warn_deprecated(
                since=3.7,
                message="Setting data with a non sequence type "
                "is deprecated since %(since)s and will be "
                "remove %(removal)s")
            y = [y, ]
        self._yorig = copy.copy(y)
        self._invalidy = True
        self.stale = True
