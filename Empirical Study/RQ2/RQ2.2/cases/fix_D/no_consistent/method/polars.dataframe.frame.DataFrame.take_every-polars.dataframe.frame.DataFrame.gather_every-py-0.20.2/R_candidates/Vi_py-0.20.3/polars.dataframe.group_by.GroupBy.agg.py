    def agg(
        self,
        *aggs: IntoExpr | Iterable[IntoExpr],
        **named_aggs: IntoExpr,
    ) -> DataFrame:
        """
        Compute aggregations for each group of a group by operation.

        Parameters
        ----------
        *aggs
            Aggregations to compute for each group of the group by operation,
            specified as positional arguments.
            Accepts expression input. Strings are parsed as column names.
        **named_aggs
            Additional aggregations, specified as keyword arguments.
            The resulting columns will be renamed to the keyword used.

        Examples
        --------
        Compute the aggregation of the columns for each group.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "c"],
        ...         "b": [1, 2, 1, 3, 3],
        ...         "c": [5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> df.group_by("a").agg(pl.col("b"), pl.col("c"))  # doctest: +IGNORE_RESULT
        shape: (3, 3)
        ┌─────┬───────────┬───────────┐
        │ a   ┆ b         ┆ c         │
        │ --- ┆ ---       ┆ ---       │
        │ str ┆ list[i64] ┆ list[i64] │
        ╞═════╪═══════════╪═══════════╡
        │ a   ┆ [1, 1]    ┆ [5, 3]    │
        ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┤
        │ b   ┆ [2, 3]    ┆ [4, 2]    │
        ├╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┤
        │ c   ┆ [3]       ┆ [1]       │
        └─────┴───────────┴───────────┘

        Compute the sum of a column for each group.

        >>> df.group_by("a").agg(pl.col("b").sum())  # doctest: +IGNORE_RESULT
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 2   │
        │ b   ┆ 5   │
        │ c   ┆ 3   │
        └─────┴─────┘

        Compute multiple aggregates at once by passing a list of expressions.

        >>> df.group_by("a").agg([pl.sum("b"), pl.mean("c")])  # doctest: +IGNORE_RESULT
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ f64 │
        ╞═════╪═════╪═════╡
        │ c   ┆ 3   ┆ 1.0 │
        │ a   ┆ 2   ┆ 4.0 │
        │ b   ┆ 5   ┆ 3.0 │
        └─────┴─────┴─────┘

        Or use positional arguments to compute multiple aggregations in the same way.

        >>> df.group_by("a").agg(
        ...     pl.sum("b").name.suffix("_sum"),
        ...     (pl.col("c") ** 2).mean().name.suffix("_mean_squared"),
        ... )  # doctest: +IGNORE_RESULT
        shape: (3, 3)
        ┌─────┬───────┬────────────────┐
        │ a   ┆ b_sum ┆ c_mean_squared │
        │ --- ┆ ---   ┆ ---            │
        │ str ┆ i64   ┆ f64            │
        ╞═════╪═══════╪════════════════╡
        │ a   ┆ 2     ┆ 17.0           │
        │ c   ┆ 3     ┆ 1.0            │
        │ b   ┆ 5     ┆ 10.0           │
        └─────┴───────┴────────────────┘

        Use keyword arguments to easily name your expression inputs.

        >>> df.group_by("a").agg(
        ...     b_sum=pl.sum("b"),
        ...     c_mean_squared=(pl.col("c") ** 2).mean(),
        ... )  # doctest: +IGNORE_RESULT
        shape: (3, 3)
        ┌─────┬───────┬────────────────┐
        │ a   ┆ b_sum ┆ c_mean_squared │
        │ --- ┆ ---   ┆ ---            │
        │ str ┆ i64   ┆ f64            │
        ╞═════╪═══════╪════════════════╡
        │ a   ┆ 2     ┆ 17.0           │
        │ c   ┆ 3     ┆ 1.0            │
        │ b   ┆ 5     ┆ 10.0           │
        └─────┴───────┴────────────────┘

        """
        return (
            self.df.lazy()
            .group_by(self.by, *self.more_by, maintain_order=self.maintain_order)
            .agg(*aggs, **named_aggs)
            .collect(no_optimization=True)
        )
