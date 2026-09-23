def categorical() -> SelectorType:
    """
    Select all categorical columns.

    See Also
    --------
    by_dtype : Select all columns matching the given dtype(s).
    string : Select all string columns (optionally including categoricals).

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "foo": ["xx", "yy"],
    ...         "bar": [123, 456],
    ...         "baz": [2.0, 5.5],
    ...     },
    ...     schema_overrides={"foo": pl.Categorical},
    ... )

    Select all categorical columns:

    >>> df.select(cs.categorical())
    shape: (2, 1)
    ┌─────┐
    │ foo │
    │ --- │
    │ cat │
    ╞═════╡
    │ xx  │
    │ yy  │
    └─────┘

    Select all columns *except* for those that are categorical:

    >>> df.select(~cs.categorical())
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ baz │
    │ --- ┆ --- │
    │ i64 ┆ f64 │
    ╞═════╪═════╡
    │ 123 ┆ 2.0 │
    │ 456 ┆ 5.5 │
    └─────┴─────┘

    """
    return _selector_proxy_(F.col(Categorical), name="categorical")
