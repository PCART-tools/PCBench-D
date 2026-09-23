    def sum(self) -> Expr:
        """
        Sum all the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.with_columns(sum=pl.col("values").list.sum())
        shape: (2, 2)
        ┌───────────┬─────┐
        │ values    ┆ sum │
        │ ---       ┆ --- │
        │ list[i64] ┆ i64 │
        ╞═══════════╪═════╡
        │ [1]       ┆ 1   │
        │ [2, 3]    ┆ 5   │
        └───────────┴─────┘

        """
        return wrap_expr(self._pyexpr.list_sum())
