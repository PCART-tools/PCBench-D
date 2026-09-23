    def count_match(self, pattern: str | Series) -> Series:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_. Can also be a :class:`Series` of
            regular expressions.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`. Returns null if the original
            value is null.

        Examples
        --------
        >>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t", "bar", None])
        >>> # count digits
        >>> s.str.count_match(r"\d")
        shape: (4,)
        Series: 'foo' [u32]
        [
            5
            6
            0
            null
        ]

        """
