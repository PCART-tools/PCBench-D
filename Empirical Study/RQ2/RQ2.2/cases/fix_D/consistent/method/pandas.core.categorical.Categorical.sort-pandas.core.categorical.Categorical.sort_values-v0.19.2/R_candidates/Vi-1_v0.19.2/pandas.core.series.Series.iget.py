    def iget(self, i, axis=0):
        """
        DEPRECATED. Use ``.iloc[i]`` or ``.iat[i]`` instead
        """

        warnings.warn("iget(i) is deprecated. Please use .iloc[i] or .iat[i]",
                      FutureWarning, stacklevel=2)
        return self._ixs(i)
