    def slice(self, offset: int, length: int | None = None) -> Series:
        """
        Create subslices of the string values of a String Series.

        Parameters
        ----------
        offset
            Start index. Negative indexing is supported.
        length
            Length of the slice. If set to `None` (default), the slice is taken to the
            end of the string.

        Returns
        -------
        Series
            Series of data type :class:`Struct` with fields of data type
            :class:`String`.

        Examples
        --------
        >>> s = pl.Series("s", ["pear", None, "papaya", "dragonfruit"])
        >>> s.str.slice(-3)
        shape: (4,)
        Series: 's' [str]
        [
            "ear"
            null
            "aya"
            "uit"
        ]

        Using the optional `length` parameter

        >>> s.str.slice(4, length=3)
        shape: (4,)
        Series: 's' [str]
        [
            ""
            null
            "ya"
            "onf"
        ]
        """
