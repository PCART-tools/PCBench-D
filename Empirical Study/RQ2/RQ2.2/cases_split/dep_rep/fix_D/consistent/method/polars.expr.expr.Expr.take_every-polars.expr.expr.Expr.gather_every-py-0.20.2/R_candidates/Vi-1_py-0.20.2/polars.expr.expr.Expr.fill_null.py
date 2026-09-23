    def fill_null(
        self,
        value: Any | None = None,
        strategy: FillNullStrategy | None = None,
        limit: int | None = None,
    ) -> Self:
        """
        Fill null values using the specified value or strategy.

        To interpolate over null values see interpolate.
        See the examples below to fill nulls with an expression.

        Parameters
        ----------
        value
            Value used to fill null values.
        strategy : {None, 'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one'}
            Strategy used to fill null values.
        limit
            Number of consecutive null values to fill when using the 'forward' or
            'backward' strategy.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, None],
        ...         "b": [4, None, 6],
        ...     }
        ... )
        >>> df.with_columns(pl.col("b").fill_null(strategy="zero"))
        shape: (3, 2)
        ┌──────┬─────┐
        │ a    ┆ b   │
        │ ---  ┆ --- │
        │ i64  ┆ i64 │
        ╞══════╪═════╡
        │ 1    ┆ 4   │
        │ 2    ┆ 0   │
        │ null ┆ 6   │
        └──────┴─────┘
        >>> df.with_columns(pl.col("b").fill_null(99))
        shape: (3, 2)
        ┌──────┬─────┐
        │ a    ┆ b   │
        │ ---  ┆ --- │
        │ i64  ┆ i64 │
        ╞══════╪═════╡
        │ 1    ┆ 4   │
        │ 2    ┆ 99  │
        │ null ┆ 6   │
        └──────┴─────┘
        >>> df.with_columns(pl.col("b").fill_null(strategy="forward"))
        shape: (3, 2)
        ┌──────┬─────┐
        │ a    ┆ b   │
        │ ---  ┆ --- │
        │ i64  ┆ i64 │
        ╞══════╪═════╡
        │ 1    ┆ 4   │
        │ 2    ┆ 4   │
        │ null ┆ 6   │
        └──────┴─────┘
        >>> df.with_columns(pl.col("b").fill_null(pl.col("b").median()))
        shape: (3, 2)
        ┌──────┬─────┐
        │ a    ┆ b   │
        │ ---  ┆ --- │
        │ i64  ┆ f64 │
        ╞══════╪═════╡
        │ 1    ┆ 4.0 │
        │ 2    ┆ 5.0 │
        │ null ┆ 6.0 │
        └──────┴─────┘
        >>> df.with_columns(pl.all().fill_null(pl.all().median()))
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ f64 ┆ f64 │
        ╞═════╪═════╡
        │ 1.0 ┆ 4.0 │
        │ 2.0 ┆ 5.0 │
        │ 1.5 ┆ 6.0 │
        └─────┴─────┘

        """
        if value is not None and strategy is not None:
            raise ValueError("cannot specify both `value` and `strategy`")
        elif value is None and strategy is None:
            raise ValueError("must specify either a fill `value` or `strategy`")
        elif strategy not in ("forward", "backward") and limit is not None:
            raise ValueError(
                "can only specify `limit` when strategy is set to 'backward' or 'forward'"
            )

        if value is not None:
            value = parse_as_expression(value, str_as_lit=True)
            return self._from_pyexpr(self._pyexpr.fill_null(value))
        else:
            return self._from_pyexpr(
                self._pyexpr.fill_null_with_strategy(strategy, limit)
            )
