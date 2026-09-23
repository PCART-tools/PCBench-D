    def iget_value(self, i, axis=0):
        """
        DEPRECATED. Use ``.iloc[i]`` or ``.iat[i]`` instead
        """
        warnings.warn("iget_value(i) is deprecated. Please use .iloc[i] or "
                      ".iat[i]", FutureWarning, stacklevel=2)
        return self._ixs(i)
