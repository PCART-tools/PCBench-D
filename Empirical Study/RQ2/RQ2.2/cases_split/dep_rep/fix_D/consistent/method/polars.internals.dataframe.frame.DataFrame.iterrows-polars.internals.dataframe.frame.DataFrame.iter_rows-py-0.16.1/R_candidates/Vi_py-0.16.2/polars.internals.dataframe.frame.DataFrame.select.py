    def select(
        self: DF,
        exprs: (
            str
            | PolarsExprType
            | PythonLiteral
            | pli.Series
            | Iterable[str | PolarsExprType | PythonLiteral | pli.Series]
            | None
        ) = None,
        **named_exprs: PolarsExprType | PythonLiteral | pli.Series | None,
    ) -> DF:
        """
        Select columns from this DataFrame.

        Parameters
        ----------
        exprs
            Column or columns to select.
        **named_exprs
            Named column expressions, provided as kwargs.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df.select("foo")
        shape: (3, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 1   │
        │ 2   │
        │ 3   │
        └─────┘

        >>> df.select(["foo", "bar"])
        shape: (3, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 6   │
        │ 2   ┆ 7   │
        │ 3   ┆ 8   │
        └─────┴─────┘

        >>> df.select(pl.col("foo") + 1)
        shape: (3, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 2   │
        │ 3   │
        │ 4   │
        └─────┘

        >>> df.select([pl.col("foo") + 1, pl.col("bar") + 1])
        shape: (3, 2)
        ┌─────┬─────┐
        │ foo ┆ bar │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 2   ┆ 7   │
        │ 3   ┆ 8   │
        │ 4   ┆ 9   │
        └─────┴─────┘

        >>> df.select(pl.when(pl.col("foo") > 2).then(10).otherwise(0))
        shape: (3, 1)
        ┌─────────┐
        │ literal │
        │ ---     │
        │ i32     │
        ╞═════════╡
        │ 0       │
        │ 0       │
        │ 10      │
        └─────────┘

        Expressions with multiple outputs can be automatically instantiated as Structs
        by enabling the experimental setting ``Config.set_auto_structify(True)``:

        >>> from polars.datatypes import INTEGER_DTYPES
        >>> with pl.Config() as cfg:
        ...     cfg.set_auto_structify(True)  # doctest: +IGNORE_RESULT
        ...     df.select(
        ...         is_odd=(pl.col(INTEGER_DTYPES) % 2).suffix("_is_odd"),
        ...     )
        ...
        shape: (3, 1)
        ┌───────────┐
        │ is_odd    │
        │ ---       │
        │ struct[2] │
        ╞═══════════╡
        │ {1,0}     │
        │ {0,1}     │
        │ {1,0}     │
        └───────────┘

        """
        return self._from_pydf(
            self.lazy().select(exprs, **named_exprs).collect(no_optimization=True)._df
        )
