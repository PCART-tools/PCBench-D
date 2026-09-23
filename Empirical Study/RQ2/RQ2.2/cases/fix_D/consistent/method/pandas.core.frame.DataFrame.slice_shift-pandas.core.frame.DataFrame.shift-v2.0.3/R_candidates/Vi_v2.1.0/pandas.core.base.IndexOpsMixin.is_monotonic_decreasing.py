    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically decreasing.

        Returns
        -------
        bool

        Examples
        --------
        >>> s = pd.Series([3, 2, 2, 1])
        >>> s.is_monotonic_decreasing
        True

        >>> s = pd.Series([1, 2, 3])
        >>> s.is_monotonic_decreasing
        False
        """
        from pandas import Index

        return Index(self).is_monotonic_decreasing
