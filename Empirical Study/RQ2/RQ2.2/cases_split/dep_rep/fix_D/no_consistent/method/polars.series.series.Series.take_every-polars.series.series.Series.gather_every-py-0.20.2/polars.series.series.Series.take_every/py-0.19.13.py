    def take_every(self, n: int) -> Series:
        """
        Take every nth value in the Series and return as new Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4])
        >>> s.take_every(2)
        shape: (2,)
        Series: 'a' [i64]
        [
            1
            3
        ]

        """
