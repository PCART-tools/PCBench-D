@deprecate_nonkeyword_arguments(version="0.19.3")
def string(include_categorical: bool = False) -> SelectorType:  # noqa: FBT001
    """
    Select all Utf8 (and, optionally, Categorical) string columns .

    See Also
    --------
    binary : Select all binary columns.
    by_dtype : Select all columns matching the given dtype(s).
    categorical: Select all categorical columns.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> df = pl.DataFrame(
    ...     {
    ...         "w": ["xx", "yy", "xx", "yy", "xx"],
    ...         "x": [1, 2, 1, 4, -2],
    ...         "y": [3.0, 4.5, 1.0, 2.5, -2.0],
    ...         "z": ["a", "b", "a", "b", "b"],
    ...     },
    ... ).with_columns(
    ...     z=pl.col("z").cast(pl.Categorical).cat.set_ordering("lexical"),
    ... )

    Group by all string columns, sum the numeric columns, then sort by the string cols:

    >>> df.group_by(cs.string()).agg(cs.numeric().sum()).sort(by=cs.string())
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ w   ┆ x   ┆ y   │
    │ --- ┆ --- ┆ --- │
    │ str ┆ i64 ┆ f64 │
    ╞═════╪═════╪═════╡
    │ xx  ┆ 0   ┆ 2.0 │
    │ yy  ┆ 6   ┆ 7.0 │
    └─────┴─────┴─────┘

    Group by all string *and* categorical columns:

    >>> df.group_by(cs.string(include_categorical=True)).agg(cs.numeric().sum()).sort(
    ...     by=cs.string(include_categorical=True)
    ... )
    shape: (3, 4)
    ┌─────┬─────┬─────┬──────┐
    │ w   ┆ z   ┆ x   ┆ y    │
    │ --- ┆ --- ┆ --- ┆ ---  │
    │ str ┆ cat ┆ i64 ┆ f64  │
    ╞═════╪═════╪═════╪══════╡
    │ xx  ┆ a   ┆ 2   ┆ 4.0  │
    │ xx  ┆ b   ┆ -2  ┆ -2.0 │
    │ yy  ┆ b   ┆ 6   ┆ 7.0  │
    └─────┴─────┴─────┴──────┘

    """
    string_dtypes: list[PolarsDataType] = [Utf8]
    if include_categorical:
        string_dtypes.append(Categorical)

    return _selector_proxy_(
        F.col(string_dtypes),
        name="string",
        parameters={"include_categorical": include_categorical},
    )
