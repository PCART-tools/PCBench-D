    def milliseconds(self) -> Expr:
        """
        Extract the milliseconds from a Duration type.

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
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date").diff().dt.milliseconds().alias("milliseconds_diff"),
        ...     ]
        ... )
        shape: (1_001, 2)
        ┌─────────────────────────┬───────────────────┐
        │ date                    ┆ milliseconds_diff │
        │ ---                     ┆ ---               │
        │ datetime[μs]            ┆ i64               │
        ╞═════════════════════════╪═══════════════════╡
        │ 2020-01-01 00:00:00     ┆ null              │
        │ 2020-01-01 00:00:00.001 ┆ 1                 │
        │ 2020-01-01 00:00:00.002 ┆ 1                 │
        │ 2020-01-01 00:00:00.003 ┆ 1                 │
        │ …                       ┆ …                 │
        │ 2020-01-01 00:00:00.997 ┆ 1                 │
        │ 2020-01-01 00:00:00.998 ┆ 1                 │
        │ 2020-01-01 00:00:00.999 ┆ 1                 │
        │ 2020-01-01 00:00:01     ┆ 1                 │
        └─────────────────────────┴───────────────────┘

        """
        return wrap_expr(self._pyexpr.duration_milliseconds())
