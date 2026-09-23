def arg_sort_by(
    exprs: IntoExpr | Iterable[IntoExpr],
    *more_exprs: IntoExpr,
    descending: bool | Sequence[bool] = False,
) -> Expr:
    """
    Return the row indices that would sort the columns.

    Parameters
    ----------
    exprs
        Column(s) to arg sort by. Accepts expression input. Strings are parsed as column
        names.
    *more_exprs
        Additional columns to arg sort by, specified as positional arguments.
    descending
        Sort in descending order. When sorting by multiple columns, can be specified
        per column by passing a sequence of booleans.

    Examples
    --------
    Pass a single column name to compute the arg sort by that column.

    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [0, 1, 1, 0],
    ...         "b": [3, 2, 3, 2],
    ...     }
    ... )
    >>> df.select(pl.arg_sort_by("a"))
    shape: (4, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 0   │
    │ 3   │
    │ 1   │
    │ 2   │
    └─────┘

    Compute the arg sort by multiple columns by either passing a list of columns, or by
    specifying each column as a positional argument.

    >>> df.select(pl.arg_sort_by(["a", "b"], descending=True))
    shape: (4, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ u32 │
    ╞═════╡
    │ 2   │
    │ 1   │
    │ 0   │
    │ 3   │
    └─────┘

    """
    exprs = parse_as_list_of_expressions(exprs, *more_exprs)

    if isinstance(descending, bool):
        descending = [descending] * len(exprs)
    elif len(exprs) != len(descending):
        raise ValueError(
            f"the length of `descending` ({len(descending)}) does not match the length of `exprs` ({len(exprs)})"
        )
    return wrap_expr(plr.arg_sort_by(exprs, descending))
