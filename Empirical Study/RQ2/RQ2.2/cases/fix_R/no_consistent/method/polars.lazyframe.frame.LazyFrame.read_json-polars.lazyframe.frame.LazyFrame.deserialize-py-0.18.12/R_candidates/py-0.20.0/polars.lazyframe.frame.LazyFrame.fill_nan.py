    def fill_nan(self, value: int | float | Expr | None) -> Self:
        """
        Fill floating point NaN values.

        Parameters
        ----------
        value
            Value to fill the NaN values with.

        Warnings
        --------
        Note that floating point NaN (Not a Number) are not missing values!
        To replace missing values, use :func:`fill_null` instead.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1.5, 2, float("nan"), 4],
        ...         "b": [0.5, 4, float("nan"), 13],
        ...     }
        ... )
        >>> lf.fill_nan(99).collect()
        shape: (4, 2)
        ┌──────┬──────┐
        │ a    ┆ b    │
        │ ---  ┆ ---  │
        │ f64  ┆ f64  │
        ╞══════╪══════╡
        │ 1.5  ┆ 0.5  │
        │ 2.0  ┆ 4.0  │
        │ 99.0 ┆ 99.0 │
        │ 4.0  ┆ 13.0 │
        └──────┴──────┘

        """
        if not isinstance(value, pl.Expr):
            value = F.lit(value)
        return self._from_pyldf(self._ldf.fill_nan(value._pyexpr))
