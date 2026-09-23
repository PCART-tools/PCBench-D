    def var(self, ddof: int = 1) -> Series:
        """
        Compute the var value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[-1, 0, 1], [1, 10]])
        >>> s.list.var()
        shape: (2,)
        Series: 'values' [f64]
        [
                1.0
                40.5
        ]
        """
