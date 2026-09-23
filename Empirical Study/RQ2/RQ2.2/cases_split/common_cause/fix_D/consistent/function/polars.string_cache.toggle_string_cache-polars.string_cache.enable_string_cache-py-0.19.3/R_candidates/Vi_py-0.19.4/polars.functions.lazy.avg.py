@deprecate_renamed_function("mean", version="0.18.12")
def avg(column: str | Series) -> Expr | float:
    """
    Alias for mean.

    .. deprecated:: 0.18.12
        Use ``mean`` instead.

    Examples
    --------
    >>> df = pl.DataFrame({"a": [1, 8, 3], "b": [4, 5, 2], "c": ["foo", "bar", "foo"]})
    >>> df.select(pl.avg("a"))  # doctest: +SKIP
    shape: (1, 1)
    ┌─────┐
    │ a   │
    │ --- │
    │ f64 │
    ╞═════╡
    │ 4.0 │
    └─────┘

    """
    return mean(column)
