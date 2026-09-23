def register_dataframe_namespace(name: str) -> Callable[[type[NS]], type[NS]]:
    """
    Decorator for registering custom functionality with a polars DataFrame.

    Parameters
    ----------
    name
        Name under which the functionality will be accessed.

    See Also
    --------
    register_expr_namespace: Register functionality on an Expr.
    register_lazyframe_namespace: Register functionality on a LazyFrame.
    register_series_namespace: Register functionality on a Series.

    Examples
    --------
    >>> @pl.api.register_dataframe_namespace("split")
    ... class SplitFrame:
    ...     def __init__(self, df: pl.DataFrame):
    ...         self._df = df
    ...
    ...     def by_first_letter_of_column_names(self) -> list[pl.DataFrame]:
    ...         return [
    ...             self._df.select([col for col in self._df.columns if col[0] == f])
    ...             for f in dict.fromkeys(col[0] for col in self._df.columns)
    ...         ]
    ...
    ...     def by_first_letter_of_column_values(self, col: str) -> list[pl.DataFrame]:
    ...         return [
    ...             self._df.filter(pl.col(col).str.starts_with(c))
    ...             for c in sorted(
    ...                 set(df.select(pl.col(col).str.slice(0, 1)).to_series())
    ...             )
    ...         ]
    ...
    >>>
    >>> df = pl.DataFrame(
    ...     data=[["xx", 2, 3, 4], ["xy", 4, 5, 6], ["yy", 5, 6, 7], ["yz", 6, 7, 8]],
    ...     schema=["a1", "a2", "b1", "b2"],
    ...     orient="row",
    ... )
    >>> df
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
    >>> df.split.by_first_letter_of_column_names()
    [shape: (4, 2)
    ┌─────┬─────┐
    │ a1  ┆ a2  │
    │ --- ┆ --- │
    │ str ┆ i64 │
    ╞═════╪═════╡
    │ xx  ┆ 2   │
    │ xy  ┆ 4   │
    │ yy  ┆ 5   │
    │ yz  ┆ 6   │
    └─────┴─────┘,
    shape: (4, 2)
    ┌─────┬─────┐
    │ b1  ┆ b2  │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 3   ┆ 4   │
    │ 5   ┆ 6   │
    │ 6   ┆ 7   │
    │ 7   ┆ 8   │
    └─────┴─────┘]
    >>> df.split.by_first_letter_of_column_values("a1")
    [shape: (2, 4)
    ┌─────┬─────┬─────┬─────┐
    │ a1  ┆ a2  ┆ b1  ┆ b2  │
    │ --- ┆ --- ┆ --- ┆ --- │
    │ str ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╡
    │ xx  ┆ 2   ┆ 3   ┆ 4   │
    │ xy  ┆ 4   ┆ 5   ┆ 6   │
    └─────┴─────┴─────┴─────┘, shape: (2, 4)
    ┌─────┬─────┬─────┬─────┐
    │ a1  ┆ a2  ┆ b1  ┆ b2  │
    │ --- ┆ --- ┆ --- ┆ --- │
    │ str ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╡
    │ yy  ┆ 5   ┆ 6   ┆ 7   │
    │ yz  ┆ 6   ┆ 7   ┆ 8   │
    └─────┴─────┴─────┴─────┘]

    """
    return _create_namespace(name, pl.DataFrame)
