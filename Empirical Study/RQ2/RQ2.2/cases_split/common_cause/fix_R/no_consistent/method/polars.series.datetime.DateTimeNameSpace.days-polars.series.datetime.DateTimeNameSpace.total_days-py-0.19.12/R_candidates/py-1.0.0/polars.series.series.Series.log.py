    def log(self, base: float = math.e) -> Series:
        """
        Compute the logarithm to a given base.

        Examples
        --------
        >>> s = pl.Series([1, 2, 3])
        >>> s.log()
        shape: (3,)
        Series: '' [f64]
        [
            0.0
            0.693147
            1.098612
        ]
        """
