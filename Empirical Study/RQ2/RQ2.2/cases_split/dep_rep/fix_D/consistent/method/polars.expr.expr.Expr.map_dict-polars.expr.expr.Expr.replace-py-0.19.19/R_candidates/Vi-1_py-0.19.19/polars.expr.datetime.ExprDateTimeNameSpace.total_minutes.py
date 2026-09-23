    def total_minutes(self) -> Expr:
        """
        Extract the total minutes from a Duration type.

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
        ...             datetime(2020, 1, 1), datetime(2020, 1, 4), "1d", eager=True
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date").diff().dt.total_minutes().alias("minutes_diff"),
        ...     ]
        ... )
        shape: (4, 2)
        ┌─────────────────────┬──────────────┐
        │ date                ┆ minutes_diff │
        │ ---                 ┆ ---          │
        │ datetime[μs]        ┆ i64          │
        ╞═════════════════════╪══════════════╡
        │ 2020-01-01 00:00:00 ┆ null         │
        │ 2020-01-02 00:00:00 ┆ 1440         │
        │ 2020-01-03 00:00:00 ┆ 1440         │
        │ 2020-01-04 00:00:00 ┆ 1440         │
        └─────────────────────┴──────────────┘

        """
        return wrap_expr(self._pyexpr.dt_total_minutes())
