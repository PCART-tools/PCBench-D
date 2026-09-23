    def join(self, separator: IntoExprColumn) -> Series:
        """
        Join all string items in a sub-array and place a separator between them.

        This errors if inner type of array `!= String`.

        Parameters
        ----------
        separator
            string to separate the items with

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        >>> s = pl.Series([["x", "y"], ["a", "b"]], dtype=pl.Array(pl.String, 2))
        >>> s.arr.join(separator="-")
        shape: (2,)
        Series: '' [str]
        [
            "x-y"
            "a-b"
        ]

        """
