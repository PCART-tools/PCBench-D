    def count_matches(self, pattern: str | Expr, *, literal: bool = False) -> Expr:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        literal
            Treat ``pattern`` as a literal string, not as a regular expression.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`. Returns null if the
            original value is null.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t", "bar", None]})
        >>> df.select(
        ...     pl.col("foo").str.count_matches(r"\d").alias("count_digits"),
        ... )
        shape: (4, 1)
        ┌──────────────┐
        │ count_digits │
        │ ---          │
        │ u32          │
        ╞══════════════╡
        │ 5            │
        │ 6            │
        │ 0            │
        │ null         │
        └──────────────┘

        >>> df = pl.DataFrame({"bar": ["12 dbc 3xy", "cat\\w", "1zy3\\d\\d", None]})
        >>> df.select(
        ...     pl.col("bar")
        ...     .str.count_matches(r"\d", literal=True)
        ...     .alias("count_digits"),
        ... )
        shape: (4, 1)
        ┌──────────────┐
        │ count_digits │
        │ ---          │
        │ u32          │
        ╞══════════════╡
        │ 0            │
        │ 0            │
        │ 2            │
        │ null         │
        └──────────────┘

        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_count_matches(pattern, literal))
