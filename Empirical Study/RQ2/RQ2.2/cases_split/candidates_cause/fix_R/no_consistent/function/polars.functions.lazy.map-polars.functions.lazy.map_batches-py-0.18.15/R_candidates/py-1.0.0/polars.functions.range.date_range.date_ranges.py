def date_ranges(
    start: date | datetime | IntoExprColumn,
    end: date | datetime | IntoExprColumn,
    interval: str | timedelta = "1d",
    *,
    closed: ClosedInterval = "both",
    eager: bool = False,
) -> Series | Expr:
    """
    Create a column of date ranges.

    Parameters
    ----------
    start
        Lower bound of the date range.
    end
        Upper bound of the date range.
    interval
        Interval of the range periods, specified as a Python `timedelta` object
        or using the Polars duration string language (see "Notes" section below).
        Must consist of full days.
    closed : {'both', 'left', 'right', 'none'}
        Define which sides of the range are closed (inclusive).
    eager
        Evaluate immediately and return a `Series`.
        If set to `False` (default), return an expression instead.

    Returns
    -------
    Expr or Series
        Column of data type `List(Date)`.

    See Also
    --------
    date_range
    datetime_ranges

    Notes
    -----
    `interval` is created according to the following string language:

    - 1d    (1 calendar day)
    - 1w    (1 calendar week)
    - 1mo   (1 calendar month)
    - 1q    (1 calendar quarter)
    - 1y    (1 calendar year)

    Or combine them:
    "1w2d" # 1 week, 2 days

    By "calendar day", we mean the corresponding time on the next day (which may
    not be 24 hours, due to daylight savings). Similarly for "calendar week",
    "calendar month", "calendar quarter", and "calendar year".

    Examples
    --------
    >>> from datetime import date
    >>> df = pl.DataFrame(
    ...     {
    ...         "start": [date(2022, 1, 1), date(2022, 1, 2)],
    ...         "end": date(2022, 1, 3),
    ...     }
    ... )
    >>> with pl.Config(fmt_str_lengths=50):
    ...     df.with_columns(date_range=pl.date_ranges("start", "end"))
    shape: (2, 3)
    ┌────────────┬────────────┬──────────────────────────────────────┐
    │ start      ┆ end        ┆ date_range                           │
    │ ---        ┆ ---        ┆ ---                                  │
    │ date       ┆ date       ┆ list[date]                           │
    ╞════════════╪════════════╪══════════════════════════════════════╡
    │ 2022-01-01 ┆ 2022-01-03 ┆ [2022-01-01, 2022-01-02, 2022-01-03] │
    │ 2022-01-02 ┆ 2022-01-03 ┆ [2022-01-02, 2022-01-03]             │
    └────────────┴────────────┴──────────────────────────────────────┘
    """
    interval = parse_interval_argument(interval)
    start_pyexpr = parse_into_expression(start)
    end_pyexpr = parse_into_expression(end)

    result = wrap_expr(plr.date_ranges(start_pyexpr, end_pyexpr, interval, closed))

    if eager:
        return F.select(result).to_series()

    return result
