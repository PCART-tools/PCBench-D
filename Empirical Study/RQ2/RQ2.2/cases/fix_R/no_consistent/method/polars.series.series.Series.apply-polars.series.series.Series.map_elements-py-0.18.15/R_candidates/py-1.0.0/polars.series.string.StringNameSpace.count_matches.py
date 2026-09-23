    def count_matches(self, pattern: str | Series, *, literal: bool = False) -> Series:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_. Can also be a :class:`Series` of
            regular expressions.
        literal
            Treat `pattern` as a literal string, not as a regular expression.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`. Returns null if the original
            value is null.

        Examples
        --------
        >>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t", "bar", None])
        >>> # count digits
        >>> s.str.count_matches(r"\d")
        shape: (4,)
        Series: 'foo' [u32]
        [
            5
            6
            0
            null
        ]

        >>> s = pl.Series("bar", ["12 dbc 3xy", "cat\\w", "1zy3\\d\\d", None])
        >>> s.str.count_matches(r"\d", literal=True)
        shape: (4,)
        Series: 'bar' [u32]
        [
            0
            0
            2
            null
        ]
        """
