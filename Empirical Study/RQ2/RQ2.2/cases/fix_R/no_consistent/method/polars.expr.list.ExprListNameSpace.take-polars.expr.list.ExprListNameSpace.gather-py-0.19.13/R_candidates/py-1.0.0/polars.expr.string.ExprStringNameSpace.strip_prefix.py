    def strip_prefix(self, prefix: IntoExpr) -> Expr:
        """
        Remove prefix.

        The prefix will be removed from the string exactly once, if found.

        .. note::
            This method strips the exact character sequence provided in
            `prefix` from the start of the input. To strip a set of characters
            in any order, use :func:`strip_chars_start` instead.

        Parameters
        ----------
        prefix
            The prefix to be removed.

        See Also
        --------
        strip_chars_start
        strip_suffix

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["foobar", "foofoobar", "foo", "bar"]})
        >>> df.with_columns(pl.col("a").str.strip_prefix("foo").alias("stripped"))
        shape: (4, 2)
        ┌───────────┬──────────┐
        │ a         ┆ stripped │
        │ ---       ┆ ---      │
        │ str       ┆ str      │
        ╞═══════════╪══════════╡
        │ foobar    ┆ bar      │
        │ foofoobar ┆ foobar   │
        │ foo       ┆          │
        │ bar       ┆ bar      │
        └───────────┴──────────┘
        """
        prefix = parse_into_expression(prefix, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_strip_prefix(prefix))
