    def mod(self, other: Any) -> Self:
        """
        Method equivalent of modulus operator `expr % other`.

        Parameters
        ----------
        other
            Numeric literal or expression value.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [0, 1, 2, 3, 4]})
        >>> df.with_columns(pl.col("x").mod(2).alias("x%2"))
        shape: (5, 2)
        ┌─────┬─────┐
        │ x   ┆ x%2 │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 0   ┆ 0   │
        │ 1   ┆ 1   │
        │ 2   ┆ 0   │
        │ 3   ┆ 1   │
        │ 4   ┆ 0   │
        └─────┴─────┘
        """
        return self.__mod__(other)
