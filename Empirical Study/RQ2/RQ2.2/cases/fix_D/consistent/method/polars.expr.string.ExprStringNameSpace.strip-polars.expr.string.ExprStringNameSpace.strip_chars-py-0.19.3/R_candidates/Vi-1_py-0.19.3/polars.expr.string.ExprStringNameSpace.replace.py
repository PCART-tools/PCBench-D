    def replace(
        self,
        pattern: str | Expr,
        value: str | Expr,
        *,
        literal: bool = False,
        n: int = 1,
    ) -> Expr:
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
        use the inline ``(?iLmsuxU)`` syntax. For example:

        >>> df = pl.DataFrame(
        ...     {
        ...         "city": "Philadelphia",
        ...         "season": ["Spring", "Summer", "Autumn", "Winter"],
        ...         "weather": ["Rainy", "Sunny", "Cloudy", "Snowy"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     # apply case-insensitive string replacement
        ...     pl.col("weather").str.replace(r"(?i)foggy|rainy|cloudy|snowy", "Sunny")
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

        See the regex crate's section on `grouping and flags
        <https://docs.rs/regex/latest/regex/#grouping-and-flags>`_ for
        additional information about the use of inline expression modifiers.

        See Also
        --------
        replace_all : Replace all matching regex/literal substrings.

        Examples
        --------
        >>> df = pl.DataFrame({"id": [1, 2], "text": ["123abc", "abc456"]})
        >>> df.with_columns(
        ...     pl.col("text").str.replace(r"abc\b", "ABC")
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌─────┬────────┐
        │ id  ┆ text   │
        │ --- ┆ ---    │
        │ i64 ┆ str    │
        ╞═════╪════════╡
        │ 1   ┆ 123ABC │
        │ 2   ┆ abc456 │
        └─────┴────────┘

        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        value = parse_as_expression(value, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_replace_n(pattern, value, literal, n))
