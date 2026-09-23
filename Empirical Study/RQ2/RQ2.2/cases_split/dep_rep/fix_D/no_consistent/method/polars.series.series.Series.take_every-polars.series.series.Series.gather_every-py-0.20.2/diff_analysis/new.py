    def gather_every(self, n: int, offset: int = 0) -> Series:
        """
        Take every nth value in the Series and return as new Series.

        Parameters
        ----------
        n
            Gather every *n*-th row.
        offset
            Start the row count at this offset.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4])
        >>> s.gather_every(2)
        shape: (2,)
        Series: 'a' [i64]
        [
            1
            3
        ]
        >>> s.gather_every(2, offset=1)
        shape: (2,)
        Series: 'a' [i64]
        [
            2
            4
        ]

        """
