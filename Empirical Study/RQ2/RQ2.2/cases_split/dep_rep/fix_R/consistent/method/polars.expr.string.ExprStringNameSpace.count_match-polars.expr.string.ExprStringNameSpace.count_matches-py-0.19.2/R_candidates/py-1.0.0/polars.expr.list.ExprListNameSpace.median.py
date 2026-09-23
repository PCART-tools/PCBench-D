    def median(self) -> Expr:
        """
        Compute the median value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[-1, 0, 1], [1, 10]]})
        >>> df.with_columns(pl.col("values").list.median().alias("median"))
        shape: (2, 2)
        ┌────────────┬────────┐
        │ values     ┆ median │
        │ ---        ┆ ---    │
        │ list[i64]  ┆ f64    │
        ╞════════════╪════════╡
        │ [-1, 0, 1] ┆ 0.0    │
        │ [1, 10]    ┆ 5.5    │
        └────────────┴────────┘
        """
        return wrap_expr(self._pyexpr.list_median())
