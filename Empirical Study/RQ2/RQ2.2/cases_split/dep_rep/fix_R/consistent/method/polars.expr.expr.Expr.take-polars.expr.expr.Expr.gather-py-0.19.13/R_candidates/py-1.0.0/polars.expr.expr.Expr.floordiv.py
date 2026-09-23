    def floordiv(self, other: Any) -> Expr:
        """
        Method equivalent of integer division operator `expr // other`.

        Parameters
        ----------
        other
            Numeric literal or expression value.

        See Also
        --------
        truediv

        Examples
        --------
        >>> df = pl.DataFrame({"x": [1, 2, 3, 4, 5]})
        >>> df.with_columns(
        ...     pl.col("x").truediv(2).alias("x/2"),
        ...     pl.col("x").floordiv(2).alias("x//2"),
        ... )
        shape: (5, 3)
        ┌─────┬─────┬──────┐
        │ x   ┆ x/2 ┆ x//2 │
        │ --- ┆ --- ┆ ---  │
        │ i64 ┆ f64 ┆ i64  │
        ╞═════╪═════╪══════╡
        │ 1   ┆ 0.5 ┆ 0    │
        │ 2   ┆ 1.0 ┆ 1    │
        │ 3   ┆ 1.5 ┆ 1    │
        │ 4   ┆ 2.0 ┆ 2    │
        │ 5   ┆ 2.5 ┆ 2    │
        └─────┴─────┴──────┘

        Note that Polars' `floordiv` is subtly different from Python's floor division.
        For example, consider 6.0 floor-divided by 0.1.
        Python gives:

        >>> 6.0 // 0.1
        59.0

        because `0.1` is not represented internally as that exact value,
        but a slightly larger value.
        So the result of the division is slightly less than 60,
        meaning the flooring operation returns 59.0.

        Polars instead first does the floating-point division,
        resulting in a floating-point value of 60.0,
        and then performs the flooring operation using :any:`floor`:

        >>> df = pl.DataFrame({"x": [6.0, 6.03]})
        >>> df.with_columns(
        ...     pl.col("x").truediv(0.1).alias("x/0.1"),
        ... ).with_columns(
        ...     pl.col("x/0.1").floor().alias("x/0.1 floor"),
        ... )
        shape: (2, 3)
        ┌──────┬───────┬─────────────┐
        │ x    ┆ x/0.1 ┆ x/0.1 floor │
        │ ---  ┆ ---   ┆ ---         │
        │ f64  ┆ f64   ┆ f64         │
        ╞══════╪═══════╪═════════════╡
        │ 6.0  ┆ 60.0  ┆ 60.0        │
        │ 6.03 ┆ 60.3  ┆ 60.0        │
        └──────┴───────┴─────────────┘

        yielding the more intuitive result 60.0.
        The row with x = 6.03 is included to demonstrate
        the effect of the flooring operation.

        `floordiv` combines those two steps
        to give the same result with one expression:

        >>> df.with_columns(
        ...     pl.col("x").floordiv(0.1).alias("x//0.1"),
        ... )
        shape: (2, 2)
        ┌──────┬────────┐
        │ x    ┆ x//0.1 │
        │ ---  ┆ ---    │
        │ f64  ┆ f64    │
        ╞══════╪════════╡
        │ 6.0  ┆ 60.0   │
        │ 6.03 ┆ 60.0   │
        └──────┴────────┘
        """
        return self.__floordiv__(other)
