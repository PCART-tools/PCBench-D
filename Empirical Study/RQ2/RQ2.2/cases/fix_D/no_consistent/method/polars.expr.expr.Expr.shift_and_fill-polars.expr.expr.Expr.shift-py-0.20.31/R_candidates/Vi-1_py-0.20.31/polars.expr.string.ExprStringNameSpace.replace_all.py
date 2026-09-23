    def replace_all(
        self, pattern: str | Expr, value: str | Expr, *, literal: bool = False
    ) -> Expr:
        r"""
        Replace all matching regex/literal substrings with a new string value.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        value
            String that will replace the matched substring.
        literal
            Treat `pattern` as a literal string.

        See Also
        --------
        replace

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
        >>> df = pl.DataFrame({"id": [1, 2], "text": ["abcabc", "123a123"]})
        >>> df.with_columns(pl.col("text").str.replace_all("a", "-"))
        shape: (2, 2)
        ┌─────┬─────────┐
        │ id  ┆ text    │
        │ --- ┆ ---     │
        │ i64 ┆ str     │
        ╞═════╪═════════╡
        │ 1   ┆ -bc-bc  │
        │ 2   ┆ 123-123 │
        └─────┴─────────┘

        Capture groups are supported. Use `${1}` in the `value` string to refer to the
        first capture group in the `pattern`, `${2}` to refer to the second capture
        group, and so on. You can also use named capture groups.

        >>> df = pl.DataFrame({"word": ["hat", "hut"]})
        >>> df.with_columns(
        ...     positional=pl.col.word.str.replace_all("h(.)t", "b${1}d"),
        ...     named=pl.col.word.str.replace_all("h(?<vowel>.)t", "b${vowel}d"),
        ... )
        shape: (2, 3)
        ┌──────┬────────────┬───────┐
        │ word ┆ positional ┆ named │
        │ ---  ┆ ---        ┆ ---   │
        │ str  ┆ str        ┆ str   │
        ╞══════╪════════════╪═══════╡
        │ hat  ┆ bad        ┆ bad   │
        │ hut  ┆ bud        ┆ bud   │
        └──────┴────────────┴───────┘

        Apply case-insensitive string replacement using the `(?i)` flag.

        >>> df = pl.DataFrame(
        ...     {
        ...         "city": "Philadelphia",
        ...         "season": ["Spring", "Summer", "Autumn", "Winter"],
        ...         "weather": ["Rainy", "Sunny", "Cloudy", "Snowy"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     # apply case-insensitive string replacement
        ...     pl.col("weather").str.replace_all(
        ...         r"(?i)foggy|rainy|cloudy|snowy", "Sunny"
        ...     )
        ... )
        shape: (4, 3)
        ┌──────────────┬────────┬─────────┐
        │ city         ┆ season ┆ weather │
        │ ---          ┆ ---    ┆ ---     │
        │ str          ┆ str    ┆ str     │
        ╞══════════════╪════════╪═════════╡
        │ Philadelphia ┆ Spring ┆ Sunny   │
        │ Philadelphia ┆ Summer ┆ Sunny   │
        │ Philadelphia ┆ Autumn ┆ Sunny   │
        │ Philadelphia ┆ Winter ┆ Sunny   │
        └──────────────┴────────┴─────────┘
        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        value = parse_as_expression(value, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_replace_all(pattern, value, literal))
