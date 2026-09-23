def temporal() -> SelectorType:
    """
    Select all temporal columns.

    See Also
    --------
    by_dtype : Select all columns matching the given dtype(s).
    date : Select all date columns.
    datetime : Select all datetime columns, optionally filtering by time unit/zone.
    duration : Select all duration columns, optionally filtering by time unit.
    time : Select all time columns.

    Examples
    --------
    >>> from datetime import date, time
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "dt": [date(2021, 1, 1), date(2021, 1, 2)],
    ...         "tm": [time(12, 0, 0), time(20, 30, 45)],
    ...         "value": [1.2345, 2.3456],
    ...     }
    ... )

    Match all temporal columns:

    >>> df.select(cs.temporal())
    shape: (2, 2)
    ┌────────────┬──────────┐
    │ dt         ┆ tm       │
    │ ---        ┆ ---      │
    │ date       ┆ time     │
    ╞════════════╪══════════╡
    │ 2021-01-01 ┆ 12:00:00 │
    │ 2021-01-02 ┆ 20:30:45 │
    └────────────┴──────────┘

    Match all temporal columns *except* for time columns:

    >>> df.select(cs.temporal() - cs.time())
    shape: (2, 1)
    ┌────────────┐
    │ dt         │
    │ ---        │
    │ date       │
    ╞════════════╡
    │ 2021-01-01 │
    │ 2021-01-02 │
    └────────────┘

    Match all columns *except* for temporal columns:

    >>> df.select(~cs.temporal())
    shape: (2, 1)
    ┌────────┐
    │ value  │
    │ ---    │
    │ f64    │
    ╞════════╡
    │ 1.2345 │
    │ 2.3456 │
    └────────┘

    """
    return _selector_proxy_(F.col(TEMPORAL_DTYPES), name="temporal")
