    def month_start(self) -> Expr:
        """
        Roll backward to the first day of the month.

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Notes
        -----
        If you're coming from pandas, you can think of this as a vectorised version
        of ``pandas.tseries.offsets.MonthBegin().rollback(datetime)``.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "dates": pl.datetime_range(
        ...             datetime(2000, 1, 15, 2),
        ...             datetime(2000, 12, 15, 2),
        ...             "1mo",
        ...             eager=True,
        ...         )
        ...     }
        ... )
        >>> df.select(pl.col("dates").dt.month_start())
        shape: (12, 1)
        ┌─────────────────────┐
        │ dates               │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2000-01-01 02:00:00 │
        │ 2000-02-01 02:00:00 │
        │ 2000-03-01 02:00:00 │
        │ 2000-04-01 02:00:00 │
        │ …                   │
        │ 2000-09-01 02:00:00 │
        │ 2000-10-01 02:00:00 │
        │ 2000-11-01 02:00:00 │
        │ 2000-12-01 02:00:00 │
        └─────────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_month_start())
