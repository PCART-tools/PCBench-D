def integer() -> SelectorType:
    """
    Select all integer columns.

    See Also
    --------
    by_dtype : Select columns by dtype.
    float : Select all float columns.
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
    ...         "zap": [0, 1],
    ...     }
    ... )

    Select all integer columns:

    >>> df.select(cs.integer())
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ zap │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 123 ┆ 0   │
    │ 456 ┆ 1   │
    └─────┴─────┘

    Select all columns *except* for those that are integer :

    >>> df.select(~cs.integer())
    shape: (2, 2)
    ┌─────┬─────┐
    │ foo ┆ baz │
    │ --- ┆ --- │
    │ str ┆ f64 │
    ╞═════╪═════╡
    │ x   ┆ 2.0 │
    │ y   ┆ 5.5 │
    └─────┴─────┘

    """
    return _selector_proxy_(F.col(INTEGER_DTYPES), name="integer")
