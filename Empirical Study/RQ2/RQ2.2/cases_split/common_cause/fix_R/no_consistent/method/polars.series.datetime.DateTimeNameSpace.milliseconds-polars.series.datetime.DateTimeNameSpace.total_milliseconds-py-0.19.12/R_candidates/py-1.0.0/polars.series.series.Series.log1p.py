    def log1p(self) -> Series:
        """
        Compute the natural logarithm of the input array plus one, element-wise.

        Examples
        --------
        >>> s = pl.Series([1, 2, 3])
        >>> s.log1p()
        shape: (3,)
        Series: '' [f64]
        [
            0.693147
            1.098612
            1.386294
        ]
        """
