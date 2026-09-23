    def reverse(self) -> Expr:
        """
        Reverse the arrays in the list.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[3, 2, 1], [9, 1, 2]],
        ...     }
        ... )
        >>> df.with_columns(reverse=pl.col("a").list.reverse())
        shape: (2, 2)
        ┌───────────┬───────────┐
        │ a         ┆ reverse   │
        │ ---       ┆ ---       │
        │ list[i64] ┆ list[i64] │
        ╞═══════════╪═══════════╡
        │ [3, 2, 1] ┆ [1, 2, 3] │
        │ [9, 1, 2] ┆ [2, 1, 9] │
        └───────────┴───────────┘
        """
        return wrap_expr(self._pyexpr.list_reverse())
