    def extract_groups(self, pattern: str) -> Series:
        r"""
        Extract all capture groups for the given regex pattern.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Notes
        -----
        All group names are **strings**.

        If your pattern contains unnamed groups, their numerical position is converted
        to a string.

        For example, we can access the first group via the string `"1"`::

            >>> (
            ...     pl.Series(["foo bar baz"])
            ...     .str.extract_groups(r"(\w+) (.+) (\w+)")
            ...     .struct["1"]
            ... )
            shape: (1,)
            Series: '1' [str]
            [
                "foo"
            ]

        Returns
        -------
        Series
            Series of data type :class:`Struct` with fields of data type :class:`Utf8`.

        Examples
        --------
        >>> s = pl.Series(
        ...     name="url",
        ...     values=[
        ...         "http://vote.com/ballon_dor?candidate=messi&ref=python",
        ...         "http://vote.com/ballon_dor?candidate=weghorst&ref=polars",
        ...         "http://vote.com/ballon_dor?error=404&ref=rust",
        ...     ],
        ... )
        >>> s.str.extract_groups(r"candidate=(?<candidate>\w+)&ref=(?<ref>\w+)")
        shape: (3,)
        Series: 'url' [struct[2]]
        [
            {"messi","python"}
            {"weghorst","polars"}
            {null,null}
        ]

        """
