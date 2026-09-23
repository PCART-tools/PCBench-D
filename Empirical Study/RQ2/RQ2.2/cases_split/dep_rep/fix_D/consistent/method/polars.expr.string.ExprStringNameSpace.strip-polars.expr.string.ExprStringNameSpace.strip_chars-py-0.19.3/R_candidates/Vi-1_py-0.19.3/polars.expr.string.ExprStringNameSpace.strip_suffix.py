    def strip_suffix(self, suffix: str) -> Expr:
        """
        Remove suffix.

        The suffix will be removed from the string exactly once, if found.

        Parameters
        ----------
        suffix
            The suffix to be removed.

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
        return wrap_expr(self._pyexpr.str_strip_suffix(suffix))
