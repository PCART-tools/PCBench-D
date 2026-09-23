    def icol(self, i):
        """
        DEPRECATED. Use ``.iloc[:, i]`` instead
        """
        warnings.warn("icol(i) is deprecated. Please use .iloc[:,i]",
                      FutureWarning, stacklevel=2)
        return self._ixs(i, axis=1)
