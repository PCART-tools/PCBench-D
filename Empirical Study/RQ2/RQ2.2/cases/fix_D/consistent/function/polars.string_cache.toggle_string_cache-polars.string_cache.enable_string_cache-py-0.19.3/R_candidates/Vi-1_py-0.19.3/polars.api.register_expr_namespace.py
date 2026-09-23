def register_expr_namespace(name: str) -> Callable[[type[NS]], type[NS]]:
    """
    Decorator for registering custom functionality with a polars Expr.

    Parameters
    ----------
    name
        Name under which the functionality will be accessed.

    See Also
    --------
    register_dataframe_namespace: Register functionality on a DataFrame.
    register_lazyframe_namespace: Register functionality on a LazyFrame.
    register_series_namespace: Register functionality on a Series.

    Examples
    --------
    >>> @pl.api.register_expr_namespace("pow_n")
    ... class PowersOfN:
    ...     def __init__(self, expr: pl.Expr):
    ...         self._expr = expr
    ...
    ...     def next(self, p: int) -> pl.Expr:
    ...         return (p ** (self._expr.log(p).ceil()).cast(pl.Int64)).cast(pl.Int64)
    ...
    ...     def previous(self, p: int) -> pl.Expr:
    ...         return (p ** (self._expr.log(p).floor()).cast(pl.Int64)).cast(pl.Int64)
    ...
    ...     def nearest(self, p: int) -> pl.Expr:
    ...         return (p ** (self._expr.log(p)).round(0).cast(pl.Int64)).cast(pl.Int64)
    ...
    >>>
    >>> df = pl.DataFrame([1.4, 24.3, 55.0, 64.001], schema=["n"])
    >>> df.select(
    ...     pl.col("n"),
    ...     pl.col("n").pow_n.next(p=2).alias("next_pow2"),
    ...     pl.col("n").pow_n.previous(p=2).alias("prev_pow2"),
    ...     pl.col("n").pow_n.nearest(p=2).alias("nearest_pow2"),
    ... )
    shape: (4, 4)
    ┌────────┬───────────┬───────────┬──────────────┐
    │ n      ┆ next_pow2 ┆ prev_pow2 ┆ nearest_pow2 │
    │ ---    ┆ ---       ┆ ---       ┆ ---          │
    │ f64    ┆ i64       ┆ i64       ┆ i64          │
    ╞════════╪═══════════╪═══════════╪══════════════╡
    │ 1.4    ┆ 2         ┆ 1         ┆ 1            │
    │ 24.3   ┆ 32        ┆ 16        ┆ 32           │
    │ 55.0   ┆ 64        ┆ 32        ┆ 64           │
    │ 64.001 ┆ 128       ┆ 64        ┆ 64           │
    └────────┴───────────┴───────────┴──────────────┘

    """
    return _create_namespace(name, pl.Expr)
