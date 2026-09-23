    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return if the index is monotonic increasing (only equal or
        increasing) values.

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
