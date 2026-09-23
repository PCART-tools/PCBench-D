    def get_values(self):
        """
        Same as values (but handles sparseness conversions); is a view.

        .. deprecated:: 0.25.0
            Use :meth:`Series.to_numpy` or :attr:`Series.array` instead.

        Returns
        -------
        numpy.ndarray
            Data of the Series.
        """
        warnings.warn(
            "The 'get_values' method is deprecated and will be removed in a "
            "future version. Use '.to_numpy()' or '.array' instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._internal_get_values()
