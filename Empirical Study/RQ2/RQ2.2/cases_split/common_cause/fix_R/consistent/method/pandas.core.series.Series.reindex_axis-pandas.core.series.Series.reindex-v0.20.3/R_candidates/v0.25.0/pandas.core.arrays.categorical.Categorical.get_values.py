    def get_values(self):
        """
        Return the values.

        .. deprecated:: 0.25.0

        For internal compatibility with pandas formatting.

        Returns
        -------
        numpy.array
            A numpy array of the same dtype as categorical.categories.dtype or
            Index if datetime / periods.
        """
        warn(
            "The 'get_values' method is deprecated and will be removed in a "
            "future version",
            FutureWarning,
            stacklevel=2,
        )
        return self._internal_get_values()
