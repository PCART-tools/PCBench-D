    def n_unique(self) -> Expr:
        """
        Count the number of unique values in every sub-lists.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 1, 2], [2, 3, 4]],
        ...     }
        ... )
        >>> df.with_columns(n_unique=pl.col("a").list.n_unique())
        shape: (2, 2)
        ┌───────────┬──────────┐
        │ a         ┆ n_unique │
        │ ---       ┆ ---      │
        │ list[i64] ┆ u32      │
        ╞═══════════╪══════════╡
        │ [1, 1, 2] ┆ 2        │
        │ [2, 3, 4] ┆ 3        │
        └───────────┴──────────┘
        """
        return wrap_expr(self._pyexpr.list_n_unique())
