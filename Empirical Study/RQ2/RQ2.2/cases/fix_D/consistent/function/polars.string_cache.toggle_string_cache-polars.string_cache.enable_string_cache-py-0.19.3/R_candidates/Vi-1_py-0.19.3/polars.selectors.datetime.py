def datetime(
    time_unit: TimeUnit | Collection[TimeUnit] | None = None,
    time_zone: (str | timezone | Collection[str | timezone | None] | None) = (
        "*",
        None,
    ),
) -> SelectorType:
    """
    Select all datetime columns, optionally filtering by time unit/zone.

    Parameters
    ----------
    time_unit
        One (or more) of the allowed timeunit precision strings, "ms", "us", and "ns".
        Omit to select columns with any valid timeunit.
    time_zone
        * One or more timezone strings, as defined in zoneinfo (to see valid options
          run ``import zoneinfo; zoneinfo.available_timezones()`` for a full list).
        * Set ``None`` to select Datetime columns that do not have a timezone.
        * Set "*" to select Datetime columns that have *any* timezone.

    See Also
    --------
    date : Select all date columns.
    duration : Select all duration columns, optionally filtering by time unit.
    temporal : Select all temporal columns.
    time : Select all time columns.

    Examples
    --------
    >>> from datetime import datetime, date
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "tstamp_tokyo": [
    ...             datetime(1999, 7, 21, 5, 20, 16, 987654),
    ...             datetime(2000, 5, 16, 6, 21, 21, 123465),
    ...         ],
    ...         "tstamp_utc": [
    ...             datetime(2023, 4, 10, 12, 14, 16, 999000),
    ...             datetime(2025, 8, 25, 14, 18, 22, 666000),
    ...         ],
    ...         "tstamp": [
    ...             datetime(2000, 11, 20, 18, 12, 16, 600000),
    ...             datetime(2020, 10, 30, 10, 20, 25, 123000),
    ...         ],
    ...         "dt": [date(1999, 12, 31), date(2010, 7, 5)],
    ...     },
    ...     schema_overrides={
    ...         "tstamp_tokyo": pl.Datetime("ns", "Asia/Tokyo"),
    ...         "tstamp_utc": pl.Datetime("us", "UTC"),
    ...     },
    ... )

    Select all datetime columns:

    >>> df.select(cs.datetime())
    shape: (2, 3)
    ┌────────────────────────────────┬─────────────────────────────┬─────────────────────────┐
    │ tstamp_tokyo                   ┆ tstamp_utc                  ┆ tstamp                  │
    │ ---                            ┆ ---                         ┆ ---                     │
    │ datetime[ns, Asia/Tokyo]       ┆ datetime[μs, UTC]           ┆ datetime[μs]            │
    ╞════════════════════════════════╪═════════════════════════════╪═════════════════════════╡
    │ 1999-07-21 05:20:16.987654 JST ┆ 2023-04-10 12:14:16.999 UTC ┆ 2000-11-20 18:12:16.600 │
    │ 2000-05-16 06:21:21.123465 JST ┆ 2025-08-25 14:18:22.666 UTC ┆ 2020-10-30 10:20:25.123 │
    └────────────────────────────────┴─────────────────────────────┴─────────────────────────┘

    Select all datetime columns that have 'us' precision:

    >>> df.select(cs.datetime("us"))
    shape: (2, 2)
    ┌─────────────────────────────┬─────────────────────────┐
    │ tstamp_utc                  ┆ tstamp                  │
    │ ---                         ┆ ---                     │
    │ datetime[μs, UTC]           ┆ datetime[μs]            │
    ╞═════════════════════════════╪═════════════════════════╡
    │ 2023-04-10 12:14:16.999 UTC ┆ 2000-11-20 18:12:16.600 │
    │ 2025-08-25 14:18:22.666 UTC ┆ 2020-10-30 10:20:25.123 │
    └─────────────────────────────┴─────────────────────────┘

    Select all datetime columns that have *any* timezone:

    >>> df.select(cs.datetime(time_zone="*"))
    shape: (2, 2)
    ┌────────────────────────────────┬─────────────────────────────┐
    │ tstamp_tokyo                   ┆ tstamp_utc                  │
    │ ---                            ┆ ---                         │
    │ datetime[ns, Asia/Tokyo]       ┆ datetime[μs, UTC]           │
    ╞════════════════════════════════╪═════════════════════════════╡
    │ 1999-07-21 05:20:16.987654 JST ┆ 2023-04-10 12:14:16.999 UTC │
    │ 2000-05-16 06:21:21.123465 JST ┆ 2025-08-25 14:18:22.666 UTC │
    └────────────────────────────────┴─────────────────────────────┘

    Select all datetime columns that have a *specific* timezone:

    >>> df.select(cs.datetime(time_zone="UTC"))
    shape: (2, 1)
    ┌─────────────────────────────┐
    │ tstamp_utc                  │
    │ ---                         │
    │ datetime[μs, UTC]           │
    ╞═════════════════════════════╡
    │ 2023-04-10 12:14:16.999 UTC │
    │ 2025-08-25 14:18:22.666 UTC │
    └─────────────────────────────┘

    Select all datetime columns that have NO timezone:

    >>> df.select(cs.datetime(time_zone=None))
    shape: (2, 1)
    ┌─────────────────────────┐
    │ tstamp                  │
    │ ---                     │
    │ datetime[μs]            │
    ╞═════════════════════════╡
    │ 2000-11-20 18:12:16.600 │
    │ 2020-10-30 10:20:25.123 │
    └─────────────────────────┘

    Select all columns *except* for datetime columns:

    >>> df.select(~cs.datetime())
    shape: (2, 1)
    ┌────────────┐
    │ dt         │
    │ ---        │
    │ date       │
    ╞════════════╡
    │ 1999-12-31 │
    │ 2010-07-05 │
    └────────────┘

    """  # noqa: W505
    if time_unit is None:
        time_unit = ["ms", "us", "ns"]
    else:
        time_unit = [time_unit] if isinstance(time_unit, str) else list(time_unit)

    if time_zone is None:
        time_zone = [None]
    elif time_zone:
        time_zone = (
            [time_zone] if isinstance(time_zone, (str, timezone)) else list(time_zone)
        )

    datetime_dtypes = [Datetime(tu, tz) for tu in time_unit for tz in time_zone]  # type: ignore[union-attr]

    return _selector_proxy_(
        F.col(datetime_dtypes),
        name="datetime",
        parameters={"time_unit": time_unit, "time_zone": time_zone},
    )
