    def get_value(self, index, col, takeable=False):
        """
        Quickly retrieve single value at passed column and index.

        .. deprecated:: 0.21.0
            Use .at[] or .iat[] accessors instead.

        Parameters
        ----------
        index : row label
        col : column label
        takeable : interpret the index/col as indexers, default False

        Returns
        -------
        value : scalar value
        """

        warnings.warn("get_value is deprecated and will be removed "
                      "in a future release. Please use "
                      ".at[] or .iat[] accessors instead", FutureWarning,
                      stacklevel=2)
        return self._get_value(index, col, takeable=takeable)
