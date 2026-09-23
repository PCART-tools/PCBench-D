    def nanoseconds(self) -> Expr:
        """
        Extract the nanoseconds from a Duration type.

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
        ...         pl.col("date").diff().dt.nanoseconds().alias("nanoseconds_diff"),
        ...     ]
        ... )
        shape: (1_001, 2)
        ┌─────────────────────────┬──────────────────┐
        │ date                    ┆ nanoseconds_diff │
        │ ---                     ┆ ---              │
        │ datetime[μs]            ┆ i64              │
        ╞═════════════════════════╪══════════════════╡
        │ 2020-01-01 00:00:00     ┆ null             │
        │ 2020-01-01 00:00:00.001 ┆ 1000000          │
        │ 2020-01-01 00:00:00.002 ┆ 1000000          │
        │ 2020-01-01 00:00:00.003 ┆ 1000000          │
        │ …                       ┆ …                │
        │ 2020-01-01 00:00:00.997 ┆ 1000000          │
        │ 2020-01-01 00:00:00.998 ┆ 1000000          │
        │ 2020-01-01 00:00:00.999 ┆ 1000000          │
        │ 2020-01-01 00:00:01     ┆ 1000000          │
        └─────────────────────────┴──────────────────┘

        """
        return wrap_expr(self._pyexpr.duration_nanoseconds())
