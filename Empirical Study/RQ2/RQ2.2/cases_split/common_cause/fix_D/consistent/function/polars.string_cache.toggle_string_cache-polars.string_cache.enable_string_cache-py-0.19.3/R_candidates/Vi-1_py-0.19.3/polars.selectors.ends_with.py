def ends_with(*suffix: str) -> SelectorType:
    """
    Select columns that end with the given substring(s).

    See Also
    --------
    contains : Select columns that contain the given literal substring(s).
    matches : Select all columns that match the given regex pattern.
    starts_with : Select columns that start with the given substring(s).

    Parameters
    ----------
    suffix
        Substring(s) that matching column names should end with.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "foo": ["x", "y"],
    ...         "bar": [123, 456],
    ...         "baz": [2.0, 5.5],
    ...         "zap": [False, True],
    ...     }
    ... )

    Select columns that end with the substring 'z':

    >>> df.select(cs.ends_with("z"))
    shape: (2, 1)
    ┌─────┐
    │ baz │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 2.0 │
    │ 5.5 │
    └─────┘

    Select columns that end with *either* the letter 'z' or 'r':

    >>> df.select(cs.ends_with("z", "r"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ baz │
    │ --- ┆ --- │
    │ i64 ┆ f64 │
    ╞═════╪═════╡
    │ 123 ┆ 2.0 │
    │ 456 ┆ 5.5 │
    └─────┴─────┘

    Select all columns *except* for those that end with the substring 'z':

    >>> df.select(~cs.ends_with("z"))
    shape: (2, 3)
    ┌─────┬─────┬───────┐
    │ foo ┆ bar ┆ zap   │
    │ --- ┆ --- ┆ ---   │
    │ str ┆ i64 ┆ bool  │
    ╞═════╪═════╪═══════╡
    │ x   ┆ 123 ┆ false │
    │ y   ┆ 456 ┆ true  │
    └─────┴─────┴───────┘

    """
    escaped_suffix = _re_string(suffix)
    raw_params = f"^.*{escaped_suffix}$"

    return _selector_proxy_(
        F.col(raw_params),
        name="ends_with",
        parameters={"*suffix": escaped_suffix},
    )
