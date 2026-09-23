    def eq_missing(self, other: Any) -> Self:
        """
        Method equivalent of equality operator `expr == other` where `None == None`.

        This differs from default `eq` where null values are propagated.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [1.0, 2.0, float("nan"), 4.0, None, None],
        ...         "y": [2.0, 2.0, float("nan"), 4.0, 5.0, None],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("x").eq(pl.col("y")).alias("x eq y"),
        ...     pl.col("x").eq_missing(pl.col("y")).alias("x eq_missing y"),
        ... )
        shape: (6, 4)
        ┌──────┬──────┬────────┬────────────────┐
        │ x    ┆ y    ┆ x eq y ┆ x eq_missing y │
        │ ---  ┆ ---  ┆ ---    ┆ ---            │
        │ f64  ┆ f64  ┆ bool   ┆ bool           │
        ╞══════╪══════╪════════╪════════════════╡
        │ 1.0  ┆ 2.0  ┆ false  ┆ false          │
        │ 2.0  ┆ 2.0  ┆ true   ┆ true           │
        │ NaN  ┆ NaN  ┆ true   ┆ true           │
        │ 4.0  ┆ 4.0  ┆ true   ┆ true           │
        │ null ┆ 5.0  ┆ null   ┆ false          │
        │ null ┆ null ┆ null   ┆ true           │
        └──────┴──────┴────────┴────────────────┘
        """
        other = parse_as_expression(other, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.eq_missing(other))
