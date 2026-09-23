    def count_matches(self, element: IntoExpr) -> Series:
        """
        Count how often the value produced by `element` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3], [2, 2, 2]], dtype=pl.Array(pl.Int64, 3))
        >>> s.arr.count_matches(2)
        shape: (2,)
        Series: 'a' [u32]
        [
            1
            3
        ]

        """
