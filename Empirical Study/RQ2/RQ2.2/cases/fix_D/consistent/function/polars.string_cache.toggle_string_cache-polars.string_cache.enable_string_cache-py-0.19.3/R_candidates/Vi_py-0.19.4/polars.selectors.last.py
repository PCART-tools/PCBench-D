def last() -> SelectorType:
    """
    Select the last column in the current scope.

    See Also
    --------
    all : Select all columns.
    first : Select the first column in the current scope.

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

    Select the last column:

    >>> df.select(cs.last())
    shape: (2, 1)
    ┌─────┐
    │ zap │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 0   │
    │ 1   │
    └─────┘

    Select everything  *except* for the last column:

    >> df.select(~cs.last())
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ foo ┆ bar ┆ baz │
    │ --- ┆ --- ┆ --- │
    │ str ┆ i64 ┆ f64 │
    ╞═════╪═════╪═════╡
    │ x   ┆ 123 ┆ 2.0 │
    │ y   ┆ 456 ┆ 5.5 │
    └─────┴─────┴─────┘

    """
    return _selector_proxy_(F.last(), name="last")
