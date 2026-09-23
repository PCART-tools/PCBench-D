def register_lazyframe_namespace(name: str) -> Callable[[type[NS]], type[NS]]:
    """
    Decorator for registering custom functionality with a polars LazyFrame.

    Parameters
    ----------
    name
        Name under which the functionality will be accessed.

    See Also
    --------
    register_expr_namespace: Register functionality on an Expr.
    register_dataframe_namespace: Register functionality on a DataFrame.
    register_series_namespace: Register functionality on a Series.

    Examples
    --------
    >>> @pl.api.register_lazyframe_namespace("types")
    ... class DTypeOperations:
    ...     def __init__(self, ldf: pl.LazyFrame):
    ...         self._ldf = ldf
    ...
    ...     def split_by_column_dtypes(self) -> list[pl.LazyFrame]:
    ...         return [
    ...             self._ldf.select(pl.col(tp))
    ...             for tp in dict.fromkeys(self._ldf.dtypes)
    ...         ]
    ...
    ...     def upcast_integer_types(self) -> pl.LazyFrame:
    ...         return self._ldf.with_columns(
    ...             pl.col(tp).cast(pl.Int64) for tp in (pl.Int8, pl.Int16, pl.Int32)
    ...         )
    ...
    >>>
    >>> ldf = pl.DataFrame(
    ...     data={"a": [1, 2], "b": [3, 4], "c": [5.6, 6.7]},
    ...     schema=[("a", pl.Int16), ("b", pl.Int32), ("c", pl.Float32)],
    ... ).lazy()
    >>>
    >>> ldf.collect()
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    │ --- ┆ --- ┆ --- │
    │ i16 ┆ i32 ┆ f32 │
    ╞═════╪═════╪═════╡
    │ 1   ┆ 3   ┆ 5.6 │
    │ 2   ┆ 4   ┆ 6.7 │
    └─────┴─────┴─────┘
    >>> ldf.types.upcast_integer_types().collect()
    shape: (2, 3)
    ┌─────┬─────┬─────┐
    │ a   ┆ b   ┆ c   │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ f32 │
    ╞═════╪═════╪═════╡
    │ 1   ┆ 3   ┆ 5.6 │
    │ 2   ┆ 4   ┆ 6.7 │
    └─────┴─────┴─────┘
    >>>
    >>> ldf = pl.DataFrame(
    ...     data=[["xx", 2, 3, 4], ["xy", 4, 5, 6], ["yy", 5, 6, 7], ["yz", 6, 7, 8]],
    ...     schema=["a1", "a2", "b1", "b2"],
    ...     orient="row",
    ... ).lazy()
    >>>
    >>> ldf.collect()
    shape: (4, 4)
    ┌─────┬─────┬─────┬─────┐
    │ a1  ┆ a2  ┆ b1  ┆ b2  │
    │ --- ┆ --- ┆ --- ┆ --- │
    │ str ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╡
    │ xx  ┆ 2   ┆ 3   ┆ 4   │
    │ xy  ┆ 4   ┆ 5   ┆ 6   │
    │ yy  ┆ 5   ┆ 6   ┆ 7   │
    │ yz  ┆ 6   ┆ 7   ┆ 8   │
    └─────┴─────┴─────┴─────┘
    >>> pl.collect_all(ldf.types.split_by_column_dtypes())
    [shape: (4, 1)
    ┌─────┐
    │ a1  │
    │ --- │
    │ str │
    ╞═════╡
    │ xx  │
    │ xy  │
    │ yy  │
    │ yz  │
    └─────┘, shape: (4, 3)
    ┌─────┬─────┬─────┐
    │ a2  ┆ b1  ┆ b2  │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 2   ┆ 3   ┆ 4   │
    │ 4   ┆ 5   ┆ 6   │
    │ 5   ┆ 6   ┆ 7   │
    │ 6   ┆ 7   ┆ 8   │
    └─────┴─────┴─────┘]

    """
    return _create_namespace(name, pl.LazyFrame)
