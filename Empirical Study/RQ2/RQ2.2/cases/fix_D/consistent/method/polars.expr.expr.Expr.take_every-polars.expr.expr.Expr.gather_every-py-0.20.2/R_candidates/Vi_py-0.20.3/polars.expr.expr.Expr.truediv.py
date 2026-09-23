    def truediv(self, other: Any) -> Self:
        """
        Method equivalent of float division operator `expr / other`.

        Parameters
        ----------
        other
            Numeric literal or expression value.

        Notes
        -----
        Zero-division behaviour follows IEEE-754:

        0/0: Invalid operation - mathematically undefined, returns NaN.
        n/0: On finite operands gives an exact infinite result, eg: ±infinity.

        See Also
        --------
        floordiv

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={"x": [-2, -1, 0, 1, 2], "y": [0.5, 0.0, 0.0, -4.0, -0.5]}
        ... )
        >>> df.with_columns(
        ...     pl.col("x").truediv(2).alias("x/2"),
        ...     pl.col("x").truediv(pl.col("y")).alias("x/y"),
        ... )
        shape: (5, 4)
        ┌─────┬──────┬──────┬───────┐
        │ x   ┆ y    ┆ x/2  ┆ x/y   │
        │ --- ┆ ---  ┆ ---  ┆ ---   │
        │ i64 ┆ f64  ┆ f64  ┆ f64   │
        ╞═════╪══════╪══════╪═══════╡
        │ -2  ┆ 0.5  ┆ -1.0 ┆ -4.0  │
        │ -1  ┆ 0.0  ┆ -0.5 ┆ -inf  │
        │ 0   ┆ 0.0  ┆ 0.0  ┆ NaN   │
        │ 1   ┆ -4.0 ┆ 0.5  ┆ -0.25 │
        │ 2   ┆ -0.5 ┆ 1.0  ┆ -4.0  │
        └─────┴──────┴──────┴───────┘

        """
        return self.__truediv__(other)
