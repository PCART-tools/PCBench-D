    def std(self, ddof: int = 1) -> Series:
        """
        Compute the std value of the arrays in the list.

        Examples
        --------
        >>> s = pl.Series("values", [[-1, 0, 1], [1, 10]])
        >>> s.list.std()
        shape: (2,)
        Series: 'values' [f64]
        [
                1.0
                6.363961
        ]
        """
