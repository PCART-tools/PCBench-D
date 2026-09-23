    def replace(
        self, pattern: str, value: str, *, literal: bool = False, n: int = 1
    ) -> Series:
        r"""
        Replace first matching regex/literal substring with a new string value.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        value
            String that will replace the matched substring.
        literal
            Treat pattern as a literal string.
        n
            Number of matches to replace.

        Notes
        -----
        To modify regular expression behaviour (such as case-sensitivity) with flags,
        use the inline `(?iLmsuxU)` syntax. For example:

        >>> s = pl.Series(
        ...     name="weather",
        ...     values=[
        ...         "Foggy",
        ...         "Rainy",
        ...         "Sunny",
        ...     ],
        ... )
        >>> # apply case-insensitive string replacement
        >>> s.str.replace(r"(?i)foggy|rainy", "Sunny")
        shape: (3,)
        Series: 'weather' [str]
        [
            "Sunny"
            "Sunny"
            "Sunny"
        ]

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        See Also
        --------
        replace_all : Replace all matching regex/literal substrings.

        Examples
        --------
        >>> s = pl.Series(["123abc", "abc456"])
        >>> s.str.replace(r"abc\b", "ABC")  # doctest: +IGNORE_RESULT
        shape: (2,)
        Series: '' [str]
        [
            "123ABC"
            "abc456"
        ]

        """
