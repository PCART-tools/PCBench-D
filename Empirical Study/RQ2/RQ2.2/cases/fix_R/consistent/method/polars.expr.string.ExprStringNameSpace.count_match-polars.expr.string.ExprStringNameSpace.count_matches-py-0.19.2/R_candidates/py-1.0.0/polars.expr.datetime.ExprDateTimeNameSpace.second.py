    def second(self, *, fractional: bool = False) -> Expr:
        """
        Extract seconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns the integer second number from 0 to 59, or a floating
        point number from 0 < 60 if `fractional=True` that includes
        any milli/micro/nanosecond component.

        Parameters
        ----------
        fractional
            Whether to include the fractional component of the second.

        Returns
        -------
        Expr
            Expression of data type :class:`Int8` or :class:`Float64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime": [
        ...             datetime(1978, 1, 1, 1, 1, 1, 0),
        ...             datetime(2024, 10, 13, 5, 30, 14, 500_000),
        ...             datetime(2065, 1, 1, 10, 20, 30, 60_000),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("datetime").dt.hour().alias("hour"),
        ...     pl.col("datetime").dt.minute().alias("minute"),
        ...     pl.col("datetime").dt.second().alias("second"),
        ... )
        shape: (3, 4)
        ┌─────────────────────────┬──────┬────────┬────────┐
        │ datetime                ┆ hour ┆ minute ┆ second │
        │ ---                     ┆ ---  ┆ ---    ┆ ---    │
        │ datetime[μs]            ┆ i8   ┆ i8     ┆ i8     │
        ╞═════════════════════════╪══════╪════════╪════════╡
        │ 1978-01-01 01:01:01     ┆ 1    ┆ 1      ┆ 1      │
        │ 2024-10-13 05:30:14.500 ┆ 5    ┆ 30     ┆ 14     │
        │ 2065-01-01 10:20:30.060 ┆ 10   ┆ 20     ┆ 30     │
        └─────────────────────────┴──────┴────────┴────────┘
        >>> df.with_columns(
        ...     pl.col("datetime").dt.hour().alias("hour"),
        ...     pl.col("datetime").dt.minute().alias("minute"),
        ...     pl.col("datetime").dt.second(fractional=True).alias("second"),
        ... )
        shape: (3, 4)
        ┌─────────────────────────┬──────┬────────┬────────┐
        │ datetime                ┆ hour ┆ minute ┆ second │
        │ ---                     ┆ ---  ┆ ---    ┆ ---    │
        │ datetime[μs]            ┆ i8   ┆ i8     ┆ f64    │
        ╞═════════════════════════╪══════╪════════╪════════╡
        │ 1978-01-01 01:01:01     ┆ 1    ┆ 1      ┆ 1.0    │
        │ 2024-10-13 05:30:14.500 ┆ 5    ┆ 30     ┆ 14.5   │
        │ 2065-01-01 10:20:30.060 ┆ 10   ┆ 20     ┆ 30.06  │
        └─────────────────────────┴──────┴────────┴────────┘
        """
        sec = wrap_expr(self._pyexpr.dt_second())
        return (
            sec + (wrap_expr(self._pyexpr.dt_nanosecond()) / F.lit(1_000_000_000.0))
            if fractional
            else sec
        )
