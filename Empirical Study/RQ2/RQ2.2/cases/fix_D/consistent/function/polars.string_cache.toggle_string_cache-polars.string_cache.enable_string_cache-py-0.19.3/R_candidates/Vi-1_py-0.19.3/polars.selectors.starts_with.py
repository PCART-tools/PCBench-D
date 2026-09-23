def starts_with(*prefix: str) -> SelectorType:
    """
    Select columns that start with the given substring(s).

    Parameters
    ----------
    prefix
        Substring(s) that matching column names should start with.

    See Also
    --------
    contains : Select all columns that contain the given substring.
    ends_with : Select all columns that end with the given substring(s).
    matches : Select all columns that match the given regex pattern.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "foo": [1.0, 2.0],
    ...         "bar": [3.0, 4.0],
    ...         "baz": [5, 6],
    ...         "zap": [7, 8],
    ...     }
    ... )

    Match columns starting with a 'b':

    >>> df.select(cs.starts_with("b"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ baz │
    │ --- ┆ --- │
    │ f64 ┆ i64 │
    ╞═════╪═════╡
    │ 3.0 ┆ 5   │
    │ 4.0 ┆ 6   │
    └─────┴─────┘

    Match columns starting with *either* the letter 'b' or 'z':

    >>> df.select(cs.starts_with("b", "z"))
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ bar ┆ baz ┆ zap │
    │ --- ┆ --- ┆ --- │
    │ f64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 3.0 ┆ 5   ┆ 7   │
    │ 4.0 ┆ 6   ┆ 8   │
    └─────┴─────┴─────┘

    Match all columns *except* for those starting with 'b':

    >>> df.select(~cs.starts_with("b"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ foo ┆ zap │
    │ --- ┆ --- │
    │ f64 ┆ i64 │
    ╞═════╪═════╡
    │ 1.0 ┆ 7   │
    │ 2.0 ┆ 8   │
    └─────┴─────┘

    """
    escaped_prefix = _re_string(prefix)
    raw_params = f"^{escaped_prefix}.*$"

    return _selector_proxy_(
        F.col(raw_params),
        name="starts_with",
        parameters={"*prefix": prefix},
    )
