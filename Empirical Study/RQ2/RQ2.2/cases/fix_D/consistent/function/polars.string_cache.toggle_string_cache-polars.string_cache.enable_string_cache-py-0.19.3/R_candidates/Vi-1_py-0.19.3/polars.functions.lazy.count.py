def count(column: str | Series | None = None) -> Expr | int:
    """
    Count the number of values in this column/context.

    .. warning::
        `null` is deemed a value in this context.

    Parameters
    ----------
    column
        If dtype is:

        * ``pl.Series`` : count the values in the series.
        * ``str`` : count the values in this column.
        * ``None`` : count the number of values in this context.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.count())
    shape: (1, 1)
    ┌───────┐
    │ count │
    │ ---   │
    │ u32   │
    ╞═══════╡
    │ 3     │
    └───────┘
    >>> df.group_by("c", maintain_order=True).agg(pl.count())
    shape: (2, 2)
    ┌─────┬───────┐
    │ c   ┆ count │
    │ --- ┆ ---   │
    │ str ┆ u32   │
    ╞═════╪═══════╡
    │ foo ┆ 2     │
    │ bar ┆ 1     │
    └─────┴───────┘

    """
    if column is None:
        return wrap_expr(plr.count())

    if isinstance(column, pl.Series):
        issue_deprecation_warning(
            "passing a Series to `count` is deprecated. Use `Series.len()` instead.",
            version="0.18.8",
        )
        return column.len()
    return F.col(column).count()
