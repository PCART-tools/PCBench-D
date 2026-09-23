    def diff(self, n: int = 1, null_behavior: NullBehavior = "ignore") -> Expr:
        """
        Calculate the n-th discrete difference of every sublist.

        Parameters
        ----------
        n
            Number of slots to shift.
        null_behavior : {'ignore', 'drop'}
            How to handle null values.

        Examples
        --------
        >>> df = pl.DataFrame({"n": [[1, 2, 3, 4], [10, 2, 1]]})
        >>> df.select(pl.col("n").list.diff())
        shape: (2, 1)
        ┌────────────────┐
        │ n              │
        │ ---            │
        │ list[i64]      │
        ╞════════════════╡
        │ [null, 1, … 1] │
        │ [null, -8, -1] │
        └────────────────┘

        >>> df.select(pl.col("n").list.diff(n=2))
        shape: (2, 1)
        ┌───────────────────┐
        │ n                 │
        │ ---               │
        │ list[i64]         │
        ╞═══════════════════╡
        │ [null, null, … 2] │
        │ [null, null, -9]  │
        └───────────────────┘

        >>> df.select(pl.col("n").list.diff(n=2, null_behavior="drop"))
        shape: (2, 1)
        ┌───────────┐
        │ n         │
        │ ---       │
        │ list[i64] │
        ╞═══════════╡
        │ [2, 2]    │
        │ [-9]      │
        └───────────┘

        """
        return wrap_expr(self._pyexpr.list_diff(n, null_behavior))
