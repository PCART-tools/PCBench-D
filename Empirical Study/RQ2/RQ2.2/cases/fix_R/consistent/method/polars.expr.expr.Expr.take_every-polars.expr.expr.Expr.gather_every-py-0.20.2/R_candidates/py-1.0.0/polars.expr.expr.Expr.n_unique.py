    def n_unique(self) -> Expr:
        """
        Count unique values.

        Notes
        -----
        `null` is considered to be a unique value for the purposes of this operation.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [1, 1, 2, 2, 3], "y": [1, 1, 1, None, None]})
        >>> df.select(
        ...     x_unique=pl.col("x").n_unique(),
        ...     y_unique=pl.col("y").n_unique(),
        ... )
        shape: (1, 2)
        ┌──────────┬──────────┐
        │ x_unique ┆ y_unique │
        │ ---      ┆ ---      │
        │ u32      ┆ u32      │
        ╞══════════╪══════════╡
        │ 3        ┆ 2        │
        └──────────┴──────────┘
        """
        return self._from_pyexpr(self._pyexpr.n_unique())
