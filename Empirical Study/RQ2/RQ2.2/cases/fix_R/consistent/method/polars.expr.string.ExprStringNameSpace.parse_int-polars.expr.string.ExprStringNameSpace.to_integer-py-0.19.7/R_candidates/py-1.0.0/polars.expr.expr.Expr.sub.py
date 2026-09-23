    def sub(self, other: Any) -> Expr:
        """
        Method equivalent of subtraction operator `expr - other`.

        Parameters
        ----------
        other
            Numeric literal or expression value.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [0, 1, 2, 3, 4]})
        >>> df.with_columns(
        ...     pl.col("x").sub(2).alias("x-2"),
        ...     pl.col("x").sub(pl.col("x").cum_sum()).alias("x-expr"),
        ... )
        shape: (5, 3)
        ┌─────┬─────┬────────┐
        │ x   ┆ x-2 ┆ x-expr │
        │ --- ┆ --- ┆ ---    │
        │ i64 ┆ i64 ┆ i64    │
        ╞═════╪═════╪════════╡
        │ 0   ┆ -2  ┆ 0      │
        │ 1   ┆ -1  ┆ 0      │
        │ 2   ┆ 0   ┆ -1     │
        │ 3   ┆ 1   ┆ -3     │
        │ 4   ┆ 2   ┆ -6     │
        └─────┴─────┴────────┘
        """
        return self.__sub__(other)
