    def first(self) -> Series:
        """
        Get the first value of the sub-arrays.

        Examples
        --------
        >>> s = pl.Series(
        ...     "a", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=pl.Array(pl.Int32, 3)
        ... )
        >>> s.arr.first()
        shape: (3,)
        Series: 'a' [i32]
        [
            1
            4
            7
        ]

        """
