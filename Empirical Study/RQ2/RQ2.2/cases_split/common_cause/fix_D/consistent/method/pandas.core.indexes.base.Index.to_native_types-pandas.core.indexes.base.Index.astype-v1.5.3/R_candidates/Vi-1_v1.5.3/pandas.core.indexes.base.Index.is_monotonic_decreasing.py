    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return a boolean if the values are equal or decreasing.

        Examples
        --------
        >>> Index([3, 2, 1]).is_monotonic_decreasing
        True
        >>> Index([3, 2, 2]).is_monotonic_decreasing
        True
        >>> Index([3, 1, 2]).is_monotonic_decreasing
        False
        """
        return self._engine.is_monotonic_decreasing
