    def n_unique(self) -> Expr:
        """
        Count the number of unique values in every sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[1, 1, 2], [2, 3, 4]],
        ...     },
        ...     schema={"a": pl.Array(pl.Int64, 3)},
        ... )
        >>> df.with_columns(n_unique=pl.col("a").arr.n_unique())
        shape: (2, 2)
        ┌───────────────┬──────────┐
        │ a             ┆ n_unique │
        │ ---           ┆ ---      │
        │ array[i64, 3] ┆ u32      │
        ╞═══════════════╪══════════╡
        │ [1, 1, 2]     ┆ 2        │
        │ [2, 3, 4]     ┆ 3        │
        └───────────────┴──────────┘
        """
        return wrap_expr(self._pyexpr.arr_n_unique())
