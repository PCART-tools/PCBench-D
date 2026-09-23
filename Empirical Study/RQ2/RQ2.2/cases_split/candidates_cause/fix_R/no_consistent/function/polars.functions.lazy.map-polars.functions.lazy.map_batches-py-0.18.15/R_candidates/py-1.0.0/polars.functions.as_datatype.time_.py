def time_(
    hour: Expr | str | int | None = None,
    minute: Expr | str | int | None = None,
    second: Expr | str | int | None = None,
    microsecond: Expr | str | int | None = None,
) -> Expr:
    """
    Create a Polars literal expression of type Time.

    Parameters
    ----------
    hour
        column or literal, ranging from 0-23.
    minute
        column or literal, ranging from 0-59.
    second
        column or literal, ranging from 0-59.
    microsecond
        column or literal, ranging from 0-999999.

    Returns
    -------
    Expr
        Expression of data type :class:`Date`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "hour": [12, 13, 14],
    ...         "minute": [15, 30, 45],
    ...     }
    ... )

    >>> df.with_columns(pl.time(pl.col("hour"), pl.col("minute")))
    shape: (3, 3)
    ┌──────┬────────┬──────────┐
    │ hour ┆ minute ┆ time     │
    │ ---  ┆ ---    ┆ ---      │
    │ i64  ┆ i64    ┆ time     │
    ╞══════╪════════╪══════════╡
    │ 12   ┆ 15     ┆ 12:15:00 │
    │ 13   ┆ 30     ┆ 13:30:00 │
    │ 14   ┆ 45     ┆ 14:45:00 │
    └──────┴────────┴──────────┘
    """
    epoch_start = (1970, 1, 1)
    return (
        datetime_(*epoch_start, hour, minute, second, microsecond)
        .cast(Time)
        .alias("time")
    )
