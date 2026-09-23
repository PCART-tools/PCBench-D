def duration(
    *,
    days: Expr | str | int | None = None,
    seconds: Expr | str | int | None = None,
    nanoseconds: Expr | str | int | None = None,
    microseconds: Expr | str | int | None = None,
    milliseconds: Expr | str | int | None = None,
    minutes: Expr | str | int | None = None,
    hours: Expr | str | int | None = None,
    weeks: Expr | str | int | None = None,
) -> Expr:
    """
    Create polars `Duration` from distinct time components.

    Returns
    -------
    Expr
        Expression of data type :class:`Duration`.

    Notes
    -----
    A `duration` represents a fixed amount of time. For example,
    ``pl.duration(days=1)`` means "exactly 24 hours". By contrast,
    ``Expr.dt.offset_by('1d')`` means "1 calendar day", which could sometimes be
    23 hours or 25 hours depending on Daylight Savings Time.
    For non-fixed durations such as "calendar month" or "calendar day",
    please use :meth:`polars.Expr.dt.offset_by` instead.

    Examples
    --------
    >>> from datetime import datetime
    >>> df = pl.DataFrame(
    ...     {
    ...         "dt": [datetime(2022, 1, 1), datetime(2022, 1, 2)],
    ...         "add": [1, 2],
    ...     }
    ... )
    >>> df
    shape: (2, 2)
    ┌─────────────────────┬─────┐
    │ dt                  ┆ add │
    │ ---                 ┆ --- │
    │ datetime[μs]        ┆ i64 │
    ╞═════════════════════╪═════╡
    │ 2022-01-01 00:00:00 ┆ 1   │
    │ 2022-01-02 00:00:00 ┆ 2   │
    └─────────────────────┴─────┘
    >>> with pl.Config(tbl_width_chars=120):
    ...     df.select(
    ...         (pl.col("dt") + pl.duration(weeks="add")).alias("add_weeks"),
    ...         (pl.col("dt") + pl.duration(days="add")).alias("add_days"),
    ...         (pl.col("dt") + pl.duration(seconds="add")).alias("add_seconds"),
    ...         (pl.col("dt") + pl.duration(milliseconds="add")).alias("add_millis"),
    ...         (pl.col("dt") + pl.duration(hours="add")).alias("add_hours"),
    ...     )
    ...
    shape: (2, 5)
    ┌─────────────────────┬─────────────────────┬─────────────────────┬─────────────────────────┬─────────────────────┐
    │ add_weeks           ┆ add_days            ┆ add_seconds         ┆ add_millis              ┆ add_hours           │
    │ ---                 ┆ ---                 ┆ ---                 ┆ ---                     ┆ ---                 │
    │ datetime[μs]        ┆ datetime[μs]        ┆ datetime[μs]        ┆ datetime[μs]            ┆ datetime[μs]        │
    ╞═════════════════════╪═════════════════════╪═════════════════════╪═════════════════════════╪═════════════════════╡
    │ 2022-01-08 00:00:00 ┆ 2022-01-02 00:00:00 ┆ 2022-01-01 00:00:01 ┆ 2022-01-01 00:00:00.001 ┆ 2022-01-01 01:00:00 │
    │ 2022-01-16 00:00:00 ┆ 2022-01-04 00:00:00 ┆ 2022-01-02 00:00:02 ┆ 2022-01-02 00:00:00.002 ┆ 2022-01-02 02:00:00 │
    └─────────────────────┴─────────────────────┴─────────────────────┴─────────────────────────┴─────────────────────┘

    If you need to add non-fixed durations, you should use :meth:`polars.Expr.dt.offset_by` instead:

    >>> with pl.Config(tbl_width_chars=120):
    ...     df.select(
    ...         add_calendar_days=pl.col("dt").dt.offset_by(
    ...             pl.format("{}d", pl.col("add"))
    ...         ),
    ...         add_calendar_months=pl.col("dt").dt.offset_by(
    ...             pl.format("{}mo", pl.col("add"))
    ...         ),
    ...         add_calendar_years=pl.col("dt").dt.offset_by(
    ...             pl.format("{}y", pl.col("add"))
    ...         ),
    ...     )
    ...
    shape: (2, 3)
    ┌─────────────────────┬─────────────────────┬─────────────────────┐
    │ add_calendar_days   ┆ add_calendar_months ┆ add_calendar_years  │
    │ ---                 ┆ ---                 ┆ ---                 │
    │ datetime[μs]        ┆ datetime[μs]        ┆ datetime[μs]        │
    ╞═════════════════════╪═════════════════════╪═════════════════════╡
    │ 2022-01-02 00:00:00 ┆ 2022-02-01 00:00:00 ┆ 2023-01-01 00:00:00 │
    │ 2022-01-04 00:00:00 ┆ 2022-03-02 00:00:00 ┆ 2024-01-02 00:00:00 │
    └─────────────────────┴─────────────────────┴─────────────────────┘

    """  # noqa: W505
    if hours is not None:
        hours = parse_as_expression(hours)
    if minutes is not None:
        minutes = parse_as_expression(minutes)
    if seconds is not None:
        seconds = parse_as_expression(seconds)
    if milliseconds is not None:
        milliseconds = parse_as_expression(milliseconds)
    if microseconds is not None:
        microseconds = parse_as_expression(microseconds)
    if nanoseconds is not None:
        nanoseconds = parse_as_expression(nanoseconds)
    if days is not None:
        days = parse_as_expression(days)
    if weeks is not None:
        weeks = parse_as_expression(weeks)

    return wrap_expr(
        plr.duration(
            days,
            seconds,
            nanoseconds,
            microseconds,
            milliseconds,
            minutes,
            hours,
            weeks,
        )
    )
