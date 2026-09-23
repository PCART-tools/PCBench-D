    def concat(self, other: list[Series] | Series | list[Any]) -> Series:
        """
        Concat the arrays in a Series dtype List in linear time.

        Parameters
        ----------
        other
            Columns to concat into a List Series

        Examples
        --------
        >>> s1 = pl.Series("a", [["a", "b"], ["c"]])
        >>> s2 = pl.Series("b", [["c"], ["d", None]])
        >>> s1.list.concat(s2)
        shape: (2,)
        Series: 'a' [list[str]]
        [
            ["a", "b", "c"]
            ["c", "d", null]
        ]
        """
