    def filter(
        self,
        *predicates: IntoExprColumn | Iterable[IntoExprColumn],
        **constraints: Any,
    ) -> Self:
        """
        Filter the expression based on one or more predicate expressions.

        The original order of the remaining elements is preserved.

        Elements where the filter does not evaluate to True are discarded, including
        nulls.

        Mostly useful in an aggregation context. If you want to filter on a DataFrame
        level, use `LazyFrame.filter`.

        Parameters
        ----------
        predicates
            Expression(s) that evaluates to a boolean Series.
        constraints
            Column filters; use `name = value` to filter columns by the supplied value.
            Each constraint will behave the same as `pl.col(name).eq(value)`, and
            will be implicitly joined with the other filter conditions using `&`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "group_col": ["g1", "g1", "g2"],
        ...         "b": [1, 2, 3],
        ...     }
        ... )
        >>> df.group_by("group_col").agg(
        ...     lt=pl.col("b").filter(pl.col("b") < 2).sum(),
        ...     gte=pl.col("b").filter(pl.col("b") >= 2).sum(),
        ... ).sort("group_col")
        shape: (2, 3)
        ┌───────────┬─────┬─────┐
        │ group_col ┆ lt  ┆ gte │
        │ ---       ┆ --- ┆ --- │
        │ str       ┆ i64 ┆ i64 │
        ╞═══════════╪═════╪═════╡
        │ g1        ┆ 1   ┆ 2   │
        │ g2        ┆ 0   ┆ 3   │
        └───────────┴─────┴─────┘

        Filter expressions can also take constraints as keyword arguments.

        >>> import polars.selectors as cs
        >>> df = pl.DataFrame(
        ...     {
        ...         "key": ["a", "a", "a", "a", "b", "b", "b", "b", "b"],
        ...         "n": [1, 2, 2, 3, 1, 3, 3, 2, 3],
        ...     },
        ... )
        >>> df.group_by("key").agg(
        ...     n_1=pl.col("n").filter(n=1).sum(),
        ...     n_2=pl.col("n").filter(n=2).sum(),
        ...     n_3=pl.col("n").filter(n=3).sum(),
        ... ).sort(by="key")
        shape: (2, 4)
        ┌─────┬─────┬─────┬─────┐
        │ key ┆ n_1 ┆ n_2 ┆ n_3 │
        │ --- ┆ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 4   ┆ 3   │
        │ b   ┆ 1   ┆ 2   ┆ 9   │
        └─────┴─────┴─────┴─────┘
        """
        if "predicate" in constraints:
            if isinstance(constraints["predicate"], pl.Expr):
                issue_deprecation_warning(
                    "`filter` no longer takes a 'predicate' parameter.\n"
                    "To silence this warning you should omit the keyword and pass "
                    "as a positional argument instead.",
                    version="0.19.17",
                )
                predicates = (*predicates, constraints.pop("predicate"))

        predicate = parse_predicates_constraints_as_expression(
            *predicates, **constraints
        )
        return self._from_pyexpr(self._pyexpr.filter(predicate))
