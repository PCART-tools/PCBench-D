def register_series_namespace(name: str) -> Callable[[type[NS]], type[NS]]:
    """
    Decorator for registering custom functionality with a polars Series.

    Parameters
    ----------
    name
        Name under which the functionality will be accessed.

    See Also
    --------
    register_expr_namespace: Register functionality on an Expr.
    register_dataframe_namespace: Register functionality on a DataFrame.
    register_lazyframe_namespace: Register functionality on a LazyFrame.

    Examples
    --------
    >>> @pl.api.register_series_namespace("math")
    ... class MathShortcuts:
    ...     def __init__(self, s: pl.Series):
    ...         self._s = s
    ...
    ...     def square(self) -> pl.Series:
    ...         return self._s * self._s
    ...
    ...     def cube(self) -> pl.Series:
    ...         return self._s * self._s * self._s
    ...
    >>>
    >>> s = pl.Series("n", [1.5, 31.0, 42.0, 64.5])
    >>> s.math.square().alias("s^2")
    shape: (4,)
    Series: 's^2' [f64]
    [
        2.25
        961.0
        1764.0
        4160.25
    ]
    >>> s = pl.Series("n", [1, 2, 3, 4, 5])
    >>> s.math.cube().alias("s^3")
    shape: (5,)
    Series: 's^3' [i64]
    [
        1
        8
        27
        64
        125
    ]

    """
    return _create_namespace(name, pl.Series)
