def all() -> SelectorType:
    """
    Select all columns.

    See Also
    --------
    first : Select the first column in the current scope.
    last : Select the last column in the current scope.

    Examples
    --------
    >>> from datetime import date
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "dt": [date(1999, 12, 31), date(2024, 1, 1)],
    ...         "value": [1_234_500, 5_000_555],
    ...     },
    ...     schema_overrides={"value": pl.Int32},
    ... )

    Select all columns, casting them to string:

    >>> df.select(cs.all().cast(pl.Utf8))
    shape: (2, 2)
    ┌────────────┬─────────┐
    │ dt         ┆ value   │
    │ ---        ┆ ---     │
    │ str        ┆ str     │
    ╞════════════╪═════════╡
    │ 1999-12-31 ┆ 1234500 │
    │ 2024-01-01 ┆ 5000555 │
    └────────────┴─────────┘

    Select all columns *except* for those matching the given dtypes:

    >>> df.select(cs.all() - cs.numeric())
    shape: (2, 1)
    ┌────────────┐
    │ dt         │
    │ ---        │
    │ date       │
    ╞════════════╡
    │ 1999-12-31 │
    │ 2024-01-01 │
    └────────────┘

    """
    return _selector_proxy_(F.all(), name="all")
