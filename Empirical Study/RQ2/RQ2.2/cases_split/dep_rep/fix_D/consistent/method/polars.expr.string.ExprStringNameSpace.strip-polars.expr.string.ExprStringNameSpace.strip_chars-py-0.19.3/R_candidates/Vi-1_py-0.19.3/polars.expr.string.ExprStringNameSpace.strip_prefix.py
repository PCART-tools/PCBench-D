    def strip_prefix(self, prefix: str) -> Expr:
        """
        Remove prefix.

        The prefix will be removed from the string exactly once, if found.

        Parameters
        ----------
        prefix
            The prefix to be removed.

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
        return wrap_expr(self._pyexpr.str_strip_prefix(prefix))
