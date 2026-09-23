    @deprecate_function(
        "Use `select(pl.all().approx_n_unique())` instead.", version="0.20.11"
    )
    def approx_n_unique(self) -> DataFrame:
        """
        Approximate count of unique values.

        .. deprecated:: 0.20.11
            Use `select(pl.all().approx_n_unique())` instead.

        This is done using the HyperLogLog++ algorithm for cardinality estimation.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [1, 2, 1, 1],
        ...     }
        ... )
        >>> df.approx_n_unique()  # doctest: +SKIP
        shape: (1, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ u32 ┆ u32 │
        ╞═════╪═════╡
        │ 4   ┆ 2   │
        └─────┴─────┘
        """
        return self.lazy().approx_n_unique().collect(_eager=True)
