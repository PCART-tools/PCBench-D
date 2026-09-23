    def interpolate_by(self, by: IntoExpr) -> Self:
        """
        Fill null values using interpolation based on another column.

        Parameters
        ----------
        by
            Column to interpolate values based on.

        Examples
        --------
        Fill null values using linear interpolation.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, None, None, 3],
        ...         "b": [1, 2, 7, 8],
        ...     }
        ... )
        >>> df.with_columns(a_interpolated=pl.col("a").interpolate_by("b"))
        shape: (4, 3)
        ┌──────┬─────┬────────────────┐
        │ a    ┆ b   ┆ a_interpolated │
        │ ---  ┆ --- ┆ ---            │
        │ i64  ┆ i64 ┆ f64            │
        ╞══════╪═════╪════════════════╡
        │ 1    ┆ 1   ┆ 1.0            │
        │ null ┆ 2   ┆ 1.285714       │
        │ null ┆ 7   ┆ 2.714286       │
        │ 3    ┆ 8   ┆ 3.0            │
        └──────┴─────┴────────────────┘
        """
        by = parse_as_expression(by)
        return self._from_pyexpr(self._pyexpr.interpolate_by(by))
