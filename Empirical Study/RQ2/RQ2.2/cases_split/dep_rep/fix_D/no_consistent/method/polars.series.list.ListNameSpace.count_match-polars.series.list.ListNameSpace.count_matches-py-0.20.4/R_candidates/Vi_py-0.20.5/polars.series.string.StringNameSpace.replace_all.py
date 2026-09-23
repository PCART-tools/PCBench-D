    def replace_all(self, pattern: str, value: str, *, literal: bool = False) -> Series:
        """
        Replace all matching regex/literal substrings with a new string value.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        value
            String that will replace the matches.
        literal
            Treat pattern as a literal string.

        See Also
        --------
        replace : Replace first matching regex/literal substring.

        Examples
        --------
        >>> df = pl.Series(["abcabc", "123a123"])
        >>> df.str.replace_all("a", "-")
        shape: (2,)
        Series: '' [str]
        [
            "-bc-bc"
            "123-123"
        ]
        """
