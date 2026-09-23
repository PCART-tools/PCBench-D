def by_dtype(
    *dtypes: PolarsDataType | Collection[PolarsDataType],
) -> SelectorType:
    """
    Select all columns matching the given dtypes.

    See Also
    --------
    by_name : Select all columns matching the given names.

    Examples
    --------
    >>> from datetime import date
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "dt": [date(1999, 12, 31), date(2024, 1, 1), date(2010, 7, 5)],
    ...         "value": [1_234_500, 5_000_555, -4_500_000],
    ...         "other": ["foo", "bar", "foo"],
    ...     }
    ... )

    Select all columns with date or integer dtypes:

    >>> df.select(cs.by_dtype(pl.Date, pl.INTEGER_DTYPES))
    shape: (3, 2)
    ┌────────────┬──────────┐
    │ dt         ┆ value    │
    │ ---        ┆ ---      │
    │ date       ┆ i64      │
    ╞════════════╪══════════╡
    │ 1999-12-31 ┆ 1234500  │
    │ 2024-01-01 ┆ 5000555  │
    │ 2010-07-05 ┆ -4500000 │
    └────────────┴──────────┘

    Select all columns that are not of date or integer dtype:

    >>> df.select(~cs.by_dtype(pl.Date, pl.INTEGER_DTYPES))
    shape: (3, 1)
    ┌───────┐
    │ other │
    │ ---   │
    │ str   │
    ╞═══════╡
    │ foo   │
    │ bar   │
    │ foo   │
    └───────┘

    Group by string columns and sum the numeric columns:

    >>> df.group_by(cs.string()).agg(cs.numeric().sum()).sort(by="other")
    shape: (2, 2)
    ┌───────┬──────────┐
    │ other ┆ value    │
    │ ---   ┆ ---      │
    │ str   ┆ i64      │
    ╞═══════╪══════════╡
    │ bar   ┆ 5000555  │
    │ foo   ┆ -3265500 │
    └───────┴──────────┘

    """
    all_dtypes: list[PolarsDataType] = []
    for tp in dtypes:
        if is_polars_dtype(tp):
            all_dtypes.append(tp)  # type: ignore[arg-type]
        elif isinstance(tp, Collection):
            for t in tp:
                if not is_polars_dtype(t):
                    raise TypeError(f"invalid dtype: {t!r}")
                all_dtypes.append(t)
        else:
            raise TypeError(f"invalid dtype: {tp!r}")

    return _selector_proxy_(
        F.col(*all_dtypes), name="by_dtype", parameters={"dtypes": all_dtypes}
    )
