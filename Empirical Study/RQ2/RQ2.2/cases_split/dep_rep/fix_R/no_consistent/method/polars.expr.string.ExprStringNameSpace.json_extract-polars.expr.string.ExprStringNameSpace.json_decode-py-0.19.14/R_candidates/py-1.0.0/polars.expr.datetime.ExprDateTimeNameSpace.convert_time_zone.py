    def convert_time_zone(self, time_zone: str) -> Expr:
        """
        Convert to given time zone for an expression of type Datetime.

        Parameters
        ----------
        time_zone
            Time zone for the `Datetime` expression.

        Notes
        -----
        If converting from a time-zone-naive datetime, then conversion will happen
        as if converting from UTC, regardless of your system's time zone.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.datetime_range(
        ...             datetime(2020, 3, 1),
        ...             datetime(2020, 5, 1),
        ...             "1mo",
        ...             time_zone="UTC",
        ...             eager=True,
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date")
        ...         .dt.convert_time_zone(time_zone="Europe/London")
        ...         .alias("London"),
        ...     ]
        ... )
        shape: (3, 2)
        ┌─────────────────────────┬─────────────────────────────┐
        │ date                    ┆ London                      │
        │ ---                     ┆ ---                         │
        │ datetime[μs, UTC]       ┆ datetime[μs, Europe/London] │
        ╞═════════════════════════╪═════════════════════════════╡
        │ 2020-03-01 00:00:00 UTC ┆ 2020-03-01 00:00:00 GMT     │
        │ 2020-04-01 00:00:00 UTC ┆ 2020-04-01 01:00:00 BST     │
        │ 2020-05-01 00:00:00 UTC ┆ 2020-05-01 01:00:00 BST     │
        └─────────────────────────┴─────────────────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_convert_time_zone(time_zone))
