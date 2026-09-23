    def abs(self) -> Series:
        """
        Compute absolute values.

        Same as `abs(series)`.

        Examples
        --------
        >>> s = pl.Series([1, -2, -3])
        >>> s.abs()
        shape: (3,)
        Series: '' [i64]
        [
            1
            2
            3
        ]
        """
