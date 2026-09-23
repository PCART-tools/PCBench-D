    def total_milliseconds(self) -> Expr:
        """
        Extract the total milliseconds from a Duration type.

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
        ...             "200ms",
        ...             eager=True,
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     pl.col("date"),
        ...     milliseconds_diff=pl.col("date").diff().dt.total_milliseconds(),
        ... )
        shape: (6, 2)
        ┌─────────────────────────┬───────────────────┐
        │ date                    ┆ milliseconds_diff │
        │ ---                     ┆ ---               │
        │ datetime[μs]            ┆ i64               │
        ╞═════════════════════════╪═══════════════════╡
        │ 2020-01-01 00:00:00     ┆ null              │
        │ 2020-01-01 00:00:00.200 ┆ 200               │
        │ 2020-01-01 00:00:00.400 ┆ 200               │
        │ 2020-01-01 00:00:00.600 ┆ 200               │
        │ 2020-01-01 00:00:00.800 ┆ 200               │
        │ 2020-01-01 00:00:01     ┆ 200               │
        └─────────────────────────┴───────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_total_milliseconds())
