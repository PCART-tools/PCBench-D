    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
    def shift(
        self, n: int | IntoExprColumn = 1, *, fill_value: IntoExpr | None = None
    ) -> Self:
        """
        Shift values by the given number of indices.

        Parameters
        ----------
        n
            Number of indices to shift forward. If a negative value is passed, values
            are shifted in the opposite direction instead.
        fill_value
            Fill the resulting null values with this value.

        Notes
        -----
        This method is similar to the `LAG` operation in SQL when the value for `n`
        is positive. With a negative value for `n`, it is similar to `LEAD`.

        Examples
        --------
        By default, values are shifted forward by one index.

        >>> df = pl.DataFrame({"a": [1, 2, 3, 4]})
        >>> df.with_columns(shift=pl.col("a").shift())
        shape: (4, 2)
        ┌─────┬───────┐
        │ a   ┆ shift │
        │ --- ┆ ---   │
        │ i64 ┆ i64   │
        ╞═════╪═══════╡
        │ 1   ┆ null  │
        │ 2   ┆ 1     │
        │ 3   ┆ 2     │
        │ 4   ┆ 3     │
        └─────┴───────┘

        Pass a negative value to shift in the opposite direction instead.

        >>> df.with_columns(shift=pl.col("a").shift(-2))
        shape: (4, 2)
        ┌─────┬───────┐
        │ a   ┆ shift │
        │ --- ┆ ---   │
        │ i64 ┆ i64   │
        ╞═════╪═══════╡
        │ 1   ┆ 3     │
        │ 2   ┆ 4     │
        │ 3   ┆ null  │
        │ 4   ┆ null  │
        └─────┴───────┘

        Specify `fill_value` to fill the resulting null values.

        >>> df.with_columns(shift=pl.col("a").shift(-2, fill_value=100))
        shape: (4, 2)
        ┌─────┬───────┐
        │ a   ┆ shift │
        │ --- ┆ ---   │
        │ i64 ┆ i64   │
        ╞═════╪═══════╡
        │ 1   ┆ 3     │
        │ 2   ┆ 4     │
        │ 3   ┆ 100   │
        │ 4   ┆ 100   │
        └─────┴───────┘

        """
        if fill_value is not None:
            fill_value = parse_as_expression(fill_value, str_as_lit=True)
        n = parse_as_expression(n)
        return self._from_pyexpr(self._pyexpr.shift(n, fill_value))
