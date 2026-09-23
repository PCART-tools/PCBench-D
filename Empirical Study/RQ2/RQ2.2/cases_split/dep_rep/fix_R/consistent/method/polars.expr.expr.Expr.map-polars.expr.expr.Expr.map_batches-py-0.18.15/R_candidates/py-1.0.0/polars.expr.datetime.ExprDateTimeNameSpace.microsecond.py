    def microsecond(self) -> Expr:
        """
        Extract microseconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

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
        ...     pl.col("datetime").dt.microsecond().alias("microsecond"),
        ... )
        shape: (3, 5)
        ┌─────────────────────────┬──────┬────────┬────────┬─────────────┐
        │ datetime                ┆ hour ┆ minute ┆ second ┆ microsecond │
        │ ---                     ┆ ---  ┆ ---    ┆ ---    ┆ ---         │
        │ datetime[μs]            ┆ i8   ┆ i8     ┆ i8     ┆ i32         │
        ╞═════════════════════════╪══════╪════════╪════════╪═════════════╡
        │ 1978-01-01 01:01:01     ┆ 1    ┆ 1      ┆ 1      ┆ 0           │
        │ 2024-10-13 05:30:14.500 ┆ 5    ┆ 30     ┆ 14     ┆ 500000      │
        │ 2065-01-01 10:20:30.060 ┆ 10   ┆ 20     ┆ 30     ┆ 60000       │
        └─────────────────────────┴──────┴────────┴────────┴─────────────┘
        """
        return wrap_expr(self._pyexpr.dt_microsecond())
