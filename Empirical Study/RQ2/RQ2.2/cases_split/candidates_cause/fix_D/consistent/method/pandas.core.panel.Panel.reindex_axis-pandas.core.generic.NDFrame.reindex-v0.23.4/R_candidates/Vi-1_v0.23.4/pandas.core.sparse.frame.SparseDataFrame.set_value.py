    def set_value(self, index, col, value, takeable=False):
        """
        Put single value at passed column and index

        .. deprecated:: 0.21.0

        Please use .at[] or .iat[] accessors.

        Parameters
        ----------
        index : row label
        col : column label
        value : scalar value
        takeable : interpret the index/col as indexers, default False

        Notes
        -----
        This method *always* returns a new object. It is currently not
        particularly efficient (and potentially very expensive) but is provided
        for API compatibility with DataFrame

        Returns
        -------
        frame : DataFrame
        """
        warnings.warn("set_value is deprecated and will be removed "
                      "in a future release. Please use "
                      ".at[] or .iat[] accessors instead", FutureWarning,
                      stacklevel=2)
        return self._set_value(index, col, value, takeable=takeable)
