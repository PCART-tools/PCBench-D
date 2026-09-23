    def agg(self, aggs: pli.Expr | Sequence[pli.Expr]) -> pli.DataFrame:
        """
        Use multiple aggregations on columns.

        This can be combined with complete lazy API and is considered idiomatic polars.

        Parameters
        ----------
        aggs
            Single / multiple aggregation expression(s).

        Returns
        -------
        Result of groupby split apply operations.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"foo": ["one", "two", "two", "one", "two"], "bar": [5, 3, 2, 4, 1]}
        ... )
        >>> df.groupby("foo", maintain_order=True).agg(
        ...     [
        ...         pl.sum("bar").suffix("_sum"),
        ...         pl.col("bar").sort().tail(2).sum().suffix("_tail_sum"),
        ...     ]
        ... )
        shape: (2, 3)
        ┌─────┬─────────┬──────────────┐
        │ foo ┆ bar_sum ┆ bar_tail_sum │
        │ --- ┆ ---     ┆ ---          │
        │ str ┆ i64     ┆ i64          │
        ╞═════╪═════════╪══════════════╡
        │ one ┆ 9       ┆ 9            │
        │ two ┆ 6       ┆ 5            │
        └─────┴─────────┴──────────────┘

        """
        df = (
            pli.wrap_df(self._df)
            .lazy()
            .groupby(self.by, maintain_order=self.maintain_order)
            .agg(aggs)
            .collect(no_optimization=True)
        )
        return self._dataframe_class._from_pydf(df._df)
