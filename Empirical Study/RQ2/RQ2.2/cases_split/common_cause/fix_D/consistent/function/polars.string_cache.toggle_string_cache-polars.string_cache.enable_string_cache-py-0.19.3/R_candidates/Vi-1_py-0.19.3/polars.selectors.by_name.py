def by_name(*names: str | Collection[str]) -> SelectorType:
    """
    Select all columns matching the given names.

    Parameters
    ----------
    *names
        One or more names of columns to select.

    See Also
    --------
    by_dtype : Select all columns matching the given dtypes.

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

    Select columns by name:

    >>> df.select(cs.by_name("foo", "bar"))
    shape: (2, 2)
    ┌─────┬─────┐
    │ foo ┆ bar │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ x   ┆ 123 │
    │ y   ┆ 456 │
    └─────┴─────┘

    Match all columns *except* for those given:

    >>> df.select(~cs.by_name("foo", "bar"))
    shape: (2, 2)
    ┌─────┬───────┐
    │ baz ┆ zap   │
    │ --- ┆ ---   │
    │ f64 ┆ bool  │
    ╞═════╪═══════╡
    │ 2.0 ┆ false │
    │ 5.5 ┆ true  │
    └─────┴───────┘

    """
    all_names = []
    for nm in names:
        if isinstance(nm, str):
            all_names.append(nm)
        elif isinstance(nm, Collection):
            for n in nm:
                if not isinstance(n, str):
                    raise TypeError(f"invalid name: {n!r}")
                all_names.append(n)
        else:
            TypeError(f"Invalid name: {nm!r}")

    return _selector_proxy_(
        F.col(*all_names), name="by_name", parameters={"*names": all_names}
    )
