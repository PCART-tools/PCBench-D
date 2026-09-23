    def combine(self, time: dt.time | Expr, time_unit: TimeUnit = "us") -> Expr:
        """
        Create a naive Datetime from an existing Date/Datetime expression and a Time.

        If the underlying expression is a Datetime then its time component is replaced,
        and if it is a Date then a new Datetime is created by combining the two values.

        Parameters
        ----------
        time
            A python time literal or polars expression/column that resolves to a time.
        time_unit : {'ns', 'us', 'ms'}
            Unit of time.

        Examples
        --------
        >>> from datetime import datetime, date, time
        >>> df = pl.DataFrame(
        ...     {
        ...         "dtm": [
        ...             datetime(2022, 12, 31, 10, 30, 45),
        ...             datetime(2023, 7, 5, 23, 59, 59),
        ...         ],
        ...         "dt": [date(2022, 10, 10), date(2022, 7, 5)],
        ...         "tm": [time(1, 2, 3, 456000), time(7, 8, 9, 101000)],
        ...     }
        ... )
        >>> df
        shape: (2, 3)
        ┌─────────────────────┬────────────┬──────────────┐
        │ dtm                 ┆ dt         ┆ tm           │
        │ ---                 ┆ ---        ┆ ---          │
        │ datetime[μs]        ┆ date       ┆ time         │
        ╞═════════════════════╪════════════╪══════════════╡
        │ 2022-12-31 10:30:45 ┆ 2022-10-10 ┆ 01:02:03.456 │
        │ 2023-07-05 23:59:59 ┆ 2022-07-05 ┆ 07:08:09.101 │
        └─────────────────────┴────────────┴──────────────┘
        >>> df.select(
        ...     [
        ...         pl.col("dtm").dt.combine(pl.col("tm")).alias("d1"),
        ...         pl.col("dt").dt.combine(pl.col("tm")).alias("d2"),
        ...         pl.col("dt").dt.combine(time(4, 5, 6)).alias("d3"),
        ...     ]
        ... )
        shape: (2, 3)
        ┌─────────────────────────┬─────────────────────────┬─────────────────────┐
        │ d1                      ┆ d2                      ┆ d3                  │
        │ ---                     ┆ ---                     ┆ ---                 │
        │ datetime[μs]            ┆ datetime[μs]            ┆ datetime[μs]        │
        ╞═════════════════════════╪═════════════════════════╪═════════════════════╡
        │ 2022-12-31 01:02:03.456 ┆ 2022-10-10 01:02:03.456 ┆ 2022-10-10 04:05:06 │
        │ 2023-07-05 07:08:09.101 ┆ 2022-07-05 07:08:09.101 ┆ 2022-07-05 04:05:06 │
        └─────────────────────────┴─────────────────────────┴─────────────────────┘
        """
        if not isinstance(time, (dt.time, pl.Expr)):
            msg = f"expected 'time' to be a Python time or Polars expression, found {type(time).__name__!r}"
            raise TypeError(msg)
        time = parse_as_expression(time)
        return wrap_expr(self._pyexpr.dt_combine(time, time_unit))
