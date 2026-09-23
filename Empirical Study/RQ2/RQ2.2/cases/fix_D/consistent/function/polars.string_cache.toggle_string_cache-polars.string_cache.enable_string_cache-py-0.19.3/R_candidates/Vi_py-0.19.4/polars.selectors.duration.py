def duration(
    time_unit: TimeUnit | Collection[TimeUnit] | None = None,
) -> SelectorType:
    """
    Select all duration columns, optionally filtering by time unit.

    Parameters
    ----------
    time_unit
        One (or more) of the allowed timeunit precision strings, "ms", "us", and "ns".
        Omit to select columns with any valid timeunit.

    See Also
    --------
    date : Select all date columns.
    datetime : Select all datetime columns, optionally filtering by time unit/zone.
    temporal : Select all temporal columns.
    time : Select all time columns.

    Examples
    --------
    >>> from datetime import date, timedelta
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "dt": [date(2022, 1, 31), date(2025, 7, 5)],
    ...         "td1": [
    ...             timedelta(days=1, milliseconds=123456),
    ...             timedelta(days=1, hours=23, microseconds=987000),
    ...         ],
    ...         "td2": [
    ...             timedelta(days=7, microseconds=456789),
    ...             timedelta(days=14, minutes=999, seconds=59),
    ...         ],
    ...         "td3": [
    ...             timedelta(weeks=4, days=-10, microseconds=999999),
    ...             timedelta(weeks=3, milliseconds=123456, microseconds=1),
    ...         ],
    ...     },
    ...     schema_overrides={
    ...         "td1": pl.Duration("ms"),
    ...         "td2": pl.Duration("us"),
    ...         "td3": pl.Duration("ns"),
    ...     },
    ... )

    Select all duration columns:

    >>> df.select(cs.duration())
    shape: (2, 3)
    ┌────────────────┬─────────────────┬────────────────────┐
    │ td1            ┆ td2             ┆ td3                │
    │ ---            ┆ ---             ┆ ---                │
    │ duration[ms]   ┆ duration[μs]    ┆ duration[ns]       │
    ╞════════════════╪═════════════════╪════════════════════╡
    │ 1d 2m 3s 456ms ┆ 7d 456789µs     ┆ 18d 999999µs       │
    │ 1d 23h 987ms   ┆ 14d 16h 39m 59s ┆ 21d 2m 3s 456001µs │
    └────────────────┴─────────────────┴────────────────────┘

    Select all duration columns that have 'ms' precision:

    >>> df.select(cs.duration("ms"))
    shape: (2, 1)
    ┌────────────────┐
    │ td1            │
    │ ---            │
    │ duration[ms]   │
    ╞════════════════╡
    │ 1d 2m 3s 456ms │
    │ 1d 23h 987ms   │
    └────────────────┘

    Select all duration columns that have 'ms' OR 'ns' precision:

    >>> df.select(cs.duration(["ms", "ns"]))
    shape: (2, 2)
    ┌────────────────┬────────────────────┐
    │ td1            ┆ td3                │
    │ ---            ┆ ---                │
    │ duration[ms]   ┆ duration[ns]       │
    ╞════════════════╪════════════════════╡
    │ 1d 2m 3s 456ms ┆ 18d 999999µs       │
    │ 1d 23h 987ms   ┆ 21d 2m 3s 456001µs │
    └────────────────┴────────────────────┘

    Select all columns *except* for duration columns:

    >>> df.select(~cs.duration())
    shape: (2, 1)
    ┌────────────┐
    │ dt         │
    │ ---        │
    │ date       │
    ╞════════════╡
    │ 2022-01-31 │
    │ 2025-07-05 │
    └────────────┘

    """
    if time_unit is None:
        time_unit = ["ms", "us", "ns"]
    else:
        time_unit = [time_unit] if isinstance(time_unit, str) else list(time_unit)

    duration_dtypes = [Duration(tu) for tu in time_unit]
    return _selector_proxy_(
        F.col(duration_dtypes),
        name="duration",
        parameters={"time_unit": time_unit},
    )
