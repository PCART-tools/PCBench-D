def time_range(
    start: time | IntoExpr | None = None,
    end: time | IntoExpr | None = None,
    interval: str | timedelta = "1h",
    *,
    closed: ClosedInterval = "both",
    eager: bool = False,
    name: str | None = None,
) -> Series | Expr:
    """
    Generate a time range.

    Parameters
    ----------
    start
        Lower bound of the time range.
        If omitted, defaults to ``time(0,0,0,0)``.
    end
        Upper bound of the time range.
        If omitted, defaults to ``time(23,59,59,999999)``.
    interval
        Interval of the range periods, specified as a Python ``timedelta`` object
        or using the Polars duration string language (see "Notes" section below).
    closed : {'both', 'left', 'right', 'none'}
        Define which sides of the range are closed (inclusive).
    eager
        Evaluate immediately and return a ``Series``.
        If set to ``False`` (default), return an expression instead.
    name
        Name of the output column.

        .. deprecated:: 0.18.0
            This argument is deprecated. Use the ``alias`` method instead.

    Returns
    -------
    Expr or Series
        Column of data type `:class:Time`.

    Notes
    -----
    `interval` is created according to the following string language:

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

    Or combine them:
    "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds

    Suffix with `"_saturating"` to indicate that dates too large for
    their month should saturate at the largest date (e.g. 2022-02-29 -> 2022-02-28)
    instead of erroring.

    By "calendar day", we mean the corresponding time on the next day (which may
    not be 24 hours, due to daylight savings). Similarly for "calendar week",
    "calendar month", "calendar quarter", and "calendar year".

    See Also
    --------
    time_ranges : Create a column of time ranges.

    Examples
    --------
    >>> from datetime import time, timedelta
    >>> pl.time_range(
    ...     start=time(14, 0),
    ...     interval=timedelta(hours=3, minutes=15),
    ...     eager=True,
    ... )
    shape: (4,)
    Series: 'time' [time]
    [
        14:00:00
        17:15:00
        20:30:00
        23:45:00
    ]

    """
    if name is not None:
        issue_deprecation_warning(
            "the `name` argument is deprecated. Use the `alias` method instead.",
            version="0.18.0",
        )

    interval = parse_interval_argument(interval)
    for unit in ("y", "mo", "w", "d"):
        if unit in interval:
            raise ValueError(f"invalid interval unit for time_range: found {unit!r}")

    if start is None:
        start = time(0, 0, 0)
    if end is None:
        end = time(23, 59, 59, 999999)

    start_pyexpr = parse_as_expression(start)
    end_pyexpr = parse_as_expression(end)

    result = wrap_expr(plr.time_range(start_pyexpr, end_pyexpr, interval, closed))

    if name is not None:
        result = result.alias(name)

    if eager:
        return F.select(result).to_series()

    return result
