    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return a boolean if the values are equal or increasing.

        Returns
        -------
        bool

        See Also
        --------
        Index.is_monotonic_decreasing : Check if the values are equal or decreasing.

        Examples
        --------
        >>> pd.Index([1, 2, 3]).is_monotonic_increasing
        True
        >>> pd.Index([1, 2, 2]).is_monotonic_increasing
        True
        >>> pd.Index([1, 3, 2]).is_monotonic_increasing
        False
        """
        return self._engine.is_monotonic_increasing
