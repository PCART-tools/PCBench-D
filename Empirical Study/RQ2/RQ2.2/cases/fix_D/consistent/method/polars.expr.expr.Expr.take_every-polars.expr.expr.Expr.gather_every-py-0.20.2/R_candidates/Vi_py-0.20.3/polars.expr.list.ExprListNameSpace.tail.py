    def tail(self, n: int | str | Expr = 5) -> Expr:
        """
        Slice the last `n` values of every sublist.

        Parameters
        ----------
        n
            Number of values to return for each sublist.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [[1, 2, 3, 4], [10, 2, 1]]})
        >>> df.with_columns(tail=pl.col("a").list.tail(2))
        shape: (2, 2)
        ┌─────────────┬───────────┐
        │ a           ┆ tail      │
        │ ---         ┆ ---       │
        │ list[i64]   ┆ list[i64] │
        ╞═════════════╪═══════════╡
        │ [1, 2, … 4] ┆ [3, 4]    │
        │ [10, 2, 1]  ┆ [2, 1]    │
        └─────────────┴───────────┘

        """
        n = parse_as_expression(n)
        return wrap_expr(self._pyexpr.list_tail(n))
