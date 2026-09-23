def corr(
    a: str | Expr,
    b: str | Expr,
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

    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
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

    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
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
    if isinstance(a, str):
        a = F.col(a)
    if isinstance(b, str):
        b = F.col(b)

    if method == "pearson":
        return wrap_expr(plr.pearson_corr(a._pyexpr, b._pyexpr, ddof))
    elif method == "spearman":
        return wrap_expr(
            plr.spearman_rank_corr(a._pyexpr, b._pyexpr, ddof, propagate_nans)
        )
    else:
        raise ValueError(
            f"method must be one of {{'pearson', 'spearman'}}, got {method!r}"
        )
