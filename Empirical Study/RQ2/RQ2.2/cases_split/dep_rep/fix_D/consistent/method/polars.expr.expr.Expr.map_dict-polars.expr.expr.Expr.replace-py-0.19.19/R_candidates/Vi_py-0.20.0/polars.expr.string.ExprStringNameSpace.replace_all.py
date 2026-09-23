    def replace_all(
        self, pattern: str | Expr, value: str | Expr, *, literal: bool = False
    ) -> Expr:
        """
        Replace all matching regex/literal substrings with a new string value.

        Parameters
        ----------
        pattern
            A valid regular expression pattern, compatible with the `regex crate
            <https://docs.rs/regex/latest/regex/>`_.
        value
            Replacement string.
        literal
            Treat pattern as a literal string.

        See Also
        --------
        replace : Replace first matching regex/literal substring.

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

        """
        pattern = parse_as_expression(pattern, str_as_lit=True)
        value = parse_as_expression(value, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_replace_all(pattern, value, literal))
