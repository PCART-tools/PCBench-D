    def find(
        self, pattern: str | Expr, *, literal: bool = False, strict: bool = True
    ) -> Expr:
        """
        Return the index of the first substring in Series strings matching a pattern.

        If the pattern is not found, returns None.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        literal
            Treat `pattern` as a literal string, not as a regular expression.
        strict
            Raise an error if the underlying pattern is not a valid regex,
            otherwise mask out with a null value.

        Notes
        -----
        To modify regular expression behaviour (such as case-sensitivity) with
        flags, use the inline `(?iLmsuxU)` syntax. For example:

        >>> s = pl.Series("s", ["AAA", "aAa", "aaa"])

        Default (case-sensitive) match:

        >>> s.str.find("Aa").to_list()
        [None, 1, None]

        Case-insensitive match, using an inline flag:

        >>> s.str.find("(?i)Aa").to_list()
        [0, 0, 0]

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        See Also
        --------
        contains : Check if string contains a substring that matches a regex.

        Examples
        --------
        >>> s = pl.Series("txt", ["Crab", "Lobster", None, "Crustaceon"])

        Find the index of the first substring matching a regex pattern:

        >>> s.str.find("a|e").rename("idx_rx")
        shape: (4,)
        Series: 'idx_rx' [u32]
        [
            2
            5
            null
            5
        ]

        Find the index of the first substring matching a literal pattern:

        >>> s.str.find("e", literal=True).rename("idx_lit")
        shape: (4,)
        Series: 'idx_lit' [u32]
        [
            null
            5
            null
            7
        ]

        Match against a pattern found in another column or (expression):

        >>> p = pl.Series("pat", ["a[bc]", "b.t", "[aeiuo]", "(?i)A[BC]"])
        >>> s.str.find(p).rename("idx")
        shape: (4,)
        Series: 'idx' [u32]
        [
            2
            2
            null
            5
        ]
        """
