    def median(self) -> Series:
        """
        Compute the median value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[-1, 0, 1], [1, 10]])
        >>> s.list.median()
        shape: (2,)
        Series: 'values' [f64]
        [
                0.0
                5.5
        ]
        """
