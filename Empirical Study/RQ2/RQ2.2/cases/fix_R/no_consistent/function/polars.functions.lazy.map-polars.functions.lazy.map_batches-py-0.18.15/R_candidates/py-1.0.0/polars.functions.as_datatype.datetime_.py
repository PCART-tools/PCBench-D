def datetime_(
    year: int | IntoExpr,
    month: int | IntoExpr,
    day: int | IntoExpr,
    hour: int | IntoExpr | None = None,
    minute: int | IntoExpr | None = None,
    second: int | IntoExpr | None = None,
    microsecond: int | IntoExpr | None = None,
    *,
    time_unit: TimeUnit = "us",
    time_zone: str | None = None,
    ambiguous: Ambiguous | Expr = "raise",
) -> Expr:
    """
    Create a Polars literal expression of type Datetime.

    Parameters
    ----------
    year
        Column or literal.
    month
        Column or literal, ranging from 1-12.
    day
        Column or literal, ranging from 1-31.
    hour
        Column or literal, ranging from 0-23.
    minute
        Column or literal, ranging from 0-59.
    second
        Column or literal, ranging from 0-59.
    microsecond
        Column or literal, ranging from 0-999999.
    time_unit : {'us', 'ms', 'ns'}
        Time unit of the resulting expression.
    time_zone
        Time zone of the resulting expression.
    ambiguous
        Determine how to deal with ambiguous datetimes:

        - `'raise'` (default): raise
        - `'earliest'`: use the earliest datetime
        - `'latest'`: use the latest datetime
        - `'null'`: set to null

    Returns
    -------
    Expr
        Expression of data type :class:`Datetime`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "month": [1, 2, 3],
    ...         "day": [4, 5, 6],
    ...         "hour": [12, 13, 14],
    ...         "minute": [15, 30, 45],
    ...     }
    ... )
    >>> df.with_columns(
    ...     pl.datetime(
    ...         2024,
    ...         pl.col("month"),
    ...         pl.col("day"),
    ...         pl.col("hour"),
    ...         pl.col("minute"),
    ...         time_zone="Australia/Sydney",
    ...     )
    ... )
    shape: (3, 5)
    ┌───────┬─────┬──────┬────────┬────────────────────────────────┐
    │ month ┆ day ┆ hour ┆ minute ┆ datetime                       │
    │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---                            │
    │ i64   ┆ i64 ┆ i64  ┆ i64    ┆ datetime[μs, Australia/Sydney] │
    ╞═══════╪═════╪══════╪════════╪════════════════════════════════╡
    │ 1     ┆ 4   ┆ 12   ┆ 15     ┆ 2024-01-04 12:15:00 AEDT       │
    │ 2     ┆ 5   ┆ 13   ┆ 30     ┆ 2024-02-05 13:30:00 AEDT       │
    │ 3     ┆ 6   ┆ 14   ┆ 45     ┆ 2024-03-06 14:45:00 AEDT       │
    └───────┴─────┴──────┴────────┴────────────────────────────────┘

    We can also use `pl.datetime` for filtering:

    >>> from datetime import datetime
    >>> df = pl.DataFrame(
    ...     {
    ...         "start": [
    ...             datetime(2024, 1, 1, 0, 0, 0),
    ...             datetime(2024, 1, 1, 0, 0, 0),
    ...             datetime(2024, 1, 1, 0, 0, 0),
    ...         ],
    ...         "end": [
    ...             datetime(2024, 5, 1, 20, 15, 10),
    ...             datetime(2024, 7, 1, 21, 25, 20),
    ...             datetime(2024, 9, 1, 22, 35, 30),
    ...         ],
    ...     }
    ... )
    >>> df.filter(pl.col("end") > pl.datetime(2024, 6, 1))
        shape: (2, 2)
    ┌─────────────────────┬─────────────────────┐
    │ start               ┆ end                 │
    │ ---                 ┆ ---                 │
    │ datetime[μs]        ┆ datetime[μs]        │
    ╞═════════════════════╪═════════════════════╡
    │ 2024-01-01 00:00:00 ┆ 2024-07-01 21:25:20 │
    │ 2024-01-01 00:00:00 ┆ 2024-09-01 22:35:30 │
    └─────────────────────┴─────────────────────┘
    """
    ambiguous_expr = parse_into_expression(ambiguous, str_as_lit=True)
    year_expr = parse_into_expression(year)
    month_expr = parse_into_expression(month)
    day_expr = parse_into_expression(day)

    if hour is not None:
        hour = parse_into_expression(hour)
    if minute is not None:
        minute = parse_into_expression(minute)
    if second is not None:
        second = parse_into_expression(second)
    if microsecond is not None:
        microsecond = parse_into_expression(microsecond)

    return wrap_expr(
        plr.datetime(
            year_expr,
            month_expr,
            day_expr,
            hour,
            minute,
            second,
            microsecond,
            time_unit,
            time_zone,
            ambiguous_expr,
        )
    )
