    def min(self) -> Expr:
        """
        Compute the min value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.with_columns(min=pl.col("values").list.min())
        shape: (2, 2)
        ┌───────────┬─────┐
        │ values    ┆ min │
        │ ---       ┆ --- │
        │ list[i64] ┆ i64 │
        ╞═══════════╪═════╡
        │ [1]       ┆ 1   │
        │ [2, 3]    ┆ 2   │
        └───────────┴─────┘

        """
        return wrap_expr(self._pyexpr.list_min())
