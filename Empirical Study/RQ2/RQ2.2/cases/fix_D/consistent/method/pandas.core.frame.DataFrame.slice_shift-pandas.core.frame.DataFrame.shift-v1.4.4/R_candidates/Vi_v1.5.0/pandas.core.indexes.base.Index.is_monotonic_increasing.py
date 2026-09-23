    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return a boolean if the values are equal or increasing.

        Examples
        --------
        >>> Index([1, 2, 3]).is_monotonic_increasing
        True
        >>> Index([1, 2, 2]).is_monotonic_increasing
        True
        >>> Index([1, 3, 2]).is_monotonic_increasing
        False
        """
        return self._engine.is_monotonic_increasing
