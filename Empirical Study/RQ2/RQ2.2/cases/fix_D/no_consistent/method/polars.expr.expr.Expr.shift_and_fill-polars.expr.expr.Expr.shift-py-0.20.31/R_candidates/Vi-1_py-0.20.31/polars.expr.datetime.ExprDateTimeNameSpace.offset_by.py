    def offset_by(self, by: str | Expr) -> Expr:
        """
        Offset this date by a relative time offset.

        This differs from `pl.col("foo") + timedelta` in that it can
        take months and leap years into account. Note that only a single minus
        sign is allowed in the `by` string, as the first character.

        Parameters
        ----------
        by
            The offset is dictated by the following string language:

            - 1ns   (1 nanosecond)
            - 1us   (1 microsecond)
            - 1ms   (1 millisecond)
            - 1s    (1 second)
            - 1m    (1 minute)
            - 1h    (1 hour)
            - 1d    (1 calendar day)
            - 1w    (1 calendar week)
            - 1mo   (1 calendar month)
            - 1q    (1 calendar quarter)
            - 1y    (1 calendar year)

            By "calendar day", we mean the corresponding time on the next day (which may
            not be 24 hours, due to daylight savings). Similarly for "calendar week",
            "calendar month", "calendar quarter", and "calendar year".

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "dates": pl.datetime_range(
        ...             datetime(2000, 1, 1), datetime(2005, 1, 1), "1y", eager=True
        ...         ),
        ...         "offset": ["1d", "2d", "-1d", "1mo", None, "1y"],
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("dates").dt.offset_by("1y").alias("date_plus_1y"),
        ...         pl.col("dates").dt.offset_by("-1y2mo").alias("date_min"),
        ...     ]
        ... )
        shape: (6, 2)
        ┌─────────────────────┬─────────────────────┐
        │ date_plus_1y        ┆ date_min            │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 1998-11-01 00:00:00 │
        │ 2002-01-01 00:00:00 ┆ 1999-11-01 00:00:00 │
        │ 2003-01-01 00:00:00 ┆ 2000-11-01 00:00:00 │
        │ 2004-01-01 00:00:00 ┆ 2001-11-01 00:00:00 │
        │ 2005-01-01 00:00:00 ┆ 2002-11-01 00:00:00 │
        │ 2006-01-01 00:00:00 ┆ 2003-11-01 00:00:00 │
        └─────────────────────┴─────────────────────┘

        You can also pass the relative offset as an expression:

        >>> df.with_columns(new_dates=pl.col("dates").dt.offset_by(pl.col("offset")))
        shape: (6, 3)
        ┌─────────────────────┬────────┬─────────────────────┐
        │ dates               ┆ offset ┆ new_dates           │
        │ ---                 ┆ ---    ┆ ---                 │
        │ datetime[μs]        ┆ str    ┆ datetime[μs]        │
        ╞═════════════════════╪════════╪═════════════════════╡
        │ 2000-01-01 00:00:00 ┆ 1d     ┆ 2000-01-02 00:00:00 │
        │ 2001-01-01 00:00:00 ┆ 2d     ┆ 2001-01-03 00:00:00 │
        │ 2002-01-01 00:00:00 ┆ -1d    ┆ 2001-12-31 00:00:00 │
        │ 2003-01-01 00:00:00 ┆ 1mo    ┆ 2003-02-01 00:00:00 │
        │ 2004-01-01 00:00:00 ┆ null   ┆ null                │
        │ 2005-01-01 00:00:00 ┆ 1y     ┆ 2006-01-01 00:00:00 │
        └─────────────────────┴────────┴─────────────────────┘
        """
        by = deprecate_saturating(by)
        by = parse_as_expression(by, str_as_lit=True)
        return wrap_expr(self._pyexpr.dt_offset_by(by))
