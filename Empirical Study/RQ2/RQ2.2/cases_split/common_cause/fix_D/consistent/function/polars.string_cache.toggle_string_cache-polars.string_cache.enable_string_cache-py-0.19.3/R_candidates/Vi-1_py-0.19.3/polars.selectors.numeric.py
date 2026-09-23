def numeric() -> SelectorType:
    """
    Select all numeric columns.

    See Also
    --------
    by_dtype : Select columns by dtype.
    float : Select all float columns.
    integer : Select all integer columns.
    signed_integer : Select all signed integer columns.
    unsigned_integer : Select all unsigned integer columns.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "foo": ["x", "y"],
    ...         "bar": [123, 456],
    ...         "baz": [2.0, 5.5],
    ...         "zap": [0, 0],
    ...     },
    ...     schema_overrides={"bar": pl.Int16, "baz": pl.Float32, "zap": pl.UInt8},
    ... )

    Match all numeric columns:

    >>> df.select(cs.numeric())
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ bar ┆ baz ┆ zap │
    │ --- ┆ --- ┆ --- │
    │ i16 ┆ f32 ┆ u8  │
    ╞═════╪═════╪═════╡
    │ 123 ┆ 2.0 ┆ 0   │
    │ 456 ┆ 5.5 ┆ 0   │
    └─────┴─────┴─────┘

    Match all columns *except* for those that are numeric:

    >>> df.select(~cs.numeric())
    shape: (2, 1)
    ┌─────┐
    │ foo │
    │ --- │
    │ str │
    ╞═════╡
    │ x   │
    │ y   │
    └─────┘

    """
    return _selector_proxy_(F.col(NUMERIC_DTYPES), name="numeric")
