def corr(
    a: IntoExpr,
    b: IntoExpr,
    *,
    method: CorrelationMethod = "pearson",
    ddof: int = 1,
    propagate_nans: bool = False,
) -> Expr:
    """
    Compute the Pearson's or Spearman rank correlation correlation between two columns.

    Parameters
    ----------
    a
        Column name or Expression.
    b
        Column name or Expression.
    ddof
        "Delta Degrees of Freedom": the divisor used in the calculation is N - ddof,
        where N represents the number of elements.
        By default ddof is 1.
    method : {'pearson', 'spearman'}
        Correlation method.
    propagate_nans
        If `True` any `NaN` encountered will lead to `NaN` in the output.
        Defaults to `False` where `NaN` are regarded as larger than any finite number
        and thus lead to the highest rank.

    Examples
    --------
    Pearson's correlation:

    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.corr("a", "b"))
    shape: (1, 1)
    ┌──────────┐
    │ a        │
    │ ---      │
    │ f64      │
    ╞══════════╡
    │ 0.544705 │
    └──────────┘

    Spearman rank correlation:

    >>> df = pl.DataFrame(
    ...     {
    ...         "a": [1, 8, 3],
    ...         "b": [4, 5, 2],
    ...         "c": ["foo", "bar", "foo"],
    ...     }
    ... )
    >>> df.select(pl.corr("a", "b", method="spearman"))
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 0.5 │
    └─────┘
    """
    a = parse_into_expression(a)
    b = parse_into_expression(b)

    if method == "pearson":
        return wrap_expr(plr.pearson_corr(a, b, ddof))
    elif method == "spearman":
        return wrap_expr(plr.spearman_rank_corr(a, b, ddof, propagate_nans))
    else:
        msg = f"method must be one of {{'pearson', 'spearman'}}, got {method!r}"
        raise ValueError(msg)
