def signed_integer() -> SelectorType:
    """
    Select all signed integer columns.

    See Also
    --------
    by_dtype : Select columns by dtype.
    float : Select all float columns.
    integer : Select all integer columns.
    numeric : Select all numeric columns.
    unsigned_integer : Select all unsigned integer columns.

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

    Select all signed integer columns:

    >>> df.select(cs.signed_integer())
    shape: (2, 1)
    ┌──────┐
    │ foo  │
    │ ---  │
    │ i64  │
    ╞══════╡
    │ -123 │
    │ -456 │
    └──────┘

    >>> df.select(~cs.signed_integer())
    shape: (2, 3)
    ┌──────┬──────┬─────┐
    │ bar  ┆ baz  ┆ zap │
    │ ---  ┆ ---  ┆ --- │
    │ u32  ┆ u64  ┆ str │
    ╞══════╪══════╪═════╡
    │ 3456 ┆ 7654 ┆ ab  │
    │ 6789 ┆ 4321 ┆ cd  │
    └──────┴──────┴─────┘

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
    return _selector_proxy_(F.col(SIGNED_INTEGER_DTYPES), name="signed_integer")
