    def explode(self) -> Series:
        """
        Returns a column with a separate row for every list element.

        Returns
        -------
        Series
            Series with the data type of the list elements.

        See Also
        --------
        Series.reshape : Reshape this Series to a flat Series or a Series of Lists.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3], [4, 5, 6]])
        >>> s.list.explode()
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
        """
