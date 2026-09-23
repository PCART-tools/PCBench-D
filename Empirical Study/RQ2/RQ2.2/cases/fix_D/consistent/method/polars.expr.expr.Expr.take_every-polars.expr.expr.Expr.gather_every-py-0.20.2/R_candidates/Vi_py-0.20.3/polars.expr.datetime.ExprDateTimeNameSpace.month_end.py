    def month_end(self) -> Expr:
        """
        Roll forward to the last day of the month.

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Notes
        -----
        If you're coming from pandas, you can think of this as a vectorised version
        of `pandas.tseries.offsets.MonthEnd().rollforward(datetime)`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "dates": pl.datetime_range(
        ...             datetime(2000, 1, 1, 2),
        ...             datetime(2000, 12, 1, 2),
        ...             "1mo",
        ...             eager=True,
        ...         )
        ...     }
        ... )
        >>> df.select(pl.col("dates").dt.month_end())
        shape: (12, 1)
        ┌─────────────────────┐
        │ dates               │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2000-01-31 02:00:00 │
        │ 2000-02-29 02:00:00 │
        │ 2000-03-31 02:00:00 │
        │ 2000-04-30 02:00:00 │
        │ …                   │
        │ 2000-09-30 02:00:00 │
        │ 2000-10-31 02:00:00 │
        │ 2000-11-30 02:00:00 │
        │ 2000-12-31 02:00:00 │
        └─────────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_month_end())
