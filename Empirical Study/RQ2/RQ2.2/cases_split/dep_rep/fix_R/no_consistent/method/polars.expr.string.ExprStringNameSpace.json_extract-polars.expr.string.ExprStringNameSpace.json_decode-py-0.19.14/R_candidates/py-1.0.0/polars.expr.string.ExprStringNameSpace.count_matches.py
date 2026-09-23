    def count_matches(self, pattern: str | Expr, *, literal: bool = False) -> Expr:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        literal
            Treat `pattern` as a literal string, not as a regular expression.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`. Returns null if the
            original value is null.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t", "bar", None]})
        >>> df.with_columns(
        ...     pl.col("foo").str.count_matches(r"\d").alias("count_digits"),
        ... )
        shape: (4, 2)
        ┌────────────────┬──────────────┐
        │ foo            ┆ count_digits │
        │ ---            ┆ ---          │
        │ str            ┆ u32          │
        ╞════════════════╪══════════════╡
        │ 123 bla 45 asd ┆ 5            │
        │ xyz 678 910t   ┆ 6            │
        │ bar            ┆ 0            │
        │ null           ┆ null         │
        └────────────────┴──────────────┘

        >>> df = pl.DataFrame({"bar": ["12 dbc 3xy", "cat\\w", "1zy3\\d\\d", None]})
        >>> df.with_columns(
        ...     pl.col("bar")
        ...     .str.count_matches(r"\d", literal=True)
        ...     .alias("count_digits"),
        ... )
        shape: (4, 2)
        ┌────────────┬──────────────┐
        │ bar        ┆ count_digits │
        │ ---        ┆ ---          │
        │ str        ┆ u32          │
        ╞════════════╪══════════════╡
        │ 12 dbc 3xy ┆ 0            │
        │ cat\w      ┆ 0            │
        │ 1zy3\d\d   ┆ 2            │
        │ null       ┆ null         │
        └────────────┴──────────────┘
        """
        pattern = parse_into_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_count_matches(pattern, literal))
