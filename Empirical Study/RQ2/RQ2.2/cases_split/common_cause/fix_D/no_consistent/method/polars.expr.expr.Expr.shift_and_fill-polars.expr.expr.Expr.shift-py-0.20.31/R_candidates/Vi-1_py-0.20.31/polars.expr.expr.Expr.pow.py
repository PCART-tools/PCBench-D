    def pow(self, exponent: IntoExprColumn | int | float) -> Self:
        """
        Method equivalent of exponentiation operator `expr ** exponent`.

        Parameters
        ----------
        exponent
            Numeric literal or expression exponent value.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [1, 2, 4, 8]})
        >>> df.with_columns(
        ...     pl.col("x").pow(3).alias("cube"),
        ...     pl.col("x").pow(pl.col("x").log(2)).alias("x ** xlog2"),
        ... )
        shape: (4, 3)
        ┌─────┬──────┬────────────┐
        │ x   ┆ cube ┆ x ** xlog2 │
        │ --- ┆ ---  ┆ ---        │
        │ i64 ┆ i64  ┆ f64        │
        ╞═════╪══════╪════════════╡
        │ 1   ┆ 1    ┆ 1.0        │
        │ 2   ┆ 8    ┆ 2.0        │
        │ 4   ┆ 64   ┆ 16.0       │
        │ 8   ┆ 512  ┆ 512.0      │
        └─────┴──────┴────────────┘
        """
        return self.__pow__(exponent)
