def first() -> SelectorType:
    """
    Select the first column in the current scope.

    See Also
    --------
    all : Select all columns.
    last : Select the last column in the current scope.

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

    Select the first column:

    >>> df.select(cs.first())
    shape: (2, 1)
    ┌─────┐
    │ foo │
    │ --- │
    │ str │
    ╞═════╡
    │ x   │
    │ y   │
    └─────┘

    Select everything  *except* for the first column:

    >>> df.select(~cs.first())
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ bar ┆ baz ┆ zap │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ f64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 123 ┆ 2.0 ┆ 0   │
    │ 456 ┆ 5.5 ┆ 1   │
    └─────┴─────┴─────┘

    """
    return _selector_proxy_(F.first(), name="first")
