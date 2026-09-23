    def total_seconds(self) -> Expr:
        """
        Extract the total seconds from a Duration type.

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
        ...             datetime(2020, 1, 1, 0, 4, 0),
        ...             "1m",
        ...             eager=True,
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     pl.col("date"),
        ...     pl.col("date").diff().dt.total_seconds().alias("seconds_diff"),
        ... )
        shape: (5, 2)
        ┌─────────────────────┬──────────────┐
        │ date                ┆ seconds_diff │
        │ ---                 ┆ ---          │
        │ datetime[μs]        ┆ i64          │
        ╞═════════════════════╪══════════════╡
        │ 2020-01-01 00:00:00 ┆ null         │
        │ 2020-01-01 00:01:00 ┆ 60           │
        │ 2020-01-01 00:02:00 ┆ 60           │
        │ 2020-01-01 00:03:00 ┆ 60           │
        │ 2020-01-01 00:04:00 ┆ 60           │
        └─────────────────────┴──────────────┘
        """
        return wrap_expr(self._pyexpr.dt_total_seconds())
