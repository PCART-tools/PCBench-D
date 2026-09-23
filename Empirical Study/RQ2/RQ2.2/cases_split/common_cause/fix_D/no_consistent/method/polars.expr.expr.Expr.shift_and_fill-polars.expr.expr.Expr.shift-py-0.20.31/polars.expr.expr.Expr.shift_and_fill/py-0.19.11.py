    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
    def shift_and_fill(
        self,
        fill_value: IntoExpr,
        *,
        n: int = 1,
    ) -> Self:
        """
        Shift values by the given number of places and fill the resulting null values.

        Parameters
        ----------
        fill_value
            Fill None values with the result of this expression.
        n
            Number of places to shift (may be negative).

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4]})
        >>> df.with_columns(foo_shifted=pl.col("foo").shift_and_fill("a", n=1))
        shape: (4, 2)
        ┌─────┬─────────────┐
        │ foo ┆ foo_shifted │
        │ --- ┆ ---         │
        │ i64 ┆ str         │
        ╞═════╪═════════════╡
        │ 1   ┆ a           │
        │ 2   ┆ 1           │
        │ 3   ┆ 2           │
        │ 4   ┆ 3           │
        └─────┴─────────────┘

        """
        fill_value = parse_as_expression(fill_value, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.shift_and_fill(n, fill_value))
