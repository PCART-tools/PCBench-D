    def contains(
        self, pattern: str | Expr, *, literal: bool = False, strict: bool = True
    ) -> Series:
        """
        Check if strings in Series contain a substring that matches a regex.

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

        Default (case-sensitive) match:

        >>> s = pl.Series("s", ["AAA", "aAa", "aaa"])
        >>> s.str.contains("AA").to_list()
        [True, False, False]

        Case-insensitive match, using an inline flag:

        >>> s = pl.Series("s", ["AAA", "aAa", "aaa"])
        >>> s.str.contains("(?i)AA").to_list()
        [True, True, True]

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        Examples
        --------
        >>> s = pl.Series(["Crab", "cat and dog", "rab$bit", None])
        >>> s.str.contains("cat|bit")
        shape: (4,)
        Series: '' [bool]
        [
            false
            true
            true
            null
        ]
        >>> s.str.contains("rab$", literal=True)
        shape: (4,)
        Series: '' [bool]
        [
            false
            false
            true
            null
        ]

        """
