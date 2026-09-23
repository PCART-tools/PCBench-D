def matches(pattern: str) -> SelectorType:
    """
    Select all columns that match the given regex pattern.

    See Also
    --------
    contains : Select all columns that contain the given substring.
    ends_with : Select all columns that end with the given substring(s).
    starts_with : Select all columns that start with the given substring(s).

    Parameters
    ----------
    pattern
        A valid regular expression pattern, compatible with the `regex crate
        <https://docs.rs/regex/latest/regex/>`_.

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

    Match column names containing an 'a', preceded by a character that is not 'z':

    >>> df.select(cs.matches("[^z]a"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ bar ┆ baz │
    │ --- ┆ --- │
    │ i64 ┆ f64 │
    ╞═════╪═════╡
    │ 123 ┆ 2.0 │
    │ 456 ┆ 5.5 │
    └─────┴─────┘

    Do not match column names ending in 'R' or 'z' (case-insensitively):

    >>> df.select(~cs.matches(r"(?i)R|z$"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ foo ┆ zap │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ x   ┆ 0   │
    │ y   ┆ 1   │
    └─────┴─────┘

    """
    if pattern == ".*":
        return all()
    else:
        if pattern.startswith(".*"):
            pattern = pattern[2:]
        elif pattern.endswith(".*"):
            pattern = pattern[:-2]

        pfx = "^.*" if not pattern.startswith("^") else ""
        sfx = ".*$" if not pattern.endswith("$") else ""
        raw_params = f"{pfx}{pattern}{sfx}"

        return _selector_proxy_(
            F.col(raw_params),
            name="matches",
            parameters={"pattern": pattern},
        )
