    def irow(self, i, copy=False):
        """
        DEPRECATED. Use ``.iloc[i]`` instead
        """

        warnings.warn("irow(i) is deprecated. Please use .iloc[i]",
                      FutureWarning, stacklevel=2)
        return self._ixs(i, axis=0)
