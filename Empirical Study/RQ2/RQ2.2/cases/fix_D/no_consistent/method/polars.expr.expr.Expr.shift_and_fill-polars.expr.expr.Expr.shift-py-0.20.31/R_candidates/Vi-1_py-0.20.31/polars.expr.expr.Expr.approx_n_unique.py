    def approx_n_unique(self) -> Self:
        """
        Approximate count of unique values.

        This is done using the HyperLogLog++ algorithm for cardinality estimation.

        Examples
        --------
        >>> df = pl.DataFrame({"n": [1, 1, 2]})
        >>> df.select(pl.col("n").approx_n_unique())
        shape: (1, 1)
        ┌─────┐
        │ n   │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 2   │
        └─────┘
        >>> df = pl.DataFrame({"n": range(1000)})
        >>> df.select(
        ...     exact=pl.col("n").n_unique(),
        ...     approx=pl.col("n").approx_n_unique(),
        ... )  # doctest: +SKIP
        shape: (1, 2)
        ┌───────┬────────┐
        │ exact ┆ approx │
        │ ---   ┆ ---    │
        │ u32   ┆ u32    │
        ╞═══════╪════════╡
        │ 1000  ┆ 1005   │
        └───────┴────────┘
        """
        return self._from_pyexpr(self._pyexpr.approx_n_unique())
