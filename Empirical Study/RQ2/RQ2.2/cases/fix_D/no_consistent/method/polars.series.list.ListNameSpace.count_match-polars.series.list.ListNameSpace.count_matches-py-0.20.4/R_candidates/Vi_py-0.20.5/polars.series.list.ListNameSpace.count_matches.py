    def count_matches(self, element: IntoExpr) -> Series:
        """
        Count how often the value produced by `element` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        Examples
        --------
        >>> s = pl.Series("a", [[0], [1], [1, 2, 3, 2], [1, 2, 1], [4, 4]])
        >>> s.list.count_matches(1)
        shape: (5,)
        Series: 'a' [u32]
        [
            0
            1
            1
            2
            0
        ]
        """
