def contains(substring: str | Collection[str]) -> SelectorType:
    """
    Select columns that contain the given literal substring(s).

    Parameters
    ----------
    substring
        Substring(s) that matching column names should contain.

    See Also
    --------
    matches : Select all columns that match the given regex pattern.
    ends_with : Select columns that end with the given substring(s).
    starts_with : Select columns that start with the given substring(s).

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

    Select columns that contain the substring 'ba':

    >>> df.select(cs.contains("ba"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ baz │
    │ --- ┆ --- │
    │ i64 ┆ f64 │
    ╞═════╪═════╡
    │ 123 ┆ 2.0 │
    │ 456 ┆ 5.5 │
    └─────┴─────┘

    Select columns that contain the substring 'ba' or the letter 'z':

    >>> df.select(cs.contains(("ba", "z")))
    shape: (2, 3)
    ┌─────┬─────┬───────┐
    │ bar ┆ baz ┆ zap   │
    │ --- ┆ --- ┆ ---   │
    │ i64 ┆ f64 ┆ bool  │
    ╞═════╪═════╪═══════╡
    │ 123 ┆ 2.0 ┆ false │
    │ 456 ┆ 5.5 ┆ true  │
    └─────┴─────┴───────┘

    Select all columns *except* for those that contain the substring 'ba':

    >>> df.select(~cs.contains("ba"))
    shape: (2, 2)
    ┌─────┬───────┐
    │ foo ┆ zap   │
    │ --- ┆ ---   │
    │ str ┆ bool  │
    ╞═════╪═══════╡
    │ x   ┆ false │
    │ y   ┆ true  │
    └─────┴───────┘

    """
    escaped_substring = _re_string(substring)
    raw_params = f"^.*{escaped_substring}.*$"

    return _selector_proxy_(
        F.col(raw_params),
        name="contains",
        parameters={"substring": escaped_substring},
    )
