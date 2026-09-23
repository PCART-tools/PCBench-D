    def diff(self, n: int = 1, null_behavior: NullBehavior = "ignore") -> Expr:
        """
        Calculate the first discrete difference between shifted items of every sublist.

        Parameters
        ----------
        n
            Number of slots to shift.
        null_behavior : {'ignore', 'drop'}
            How to handle null values.

        Examples
        --------
        >>> df = pl.DataFrame({"n": [[1, 2, 3, 4], [10, 2, 1]]})
        >>> df.with_columns(diff=pl.col("n").list.diff())
        shape: (2, 2)
        ┌─────────────┬────────────────┐
        │ n           ┆ diff           │
        │ ---         ┆ ---            │
        │ list[i64]   ┆ list[i64]      │
        ╞═════════════╪════════════════╡
        │ [1, 2, … 4] ┆ [null, 1, … 1] │
        │ [10, 2, 1]  ┆ [null, -8, -1] │
        └─────────────┴────────────────┘

        >>> df.with_columns(diff=pl.col("n").list.diff(n=2))
        shape: (2, 2)
        ┌─────────────┬───────────────────┐
        │ n           ┆ diff              │
        │ ---         ┆ ---               │
        │ list[i64]   ┆ list[i64]         │
        ╞═════════════╪═══════════════════╡
        │ [1, 2, … 4] ┆ [null, null, … 2] │
        │ [10, 2, 1]  ┆ [null, null, -9]  │
        └─────────────┴───────────────────┘

        >>> df.with_columns(diff=pl.col("n").list.diff(n=2, null_behavior="drop"))
        shape: (2, 2)
        ┌─────────────┬───────────┐
        │ n           ┆ diff      │
        │ ---         ┆ ---       │
        │ list[i64]   ┆ list[i64] │
        ╞═════════════╪═══════════╡
        │ [1, 2, … 4] ┆ [2, 2]    │
        │ [10, 2, 1]  ┆ [-9]      │
        └─────────────┴───────────┘
        """
        return wrap_expr(self._pyexpr.list_diff(n, null_behavior))
