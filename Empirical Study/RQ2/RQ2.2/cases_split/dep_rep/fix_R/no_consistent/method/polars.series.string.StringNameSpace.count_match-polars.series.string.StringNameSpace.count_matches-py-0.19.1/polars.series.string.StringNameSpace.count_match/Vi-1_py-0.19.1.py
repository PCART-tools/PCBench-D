    def count_match(self, pattern: str) -> Series:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`. Contains null values if the original
            value is null or if the regex captures nothing.

        Examples
        --------
        >>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t"])
        >>> # count digits
        >>> s.str.count_match(r"\d")
        shape: (2,)
        Series: 'foo' [u32]
        [
            5
            6
        ]

        """
