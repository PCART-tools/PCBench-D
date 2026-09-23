    def cbrt(self) -> Series:
        """
        Compute the cube root of the elements.

        Optimization for

        >>> pl.Series([1, 2]) ** (1.0 / 3)
        shape: (2,)
        Series: '' [f64]
        [
            1.0
            1.259921
        ]

        Examples
        --------
        >>> s = pl.Series([1, 2, 3])
        >>> s.cbrt()
        shape: (3,)
        Series: '' [f64]
        [
            1.0
            1.259921
            1.44225
        ]

        """
