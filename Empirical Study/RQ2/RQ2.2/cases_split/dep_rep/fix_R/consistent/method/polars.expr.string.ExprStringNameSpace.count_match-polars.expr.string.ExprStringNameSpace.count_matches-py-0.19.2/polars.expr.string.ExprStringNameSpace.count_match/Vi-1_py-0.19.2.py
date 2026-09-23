    def count_match(self, pattern: str | Expr) -> Expr:
        r"""
        Count all successive non-overlapping regex matches.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`. Returns null if the
            original value is null.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t", "bar", None]})
        >>> df.select(
        ...     pl.col("foo").str.count_match(r"\d").alias("count_digits"),
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

        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_count_match(pattern))
