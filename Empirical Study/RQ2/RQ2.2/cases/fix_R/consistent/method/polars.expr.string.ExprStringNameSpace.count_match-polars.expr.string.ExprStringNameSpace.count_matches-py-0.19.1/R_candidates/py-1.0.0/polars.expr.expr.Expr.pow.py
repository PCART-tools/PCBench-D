    def pow(self, exponent: IntoExprColumn | int | float) -> Expr:
        """
        Method equivalent of exponentiation operator `expr ** exponent`.

        If the exponent is float, the result follows the dtype of exponent.
        Otherwise, it follows dtype of base.

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

        Raising an integer to a positive integer results in an integer - in order
        to raise to a negative integer, you can cast either the base or the exponent
        to float first:

        >>> df.with_columns(
        ...     x_squared=pl.col("x").pow(2),
        ...     x_inverse=pl.col("x").pow(-1.0),
        ... )
        shape: (4, 3)
        ┌─────┬───────────┬───────────┐
        │ x   ┆ x_squared ┆ x_inverse │
        │ --- ┆ ---       ┆ ---       │
        │ i64 ┆ i64       ┆ f64       │
        ╞═════╪═══════════╪═══════════╡
        │ 1   ┆ 1         ┆ 1.0       │
        │ 2   ┆ 4         ┆ 0.5       │
        │ 4   ┆ 16        ┆ 0.25      │
        │ 8   ┆ 64        ┆ 0.125     │
        └─────┴───────────┴───────────┘
        """
        return self.__pow__(exponent)
