    def fill_nan(self, value: int | float | Expr | None) -> Self:
        """
        Fill floating point NaN value with a fill value.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1.0, None, float("nan")],
        ...         "b": [4.0, float("nan"), 6],
        ...     }
        ... )
        >>> df.with_columns(pl.col("b").fill_nan(0))
        shape: (3, 2)
        ┌──────┬─────┐
        │ a    ┆ b   │
        │ ---  ┆ --- │
        │ f64  ┆ f64 │
        ╞══════╪═════╡
        │ 1.0  ┆ 4.0 │
        │ null ┆ 0.0 │
        │ NaN  ┆ 6.0 │
        └──────┴─────┘

        """
        fill_value = parse_as_expression(value, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.fill_nan(fill_value))
