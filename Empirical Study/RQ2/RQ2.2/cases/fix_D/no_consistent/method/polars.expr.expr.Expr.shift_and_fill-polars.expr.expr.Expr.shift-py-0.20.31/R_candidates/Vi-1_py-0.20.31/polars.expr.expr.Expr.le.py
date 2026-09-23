    def le(self, other: Any) -> Self:
        """
        Method equivalent of "less than or equal" operator `expr <= other`.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [5.0, 4.0, float("nan"), 0.5],
        ...         "y": [5.0, 3.5, float("nan"), 2.0],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("x").le(pl.col("y")).alias("x <= y"),
        ... )
        shape: (4, 3)
        ┌─────┬─────┬────────┐
        │ x   ┆ y   ┆ x <= y │
        │ --- ┆ --- ┆ ---    │
        │ f64 ┆ f64 ┆ bool   │
        ╞═════╪═════╪════════╡
        │ 5.0 ┆ 5.0 ┆ true   │
        │ 4.0 ┆ 3.5 ┆ false  │
        │ NaN ┆ NaN ┆ true   │
        │ 0.5 ┆ 2.0 ┆ true   │
        └─────┴─────┴────────┘
        """
        return self.__le__(other)
