    def mul(self, other: Any) -> Expr:
        """
        Method equivalent of multiplication operator `expr * other`.

        Parameters
        ----------
        other
            Numeric literal or expression value.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [1, 2, 4, 8, 16]})
        >>> df.with_columns(
        ...     pl.col("x").mul(2).alias("x*2"),
        ...     pl.col("x").mul(pl.col("x").log(2)).alias("x * xlog2"),
        ... )
        shape: (5, 3)
        ┌─────┬─────┬───────────┐
        │ x   ┆ x*2 ┆ x * xlog2 │
        │ --- ┆ --- ┆ ---       │
        │ i64 ┆ i64 ┆ f64       │
        ╞═════╪═════╪═══════════╡
        │ 1   ┆ 2   ┆ 0.0       │
        │ 2   ┆ 4   ┆ 2.0       │
        │ 4   ┆ 8   ┆ 8.0       │
        │ 8   ┆ 16  ┆ 24.0      │
        │ 16  ┆ 32  ┆ 64.0      │
        └─────┴─────┴───────────┘
        """
        return self.__mul__(other)
