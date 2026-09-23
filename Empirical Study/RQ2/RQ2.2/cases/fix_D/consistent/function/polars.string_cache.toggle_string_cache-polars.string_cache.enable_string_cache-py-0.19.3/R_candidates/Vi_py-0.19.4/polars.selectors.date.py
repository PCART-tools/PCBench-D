def date() -> SelectorType:
    """
    Select all date columns.

    See Also
    --------
    datetime : Select all datetime columns, optionally filtering by time unit/zone.
    duration : Select all duration columns, optionally filtering by time unit.
    temporal : Select all temporal columns.
    time : Select all time columns.

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

    Select all date columns:

    >>> df.select(cs.date())
    shape: (2, 1)
    ┌────────────┐
    │ dt         │
    │ ---        │
    │ date       │
    ╞════════════╡
    │ 1999-12-31 │
    │ 2024-08-09 │
    └────────────┘

    Select all columns *except* for those that are dates:

    >>> df.select(~cs.date())
    shape: (2, 2)
    ┌─────────────────────┬──────────┐
    │ dtm                 ┆ tm       │
    │ ---                 ┆ ---      │
    │ datetime[μs]        ┆ time     │
    ╞═════════════════════╪══════════╡
    │ 2001-05-07 10:25:00 ┆ 00:00:00 │
    │ 2031-12-31 00:30:00 ┆ 23:59:59 │
    └─────────────────────┴──────────┘

    """
    return _selector_proxy_(F.col(Date), name="date")
