def date_(
    year: Expr | str | int,
    month: Expr | str | int,
    day: Expr | str | int,
) -> Expr:
    """
    Create a Polars literal expression of type Date.

    Parameters
    ----------
    year
        column or literal.
    month
        column or literal, ranging from 1-12.
    day
        column or literal, ranging from 1-31.

    Returns
    -------
    Expr
        Expression of data type :class:`Date`.

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "month": [1, 2, 3],
    ...         "day": [4, 5, 6],
    ...     }
    ... )
    >>> df.with_columns(pl.date(2024, pl.col("month"), pl.col("day")))
    shape: (3, 3)
    ┌───────┬─────┬────────────┐
    │ month ┆ day ┆ date       │
    │ ---   ┆ --- ┆ ---        │
    │ i64   ┆ i64 ┆ date       │
    ╞═══════╪═════╪════════════╡
    │ 1     ┆ 4   ┆ 2024-01-04 │
    │ 2     ┆ 5   ┆ 2024-02-05 │
    │ 3     ┆ 6   ┆ 2024-03-06 │
    └───────┴─────┴────────────┘

    We can also use `pl.date` for filtering:

    >>> from datetime import date
    >>> df = pl.DataFrame(
    ...     {
    ...         "start": [date(2024, 1, 1), date(2024, 1, 1), date(2024, 1, 1)],
    ...         "end": [date(2024, 5, 1), date(2024, 7, 1), date(2024, 9, 1)],
    ...     }
    ... )
    >>> df.filter(pl.col("end") > pl.date(2024, 6, 1))
    shape: (2, 2)
    ┌────────────┬────────────┐
    │ start      ┆ end        │
    │ ---        ┆ ---        │
    │ date       ┆ date       │
    ╞════════════╪════════════╡
    │ 2024-01-01 ┆ 2024-07-01 │
    │ 2024-01-01 ┆ 2024-09-01 │
    └────────────┴────────────┘
    """
    return datetime_(year, month, day).cast(Date).alias("date")
