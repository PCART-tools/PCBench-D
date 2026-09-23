    def explode(self) -> Series:
        """
        Returns a column with a separate row for every string character.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        >>> s = pl.Series("a", ["foo", "bar"])
        >>> s.str.explode()
        shape: (6,)
        Series: 'a' [str]
        [
                "f"
                "o"
                "o"
                "b"
                "a"
                "r"
        ]
        """
