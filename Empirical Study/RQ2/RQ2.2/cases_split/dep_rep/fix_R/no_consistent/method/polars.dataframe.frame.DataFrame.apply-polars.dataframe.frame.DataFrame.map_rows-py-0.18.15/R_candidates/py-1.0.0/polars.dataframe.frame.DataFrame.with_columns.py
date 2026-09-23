    def with_columns(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> DataFrame:
        """
        Add columns to this DataFrame.

        Added columns will replace existing columns with the same name.

        Parameters
        ----------
        *exprs
            Column(s) to add, specified as positional arguments.
            Accepts expression input. Strings are parsed as column names, other
            non-expression inputs are parsed as literals.
        **named_exprs
            Additional columns to add, specified as keyword arguments.
            The columns will be renamed to the keyword used.

        Returns
        -------
        DataFrame
            A new DataFrame with the columns added.

        Notes
        -----
        Creating a new DataFrame using this method does not create a new copy of
        existing data.

        Examples
        --------
        Pass an expression to add it as a new column.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 4],
        ...         "b": [0.5, 4, 10, 13],
        ...         "c": [True, True, False, True],
        ...     }
        ... )
        >>> df.with_columns((pl.col("a") ** 2).alias("a^2"))
        shape: (4, 4)
        ┌─────┬──────┬───────┬─────┐
        │ a   ┆ b    ┆ c     ┆ a^2 │
        │ --- ┆ ---  ┆ ---   ┆ --- │
        │ i64 ┆ f64  ┆ bool  ┆ i64 │
        ╞═════╪══════╪═══════╪═════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 1   │
        │ 2   ┆ 4.0  ┆ true  ┆ 4   │
        │ 3   ┆ 10.0 ┆ false ┆ 9   │
        │ 4   ┆ 13.0 ┆ true  ┆ 16  │
        └─────┴──────┴───────┴─────┘

        Added columns will replace existing columns with the same name.

        >>> df.with_columns(pl.col("a").cast(pl.Float64))
        shape: (4, 3)
        ┌─────┬──────┬───────┐
        │ a   ┆ b    ┆ c     │
        │ --- ┆ ---  ┆ ---   │
        │ f64 ┆ f64  ┆ bool  │
        ╞═════╪══════╪═══════╡
        │ 1.0 ┆ 0.5  ┆ true  │
        │ 2.0 ┆ 4.0  ┆ true  │
        │ 3.0 ┆ 10.0 ┆ false │
        │ 4.0 ┆ 13.0 ┆ true  │
        └─────┴──────┴───────┘

        Multiple columns can be added using positional arguments.

        >>> df.with_columns(
        ...     (pl.col("a") ** 2).alias("a^2"),
        ...     (pl.col("b") / 2).alias("b/2"),
        ...     (pl.col("c").not_()).alias("not c"),
        ... )
        shape: (4, 6)
        ┌─────┬──────┬───────┬─────┬──────┬───────┐
        │ a   ┆ b    ┆ c     ┆ a^2 ┆ b/2  ┆ not c │
        │ --- ┆ ---  ┆ ---   ┆ --- ┆ ---  ┆ ---   │
        │ i64 ┆ f64  ┆ bool  ┆ i64 ┆ f64  ┆ bool  │
        ╞═════╪══════╪═══════╪═════╪══════╪═══════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 1   ┆ 0.25 ┆ false │
        │ 2   ┆ 4.0  ┆ true  ┆ 4   ┆ 2.0  ┆ false │
        │ 3   ┆ 10.0 ┆ false ┆ 9   ┆ 5.0  ┆ true  │
        │ 4   ┆ 13.0 ┆ true  ┆ 16  ┆ 6.5  ┆ false │
        └─────┴──────┴───────┴─────┴──────┴───────┘

        Multiple columns can also be added by passing a list of expressions.

        >>> df.with_columns(
        ...     [
        ...         (pl.col("a") ** 2).alias("a^2"),
        ...         (pl.col("b") / 2).alias("b/2"),
        ...         (pl.col("c").not_()).alias("not c"),
        ...     ]
        ... )
        shape: (4, 6)
        ┌─────┬──────┬───────┬─────┬──────┬───────┐
        │ a   ┆ b    ┆ c     ┆ a^2 ┆ b/2  ┆ not c │
        │ --- ┆ ---  ┆ ---   ┆ --- ┆ ---  ┆ ---   │
        │ i64 ┆ f64  ┆ bool  ┆ i64 ┆ f64  ┆ bool  │
        ╞═════╪══════╪═══════╪═════╪══════╪═══════╡
        │ 1   ┆ 0.5  ┆ true  ┆ 1   ┆ 0.25 ┆ false │
        │ 2   ┆ 4.0  ┆ true  ┆ 4   ┆ 2.0  ┆ false │
        │ 3   ┆ 10.0 ┆ false ┆ 9   ┆ 5.0  ┆ true  │
        │ 4   ┆ 13.0 ┆ true  ┆ 16  ┆ 6.5  ┆ false │
        └─────┴──────┴───────┴─────┴──────┴───────┘

        Use keyword arguments to easily name your expression inputs.

        >>> df.with_columns(
        ...     ab=pl.col("a") * pl.col("b"),
        ...     not_c=pl.col("c").not_(),
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
        by enabling the setting `Config.set_auto_structify(True)`:

        >>> with pl.Config(auto_structify=True):
        ...     df.drop("c").with_columns(
        ...         diffs=pl.col(["a", "b"]).diff().name.suffix("_diff"),
        ...     )
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
        return self.lazy().with_columns(*exprs, **named_exprs).collect(_eager=True)
