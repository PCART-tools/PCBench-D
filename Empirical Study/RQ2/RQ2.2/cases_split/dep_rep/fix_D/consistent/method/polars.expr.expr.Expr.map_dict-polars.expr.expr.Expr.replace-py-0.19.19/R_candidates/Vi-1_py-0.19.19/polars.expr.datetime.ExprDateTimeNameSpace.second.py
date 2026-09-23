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
            Expression of data type :class:`UInt32` or :class:`Float64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime": [
        ...             datetime(2000, 1, 1, 0, 0, 0, 456789),
        ...             datetime(2000, 1, 1, 0, 0, 3, 111110),
        ...             datetime(2000, 1, 1, 0, 0, 5, 765431),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(pl.col("datetime").dt.second().alias("second"))
        shape: (3, 2)
        ┌────────────────────────────┬────────┐
        │ datetime                   ┆ second │
        │ ---                        ┆ ---    │
        │ datetime[μs]               ┆ u32    │
        ╞════════════════════════════╪════════╡
        │ 2000-01-01 00:00:00.456789 ┆ 0      │
        │ 2000-01-01 00:00:03.111110 ┆ 3      │
        │ 2000-01-01 00:00:05.765431 ┆ 5      │
        └────────────────────────────┴────────┘
        >>> df.with_columns(
        ...     pl.col("datetime").dt.second(fractional=True).alias("second")
        ... )
        shape: (3, 2)
        ┌────────────────────────────┬──────────┐
        │ datetime                   ┆ second   │
        │ ---                        ┆ ---      │
        │ datetime[μs]               ┆ f64      │
        ╞════════════════════════════╪══════════╡
        │ 2000-01-01 00:00:00.456789 ┆ 0.456789 │
        │ 2000-01-01 00:00:03.111110 ┆ 3.11111  │
        │ 2000-01-01 00:00:05.765431 ┆ 5.765431 │
        └────────────────────────────┴──────────┘

        """
        sec = wrap_expr(self._pyexpr.dt_second())
        return (
            sec + (wrap_expr(self._pyexpr.dt_nanosecond()) / F.lit(1_000_000_000.0))
            if fractional
            else sec
        )
