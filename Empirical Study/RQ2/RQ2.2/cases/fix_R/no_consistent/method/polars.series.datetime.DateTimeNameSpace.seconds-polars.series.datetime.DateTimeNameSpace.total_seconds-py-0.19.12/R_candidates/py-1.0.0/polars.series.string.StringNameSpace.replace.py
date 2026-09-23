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
            Treat `pattern` as a literal string.
        n
            Number of matches to replace.

        See Also
        --------
        replace_all

        Notes
        -----
        The dollar sign (`$`) is a special character related to capture groups.
        To refer to a literal dollar sign, use `$$` instead or set `literal` to `True`.

        To modify regular expression behaviour (such as case-sensitivity) with flags,
        use the inline `(?iLmsuxU)` syntax. See the regex crate's section on
        `grouping and flags <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_
        for additional information about the use of inline expression modifiers.

        Examples
        --------
        >>> s = pl.Series(["123abc", "abc456"])
        >>> s.str.replace(r"abc\b", "ABC")
        shape: (2,)
        Series: '' [str]
        [
            "123ABC"
            "abc456"
        ]

        Capture groups are supported. Use `${1}` in the `value` string to refer to the
        first capture group in the `pattern`, `${2}` to refer to the second capture
        group, and so on. You can also use named capture groups.

        >>> s = pl.Series(["hat", "hut"])
        >>> s.str.replace("h(.)t", "b${1}d")
        shape: (2,)
        Series: '' [str]
        [
                "bad"
                "bud"
        ]
        >>> s.str.replace("h(?<vowel>.)t", "b${vowel}d")
        shape: (2,)
        Series: '' [str]
        [
                "bad"
                "bud"
        ]

        Apply case-insensitive string replacement using the `(?i)` flag.

        >>> s = pl.Series("weather", ["Foggy", "Rainy", "Sunny"])
        >>> s.str.replace(r"(?i)foggy|rainy", "Sunny")
        shape: (3,)
        Series: 'weather' [str]
        [
            "Sunny"
            "Sunny"
            "Sunny"
        ]
        """
