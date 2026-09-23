def unsigned_integer() -> SelectorType:
    """
    Select all unsigned integer columns.

    See Also
    --------
    by_dtype : Select columns by dtype.
    float : Select all float columns.
    integer : Select all integer columns.
    numeric : Select all numeric columns.
    signed_integer : Select all signed integer columns.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "foo": [-123, -456],
    ...         "bar": [3456, 6789],
    ...         "baz": [7654, 4321],
    ...         "zap": ["ab", "cd"],
    ...     },
    ...     schema_overrides={"bar": pl.UInt32, "baz": pl.UInt64},
    ... )

    Select all unsigned integer columns:

    >>> df.select(cs.unsigned_integer())
    shape: (2, 2)
    ┌──────┬──────┐
    │ bar  ┆ baz  │
    │ ---  ┆ ---  │
    │ u32  ┆ u64  │
    ╞══════╪══════╡
    │ 3456 ┆ 7654 │
    │ 6789 ┆ 4321 │
    └──────┴──────┘

    Select all columns *except* for those that are unsigned integers:

    >>> df.select(~cs.unsigned_integer())
    shape: (2, 2)
    ┌──────┬─────┐
    │ foo  ┆ zap │
    │ ---  ┆ --- │
    │ i64  ┆ str │
    ╞══════╪═════╡
    │ -123 ┆ ab  │
    │ -456 ┆ cd  │
    └──────┴─────┘

    Select all integer columns (both signed and unsigned):

    >>> df.select(cs.integer())
    shape: (2, 3)
    ┌──────┬──────┬──────┐
    │ foo  ┆ bar  ┆ baz  │
    │ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ u32  ┆ u64  │
    ╞══════╪══════╪══════╡
    │ -123 ┆ 3456 ┆ 7654 │
    │ -456 ┆ 6789 ┆ 4321 │
    └──────┴──────┴──────┘

    """
    return _selector_proxy_(F.col(UNSIGNED_INTEGER_DTYPES), name="unsigned_integer")
