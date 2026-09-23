    def mean(self) -> Series:
        """
        Compute the mean value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[3, 1], [3, 3]])
        >>> s.list.mean()
        shape: (2,)
        Series: 'values' [f64]
        [
            2.0
            3.0
        ]
        """
