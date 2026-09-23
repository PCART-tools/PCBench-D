def boolean() -> SelectorType:
    """
    Select all boolean columns.

    See Also
    --------
    by_dtype : Select all columns matching the given dtype(s).

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame({"n": range(1, 5)}).with_columns(n_even=pl.col("n") % 2 == 0)
    >>> df
    shape: (4, 2)
    ┌─────┬────────┐
    │ n   ┆ n_even │
    │ --- ┆ ---    │
    │ i64 ┆ bool   │
    ╞═════╪════════╡
    │ 1   ┆ false  │
    │ 2   ┆ true   │
    │ 3   ┆ false  │
    │ 4   ┆ true   │
    └─────┴────────┘

    Select and invert boolean columns:

    >>> df.with_columns(is_odd=cs.boolean().not_())
    shape: (4, 3)
    ┌─────┬────────┬────────┐
    │ n   ┆ n_even ┆ is_odd │
    │ --- ┆ ---    ┆ ---    │
    │ i64 ┆ bool   ┆ bool   │
    ╞═════╪════════╪════════╡
    │ 1   ┆ false  ┆ true   │
    │ 2   ┆ true   ┆ false  │
    │ 3   ┆ false  ┆ true   │
    │ 4   ┆ true   ┆ false  │
    └─────┴────────┴────────┘

    Select all columns *except* for those that are boolean:

    >>> df.select(~cs.boolean())
    shape: (4, 1)
    ┌─────┐
    │ n   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 2   │
    │ 3   │
    │ 4   │
    └─────┘

    """
    return _selector_proxy_(F.col(Boolean), name="boolean")
