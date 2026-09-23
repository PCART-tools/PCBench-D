    def reverse(self) -> Expr:
        """
        Reverse the arrays in this column.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [[3, 2, 1], [9, 1, 2]],
        ...     },
        ...     schema={"a": pl.Array(pl.Int64, 3)},
        ... )
        >>> df.with_columns(reverse=pl.col("a").arr.reverse())
        shape: (2, 2)
        ┌───────────────┬───────────────┐
        │ a             ┆ reverse       │
        │ ---           ┆ ---           │
        │ array[i64, 3] ┆ array[i64, 3] │
        ╞═══════════════╪═══════════════╡
        │ [3, 2, 1]     ┆ [1, 2, 3]     │
        │ [9, 1, 2]     ┆ [2, 1, 9]     │
        └───────────────┴───────────────┘

        """
        return wrap_expr(self._pyexpr.arr_reverse())
