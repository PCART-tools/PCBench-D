    def max(self) -> Expr:
        """
        Compute the max value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.with_columns(max=pl.col("values").list.max())
        shape: (2, 2)
        ┌───────────┬─────┐
        │ values    ┆ max │
        │ ---       ┆ --- │
        │ list[i64] ┆ i64 │
        ╞═══════════╪═════╡
        │ [1]       ┆ 1   │
        │ [2, 3]    ┆ 3   │
        └───────────┴─────┘
        """
        return wrap_expr(self._pyexpr.list_max())
