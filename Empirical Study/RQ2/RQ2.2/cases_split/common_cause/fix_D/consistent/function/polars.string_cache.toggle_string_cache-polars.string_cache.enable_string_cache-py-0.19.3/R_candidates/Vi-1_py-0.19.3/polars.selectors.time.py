def time() -> SelectorType:
    """
    Select all time columns.

    See Also
    --------
    date : Select all date columns.
    datetime : Select all datetime columns, optionally filtering by time unit/zone.
    duration : Select all duration columns, optionally filtering by time unit.
    temporal : Select all temporal columns.

    Examples
    --------
    >>> from datetime import date, datetime, time
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "dtm": [datetime(2001, 5, 7, 10, 25), datetime(2031, 12, 31, 0, 30)],
    ...         "dt": [date(1999, 12, 31), date(2024, 8, 9)],
    ...         "tm": [time(0, 0, 0), time(23, 59, 59)],
    ...     },
    ... )

    Select all time columns:

    >>> df.select(cs.time())
    shape: (2, 1)
    ┌──────────┐
    │ tm       │
    │ ---      │
    │ time     │
    ╞══════════╡
    │ 00:00:00 │
    │ 23:59:59 │
    └──────────┘

    Select all columns *except* for those that are times:

    >>> df.select(~cs.time())
    shape: (2, 2)
    ┌─────────────────────┬────────────┐
    │ dtm                 ┆ dt         │
    │ ---                 ┆ ---        │
    │ datetime[μs]        ┆ date       │
    ╞═════════════════════╪════════════╡
    │ 2001-05-07 10:25:00 ┆ 1999-12-31 │
    │ 2031-12-31 00:30:00 ┆ 2024-08-09 │
    └─────────────────────┴────────────┘

    """
    return _selector_proxy_(F.col(Time), name="time")
