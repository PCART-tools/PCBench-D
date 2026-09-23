def arg_sort_by(
    exprs: IntoExpr | Iterable[IntoExpr],
    *more_exprs: IntoExpr,
    descending: bool | Sequence[bool] = False,
    nulls_last: bool | Sequence[bool] = False,
    multithreaded: bool = True,
    maintain_order: bool = False,
) -> Expr:
    """
    Return the row indices that would sort the column(s).

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
    nulls_last
        Place null values last.
    multithreaded
        Sort using multiple threads.
    maintain_order
        Whether the order should be maintained if elements are equal.

    See Also
    --------
    Expr.gather: Take values by index.
    Expr.rank : Get the rank of each row.

    Examples
    --------
    Pass a single column name to compute the arg sort by that column.

    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [0, 1, 1, 0],
    ...         "b": [3, 2, 3, 2],
    ...         "c": [1, 2, 3, 4],
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

    Use gather to apply the arg sort to other columns.

    >>> df.select(pl.col("c").gather(pl.arg_sort_by("a")))
    shape: (4, 1)
    ┌─────┐
    │ c   │
    │ --- │
    │ i64 │
    ╞═════╡
    │ 1   │
    │ 4   │
    │ 2   │
    │ 3   │
    └─────┘
    """
    exprs = parse_into_list_of_expressions(exprs, *more_exprs)
    descending = extend_bool(descending, len(exprs), "descending", "exprs")
    nulls_last = extend_bool(nulls_last, len(exprs), "nulls_last", "exprs")
    return wrap_expr(
        plr.arg_sort_by(exprs, descending, nulls_last, multithreaded, maintain_order)
    )
