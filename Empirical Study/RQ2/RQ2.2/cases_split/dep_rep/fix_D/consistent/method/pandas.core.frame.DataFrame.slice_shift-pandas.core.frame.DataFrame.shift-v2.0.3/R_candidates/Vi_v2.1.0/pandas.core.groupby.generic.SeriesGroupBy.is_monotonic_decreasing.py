    @property
    def is_monotonic_decreasing(self) -> Series:
        """
        Return whether each group's values are monotonically decreasing.

        Returns
        -------
        Series

        Examples
        --------
        >>> s = pd.Series([2, 1, 3, 4], index=['Falcon', 'Falcon', 'Parrot', 'Parrot'])
        >>> s.groupby(level=0).is_monotonic_decreasing
        Falcon     True
        Parrot    False
        dtype: bool
        """
        return self.apply(lambda ser: ser.is_monotonic_decreasing)
