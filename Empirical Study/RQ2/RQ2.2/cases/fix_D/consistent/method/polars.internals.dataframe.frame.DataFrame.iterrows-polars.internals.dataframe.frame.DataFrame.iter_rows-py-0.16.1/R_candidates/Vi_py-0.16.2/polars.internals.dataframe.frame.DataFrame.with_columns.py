    def with_columns(
        self,
        exprs: (
            str
            | PolarsExprType
            | PythonLiteral
            | pli.Series
            | Iterable[str | PolarsExprType | PythonLiteral | pli.Series]
            | None
        ) = None,
        **named_exprs: PolarsExprType | PythonLiteral | pli.Series | None,
    ) -> DataFrame:
        """
        Return a new DataFrame with the columns added (if new), or replaced.

        Notes
        -----
        Creating a new DataFrame using this method does not create a new copy
        of existing data.

        Parameters
        ----------
        exprs
            List of expressions that evaluate to columns.
        **named_exprs
            Named column expressions, provided as kwargs.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [0.5, 4, 10, 13],
        ...         "c": [True, True, False, True],
        ...     }
        ... )

        Passing in a single expression, adding (and naming) a new column:

        >>> df.with_columns((pl.col("a") ** 2).alias("a^2"))
        shape: (4, 4)
        ┌─────┬──────┬───────┬──────┐
        │ a   ┆ b    ┆ c     ┆ a^2  │
        │ --- ┆ ---  ┆ ---   ┆ ---  │
        │ i64 ┆ f64  ┆ bool  ┆ f64  │
        ╞═════╪══════╪═══════╪══════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 1.0  │
        │ 2   ┆ 4.0  ┆ true  ┆ 4.0  │
        │ 3   ┆ 10.0 ┆ false ┆ 9.0  │
        │ 4   ┆ 13.0 ┆ true  ┆ 16.0 │
        └─────┴──────┴───────┴──────┘

        We can also override an existing column by giving the expression
        a name that already exists:

        >>> df.with_columns((pl.col("a") ** 2).alias("c"))
        shape: (4, 3)
        ┌─────┬──────┬──────┐
        │ a   ┆ b    ┆ c    │
        │ --- ┆ ---  ┆ ---  │
        │ i64 ┆ f64  ┆ f64  │
        ╞═════╪══════╪══════╡
        │ 1   ┆ 0.5  ┆ 1.0  │
        │ 2   ┆ 4.0  ┆ 4.0  │
        │ 3   ┆ 10.0 ┆ 9.0  │
        │ 4   ┆ 13.0 ┆ 16.0 │
        └─────┴──────┴──────┘

        Multiple expressions can be passed in as both a list...

        >>> df.with_columns(
        ...     [
        ...         (pl.col("a") ** 2).alias("a^2"),
        ...         (pl.col("b") / 2).alias("b/2"),
        ...         (pl.col("c").is_not()).alias("not c"),
        ...     ]
        ... )
        shape: (4, 6)
        ┌─────┬──────┬───────┬──────┬──────┬───────┐
        │ a   ┆ b    ┆ c     ┆ a^2  ┆ b/2  ┆ not c │
        │ --- ┆ ---  ┆ ---   ┆ ---  ┆ ---  ┆ ---   │
        │ i64 ┆ f64  ┆ bool  ┆ f64  ┆ f64  ┆ bool  │
        ╞═════╪══════╪═══════╪══════╪══════╪═══════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 1.0  ┆ 0.25 ┆ false │
        │ 2   ┆ 4.0  ┆ true  ┆ 4.0  ┆ 2.0  ┆ false │
        │ 3   ┆ 10.0 ┆ false ┆ 9.0  ┆ 5.0  ┆ true  │
        │ 4   ┆ 13.0 ┆ true  ┆ 16.0 ┆ 6.5  ┆ false │
        └─────┴──────┴───────┴──────┴──────┴───────┘

        ...or via kwarg expressions:

        >>> df.with_columns(
        ...     ab=pl.col("a") * pl.col("b"),
        ...     not_c=pl.col("c").is_not(),
        ... )
        shape: (4, 5)
        ┌─────┬──────┬───────┬──────┬───────┐
        │ a   ┆ b    ┆ c     ┆ ab   ┆ not_c │
        │ --- ┆ ---  ┆ ---   ┆ ---  ┆ ---   │
        │ i64 ┆ f64  ┆ bool  ┆ f64  ┆ bool  │
        ╞═════╪══════╪═══════╪══════╪═══════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 0.5  ┆ false │
        │ 2   ┆ 4.0  ┆ true  ┆ 8.0  ┆ false │
        │ 3   ┆ 10.0 ┆ false ┆ 30.0 ┆ true  │
        │ 4   ┆ 13.0 ┆ true  ┆ 52.0 ┆ false │
        └─────┴──────┴───────┴──────┴───────┘

        Expressions with multiple outputs can be automatically instantiated as Structs
        by enabling the experimental setting ``Config.set_auto_structify(True)``:

        >>> with pl.Config() as cfg:
        ...     cfg.set_auto_structify(True)  # doctest: +IGNORE_RESULT
        ...     df.drop("c").with_columns(
        ...         diffs=pl.col(["a", "b"]).diff().suffix("_diff"),
        ...     )
        ...
        shape: (4, 3)
        ┌─────┬──────┬─────────────┐
        │ a   ┆ b    ┆ diffs       │
        │ --- ┆ ---  ┆ ---         │
        │ i64 ┆ f64  ┆ struct[2]   │
        ╞═════╪══════╪═════════════╡
        │ 1   ┆ 0.5  ┆ {null,null} │
        │ 2   ┆ 4.0  ┆ {1,3.5}     │
        │ 3   ┆ 10.0 ┆ {1,6.0}     │
        │ 4   ┆ 13.0 ┆ {1,3.0}     │
        └─────┴──────┴─────────────┘

        """
        return (
            self.lazy().with_columns(exprs, **named_exprs).collect(no_optimization=True)
        )
