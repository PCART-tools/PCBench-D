    def strip_suffix(self, suffix: IntoExpr) -> Expr:
        """
        Remove suffix.

        The suffix will be removed from the string exactly once, if found.

        .. note::
            This method strips the exact character sequence provided in
            `suffix` from the end of the input. To strip a set of characters
            in any order, use :func:`strip_chars_end` instead.

        Parameters
        ----------
        suffix
            The suffix to be removed.

        See Also
        --------
        strip_chars_end
        strip_prefix

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["foobar", "foobarbar", "foo", "bar"]})
        >>> df.with_columns(pl.col("a").str.strip_suffix("bar").alias("stripped"))
        shape: (4, 2)
        ┌───────────┬──────────┐
        │ a         ┆ stripped │
        │ ---       ┆ ---      │
        │ str       ┆ str      │
        ╞═══════════╪══════════╡
        │ foobar    ┆ foo      │
        │ foobarbar ┆ foobar   │
        │ foo       ┆ foo      │
        │ bar       ┆          │
        └───────────┴──────────┘

        """
        suffix = parse_as_expression(suffix, str_as_lit=True)
        return wrap_expr(self._pyexpr.str_strip_suffix(suffix))
