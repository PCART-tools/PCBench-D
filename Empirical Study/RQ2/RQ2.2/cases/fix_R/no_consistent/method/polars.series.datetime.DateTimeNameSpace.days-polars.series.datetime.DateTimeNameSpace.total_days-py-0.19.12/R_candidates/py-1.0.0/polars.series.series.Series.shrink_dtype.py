    def shrink_dtype(self) -> Series:
        """
        Shrink numeric columns to the minimal required datatype.

        Shrink to the dtype needed to fit the extrema of this [`Series`].
        This can be used to reduce memory pressure.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4, 5, 6])
        >>> s
        shape: (6,)
        Series: 'a' [i64]
        [
                1
                2
                3
                4
                5
                6
        ]
        >>> s.shrink_dtype()
        shape: (6,)
        Series: 'a' [i8]
        [
                1
                2
                3
                4
                5
                6
        ]
        """
