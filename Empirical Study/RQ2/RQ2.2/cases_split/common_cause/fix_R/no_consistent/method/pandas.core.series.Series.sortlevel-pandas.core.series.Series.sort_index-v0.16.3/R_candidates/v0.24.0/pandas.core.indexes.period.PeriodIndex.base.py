    @property
    def base(self):
        """ return the base object if the memory of the underlying data is
        shared
        """
        warnings.warn("{obj}.base is deprecated and will be removed "
                      "in a future version".format(obj=type(self).__name__),
                      FutureWarning, stacklevel=2)
        return np.asarray(self._data)
