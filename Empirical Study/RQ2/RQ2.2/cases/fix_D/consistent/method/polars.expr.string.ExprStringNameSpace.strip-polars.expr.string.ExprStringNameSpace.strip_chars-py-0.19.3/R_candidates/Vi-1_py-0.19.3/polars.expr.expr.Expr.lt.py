    def lt(self, other: Any) -> Self:
        """
        Method equivalent of "less than" operator ``expr < other``.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [1.0, 2.0, float("nan"), 3.0],
        ...         "y": [2.0, 2.0, float("nan"), 4.0],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("x").lt(pl.col("y")).alias("x < y"),
        ... )
        shape: (4, 3)
        ┌─────┬─────┬───────┐
        │ x   ┆ y   ┆ x < y │
        │ --- ┆ --- ┆ ---   │
        │ f64 ┆ f64 ┆ bool  │
        ╞═════╪═════╪═══════╡
        │ 1.0 ┆ 2.0 ┆ true  │
        │ 2.0 ┆ 2.0 ┆ false │
        │ NaN ┆ NaN ┆ false │
        │ 3.0 ┆ 4.0 ┆ true  │
        └─────┴─────┴───────┘

        """
        return self.__lt__(other)
