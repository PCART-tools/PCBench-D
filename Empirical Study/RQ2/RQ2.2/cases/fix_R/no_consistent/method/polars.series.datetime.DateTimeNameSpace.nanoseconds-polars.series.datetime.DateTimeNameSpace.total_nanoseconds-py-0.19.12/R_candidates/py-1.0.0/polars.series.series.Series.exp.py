    def exp(self) -> Series:
        """
        Compute the exponential, element-wise.

        Examples
        --------
        >>> s = pl.Series([1, 2, 3])
        >>> s.exp()
        shape: (3,)
        Series: '' [f64]
        [
            2.718282
            7.389056
            20.085537
        ]
        """
