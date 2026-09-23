    @deprecate_function(
        "Use `select(pl.all().approx_n_unique())` instead.", version="0.20.11"
    )
    def approx_n_unique(self) -> LazyFrame:
        """
        Approximate count of unique values.

        .. deprecated:: 0.20.11
            Use `select(pl.all().approx_n_unique())` instead.

        This is done using the HyperLogLog++ algorithm for cardinality estimation.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [1, 2, 1, 1],
        ...     }
        ... )
        >>> lf.approx_n_unique().collect()  # doctest: +SKIP
        shape: (1, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ u32 ┆ u32 │
        ╞═════╪═════╡
        │ 4   ┆ 2   │
        └─────┴─────┘
        """
        return self.select(F.all().approx_n_unique())
