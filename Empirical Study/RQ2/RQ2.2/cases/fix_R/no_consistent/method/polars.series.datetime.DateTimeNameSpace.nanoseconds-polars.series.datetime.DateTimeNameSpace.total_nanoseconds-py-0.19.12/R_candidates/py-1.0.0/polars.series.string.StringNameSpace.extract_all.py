    def extract_all(self, pattern: str | Series) -> Series:
        r'''
        Extract all matches for the given regex pattern.

        Extract each successive non-overlapping regex match in an individual string
        as a list. If the haystack string is `null`, `null` is returned.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Notes
        -----
        To modify regular expression behaviour (such as "verbose" mode and/or
        case-sensitive matching) with flags, use the inline `(?iLmsuxU)` syntax.
        For example:

        >>> s = pl.Series(
        ...     name="email",
        ...     values=[
        ...         "real.email@spam.com",
        ...         "some_account@somewhere.net",
        ...         "abc.def.ghi.jkl@uvw.xyz.co.uk",
        ...     ],
        ... )
        >>> # extract name/domain parts from email, using verbose regex
        >>> s.str.extract_all(
        ...     r"""(?xi)   # activate 'verbose' and 'case-insensitive' flags
        ...       [         # (start character group)
        ...         A-Z     # letters
        ...         0-9     # digits
        ...         ._%+\-  # special chars
        ...       ]         # (end character group)
        ...       +         # 'one or more' quantifier
        ...     """
        ... ).alias("email_parts")
        shape: (3,)
        Series: 'email_parts' [list[str]]
        [
            ["real.email", "spam.com"]
            ["some_account", "somewhere.net"]
            ["abc.def.ghi.jkl", "uvw.xyz.co.uk"]
        ]

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        Returns
        -------
        Series
            Series of data type `List(String)`.

        Examples
        --------
        >>> s = pl.Series("foo", ["123 bla 45 asd", "xyz 678 910t", "bar", None])
        >>> s.str.extract_all(r"\d+")
        shape: (4,)
        Series: 'foo' [list[str]]
        [
            ["123", "45"]
            ["678", "910"]
            []
            null
        ]

        '''
