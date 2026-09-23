    def set_value(self, index, col, value, takeable=False):
        """
        Put single value at passed column and index.

        .. deprecated:: 0.21.0
            Use .at[] or .iat[] accessors instead.

        Parameters
        ----------
        index : row label
        col : column label
        value : scalar
        takeable : interpret the index/col as indexers, default False

        Returns
        -------
        DataFrame
            If label pair is contained, will be reference to calling DataFrame,
            otherwise a new object.
        """
        warnings.warn(
            "set_value is deprecated and will be removed "
            "in a future release. Please use "
            ".at[] or .iat[] accessors instead",
            FutureWarning,
            stacklevel=2,
        )
        return self._set_value(index, col, value, takeable=takeable)
