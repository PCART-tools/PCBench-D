    @deprecate_renamed_parameter("periods", "n", version="0.19.11")
    def shift_and_fill(
        self,
        fill_value: Expr | int | str | float,
        *,
        n: int = 1,
    ) -> Self:
        """
        Shift values by the given number of places and fill the resulting null values.

        Parameters
        ----------
        fill_value
            fill None values with the result of this expression.
        n
            Number of places to shift (may be negative).

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> lf.shift_and_fill(fill_value=0, n=1).collect()
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 0   ┆ 0   │
        │ 1   ┆ 2   │
        │ 3   ┆ 4   │
        └─────┴─────┘
        >>> lf.shift_and_fill(fill_value=0, n=-1).collect()
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 3   ┆ 4   │
        │ 5   ┆ 6   │
        │ 0   ┆ 0   │
        └─────┴─────┘

        """
        if not isinstance(fill_value, pl.Expr):
            fill_value = F.lit(fill_value)
        return self._from_pyldf(self._ldf.shift_and_fill(n, fill_value._pyexpr))
