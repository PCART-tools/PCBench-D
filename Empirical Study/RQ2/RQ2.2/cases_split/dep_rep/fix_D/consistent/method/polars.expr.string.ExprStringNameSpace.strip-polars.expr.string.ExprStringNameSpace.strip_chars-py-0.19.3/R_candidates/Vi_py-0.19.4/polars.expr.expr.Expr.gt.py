    def gt(self, other: Any) -> Self:
        """
        Method equivalent of "greater than" operator ``expr > other``.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [5.0, 4.0, float("nan"), 2.0],
        ...         "y": [5.0, 3.0, float("nan"), 1.0],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("x").gt(pl.col("y")).alias("x > y"),
        ... )
        shape: (4, 3)
        ┌─────┬─────┬───────┐
        │ x   ┆ y   ┆ x > y │
        │ --- ┆ --- ┆ ---   │
        │ f64 ┆ f64 ┆ bool  │
        ╞═════╪═════╪═══════╡
        │ 5.0 ┆ 5.0 ┆ false │
        │ 4.0 ┆ 3.0 ┆ true  │
        │ NaN ┆ NaN ┆ false │
        │ 2.0 ┆ 1.0 ┆ true  │
        └─────┴─────┴───────┘

        """
        return self.__gt__(other)
