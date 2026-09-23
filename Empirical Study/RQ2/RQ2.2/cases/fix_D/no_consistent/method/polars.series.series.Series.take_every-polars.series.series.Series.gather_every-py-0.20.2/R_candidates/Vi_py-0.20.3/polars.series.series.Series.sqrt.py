    def sqrt(self) -> Series:
        """
        Compute the square root of the elements.

        Syntactic sugar for

        >>> pl.Series([1, 2]) ** 0.5
        shape: (2,)
        Series: '' [f64]
        [
            1.0
            1.414214
        ]

        Examples
        --------
        >>> s = pl.Series([1, 2, 3])
        >>> s.sqrt()
        shape: (3,)
        Series: '' [f64]
        [
            1.0
            1.414214
            1.732051
        ]

        """
