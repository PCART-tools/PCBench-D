    def iget_value(self, i, j):
        """
        DEPRECATED. Use ``.iat[i, j]`` instead
        """
        warnings.warn("iget_value(i, j) is deprecated. Please use .iat[i, j]",
                      FutureWarning, stacklevel=2)
        return self.iat[i, j]
