    def days(self) -> Expr:
        """
        Extract the days from a Duration type.

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
        ...             datetime(2020, 3, 1), datetime(2020, 5, 1), "1mo", eager=True
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date").diff().dt.days().alias("days_diff"),
        ...     ]
        ... )
        shape: (3, 2)
        ┌─────────────────────┬───────────┐
        │ date                ┆ days_diff │
        │ ---                 ┆ ---       │
        │ datetime[μs]        ┆ i64       │
        ╞═════════════════════╪═══════════╡
        │ 2020-03-01 00:00:00 ┆ null      │
        │ 2020-04-01 00:00:00 ┆ 31        │
        │ 2020-05-01 00:00:00 ┆ 30        │
        └─────────────────────┴───────────┘

        """
        return wrap_expr(self._pyexpr.duration_days())
