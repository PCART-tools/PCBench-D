    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically increasing.

        Returns
        -------
        bool

        Examples
        --------
        >>> s = pd.Series([1, 2, 2])
        >>> s.is_monotonic_increasing
        True

        >>> s = pd.Series([3, 2, 1])
        >>> s.is_monotonic_increasing
        False
        """
        from pandas import Index

        return Index(self).is_monotonic_increasing
