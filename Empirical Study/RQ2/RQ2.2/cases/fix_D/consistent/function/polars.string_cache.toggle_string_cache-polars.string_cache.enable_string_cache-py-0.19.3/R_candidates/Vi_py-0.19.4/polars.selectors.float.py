def float() -> SelectorType:
    """
    Select all float columns.

    See Also
    --------
    integer : Select all integer columns.
    numeric : Select all numeric columns.
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
    ...         "zap": [0.0, 1.0],
    ...     },
    ...     schema_overrides={"baz": pl.Float32, "zap": pl.Float64},
    ... )

    Select all float columns:

    >>> df.select(cs.float())
    shape: (2, 2)
    ┌─────┬─────┐
    │ baz ┆ zap │
    │ --- ┆ --- │
    │ f32 ┆ f64 │
    ╞═════╪═════╡
    │ 2.0 ┆ 0.0 │
    │ 5.5 ┆ 1.0 │
    └─────┴─────┘

    Select all columns *except* for those that are float:

    >>> df.select(~cs.float())
    shape: (2, 2)
    ┌─────┬─────┐
    │ foo ┆ bar │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ x   ┆ 123 │
    │ y   ┆ 456 │
    └─────┴─────┘

    """
    return _selector_proxy_(F.col(FLOAT_DTYPES), name="float")
