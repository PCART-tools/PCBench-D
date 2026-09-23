    def log10(self) -> Series:
        """
        Compute the base 10 logarithm of the input array, element-wise.

        Examples
        --------
        >>> s = pl.Series([10, 100, 1000])
        >>> s.log10()
        shape: (3,)
        Series: '' [f64]
        [
            1.0
            2.0
            3.0
        ]
        """
