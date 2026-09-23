def from_epoch(
    column: str | Expr | Series | Sequence[int], time_unit: EpochTimeUnit = "s"
) -> Expr | Series:
    """
    Utility function that parses an epoch timestamp (or Unix time) to Polars Date(time).

    Depending on the `time_unit` provided, this function will return a different dtype:

    - time_unit="d" returns pl.Date
    - time_unit="s" returns pl.Datetime["us"] (pl.Datetime's default)
    - time_unit="ms" returns pl.Datetime["ms"]
    - time_unit="us" returns pl.Datetime["us"]
    - time_unit="ns" returns pl.Datetime["ns"]

    Parameters
    ----------
    column
        Series or expression to parse integers to pl.Datetime.
    time_unit
        The unit of time of the timesteps since epoch time.

    Examples
    --------
    >>> df = pl.DataFrame({"timestamp": [1666683077, 1666683099]}).lazy()
    >>> df.select(pl.from_epoch(pl.col("timestamp"), time_unit="s")).collect()
    shape: (2, 1)
    ┌─────────────────────┐
    │ timestamp           │
    │ ---                 │
    │ datetime[μs]        │
    ╞═════════════════════╡
    │ 2022-10-25 07:31:17 │
    │ 2022-10-25 07:31:39 │
    └─────────────────────┘

    The function can also be used in an eager context by passing a Series.

    >>> s = pl.Series([12345, 12346])
    >>> pl.from_epoch(s, time_unit="d")
    shape: (2,)
    Series: '' [date]
    [
            2003-10-20
            2003-10-21
    ]

    """
    if isinstance(column, str):
        column = F.col(column)
    elif not isinstance(column, (pl.Series, pl.Expr)):
        column = pl.Series(column)  # Sequence input handled by Series constructor

    if time_unit == "d":
        return column.cast(Date)
    elif time_unit == "s":
        return (column.cast(Int64) * 1_000_000).cast(Datetime("us"))
    elif time_unit in DTYPE_TEMPORAL_UNITS:
        return column.cast(Datetime(time_unit))
    else:
        raise ValueError(
            f"'time_unit' must be one of {{'ns', 'us', 'ms', 's', 'd'}}, got {time_unit!r}"
        )
