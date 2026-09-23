    def total_microseconds(self) -> Expr:
        """
        Extract the total microseconds from a Duration type.

        Returns
        -------
        Expr
            Expression of data type :class:`Int64`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.datetime_range(
        ...             datetime(2020, 1, 1),
        ...             datetime(2020, 1, 1, 0, 0, 1, 0),
        ...             "1ms",
        ...             eager=True,
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     pl.col("date"),
        ...     microseconds_diff=pl.col("date").diff().dt.total_microseconds(),
        ... )
        shape: (1_001, 2)
        ┌─────────────────────────┬───────────────────┐
        │ date                    ┆ microseconds_diff │
        │ ---                     ┆ ---               │
        │ datetime[μs]            ┆ i64               │
        ╞═════════════════════════╪═══════════════════╡
        │ 2020-01-01 00:00:00     ┆ null              │
        │ 2020-01-01 00:00:00.001 ┆ 1000              │
        │ 2020-01-01 00:00:00.002 ┆ 1000              │
        │ 2020-01-01 00:00:00.003 ┆ 1000              │
        │ …                       ┆ …                 │
        │ 2020-01-01 00:00:00.997 ┆ 1000              │
        │ 2020-01-01 00:00:00.998 ┆ 1000              │
        │ 2020-01-01 00:00:00.999 ┆ 1000              │
        │ 2020-01-01 00:00:01     ┆ 1000              │
        └─────────────────────────┴───────────────────┘

        """
        return wrap_expr(self._pyexpr.dt_total_microseconds())
