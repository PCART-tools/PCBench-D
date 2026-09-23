    def mean(self) -> Expr:
        """
        Compute the mean value of the lists in the array.

        Examples
        --------
        >>> df = pl.DataFrame({"values": [[1], [2, 3]]})
        >>> df.with_columns(mean=pl.col("values").list.mean())
        shape: (2, 2)
        ┌───────────┬──────┐
        │ values    ┆ mean │
        │ ---       ┆ ---  │
        │ list[i64] ┆ f64  │
        ╞═══════════╪══════╡
        │ [1]       ┆ 1.0  │
        │ [2, 3]    ┆ 2.5  │
        └───────────┴──────┘

        """
        return wrap_expr(self._pyexpr.list_mean())
