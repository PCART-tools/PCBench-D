    def eq(self, other: Any) -> Self:
        """
        Method equivalent of equality operator ``expr == other``.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [1.0, 2.0, float("nan"), 4.0],
        ...         "y": [2.0, 2.0, float("nan"), 4.0],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("x").eq(pl.col("y")).alias("x == y"),
        ... )
        shape: (4, 3)
        ┌─────┬─────┬────────┐
        │ x   ┆ y   ┆ x == y │
        │ --- ┆ --- ┆ ---    │
        │ f64 ┆ f64 ┆ bool   │
        ╞═════╪═════╪════════╡
        │ 1.0 ┆ 2.0 ┆ false  │
        │ 2.0 ┆ 2.0 ┆ true   │
        │ NaN ┆ NaN ┆ false  │
        │ 4.0 ┆ 4.0 ┆ true   │
        └─────┴─────┴────────┘

        """
        return self.__eq__(other)
