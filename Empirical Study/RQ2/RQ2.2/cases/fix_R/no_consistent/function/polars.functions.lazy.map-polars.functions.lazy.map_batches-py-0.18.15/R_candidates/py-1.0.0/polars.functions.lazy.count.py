def count(*columns: str) -> Expr:
    """
    Return the number of non-null values in the column.

    This function is syntactic sugar for `col(columns).count()`.

    Calling this function without any arguments returns the number of rows in the
    context. **This way of using the function is deprecated.** Please use :func:`len`
    instead.

    Parameters
    ----------
    *columns
        One or more column names.

    Returns
    -------
    Expr
        Expression of data type :class:`UInt32`.

    See Also
    --------
    Expr.count

    Examples
    --------
    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 2, None],
    ...         "b": [3, None, None],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.count("a"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 2   │
    └─────┘

    Return the number of non-null values in multiple columns.

    >>> df.select(pl.count("b", "c"))
    shape: (1, 2)
    ┌─────┬─────┐
    │ b   ┆ c   │
    │ --- ┆ --- │
    │ u32 ┆ u32 │
    ╞═════╪═════╡
    │ 1   ┆ 3   │
    └─────┴─────┘

    Return the number of rows in a context. **This way of using the function is
    deprecated.** Please use :func:`len` instead.

    >>> df.select(pl.count())  # doctest: +SKIP
    shape: (1, 1)
    ┌───────┐
    │ count │
    │ ---   │
    │ u32   │
    ╞═══════╡
    │ 3     │
    └───────┘
    """
    if not columns:
        issue_deprecation_warning(
            "`pl.count()` is deprecated. Please use `pl.len()` instead.",
            version="0.20.5",
        )
        return F.len().alias("count")
    return F.col(*columns).count()
