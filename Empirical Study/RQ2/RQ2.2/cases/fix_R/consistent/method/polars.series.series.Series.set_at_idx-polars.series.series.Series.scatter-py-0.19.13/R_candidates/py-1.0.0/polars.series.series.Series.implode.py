    def implode(self) -> Self:
        """
        Aggregate values into a list.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.implode()
        shape: (1,)
        Series: 'a' [list[i64]]
        [
            [1, 2, 3]
        ]
        """
