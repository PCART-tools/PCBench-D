    def explain(
        self,
        *,
        optimized: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        streaming: bool = False,
    ) -> str:
        """
        Create a string representation of the query plan.

        Different optimizations can be turned on or off.

        Parameters
        ----------
        optimized
            Return an optimized query plan. Defaults to `True`.
            If this is set to `True` the subsequent
            optimization flags control which optimizations
            run.
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        slice_pushdown
            Slice pushdown optimization.
        comm_subplan_elim
            Will try to cache branching subplans that occur on self-joins or unions.
        comm_subexpr_elim
            Common subexpressions will be cached and reused.
        streaming
            Run parts of the query in a streaming fashion (this is in an alpha state)

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [1, 2, 3, 4, 5, 6],
        ...         "c": [6, 5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> lf.group_by("a", maintain_order=True).agg(pl.all().sum()).sort(
        ...     "a"
        ... ).explain()  # doctest: +SKIP
        """
        if optimized:
            ldf = self._ldf.optimization_toggle(
                type_coercion,
                predicate_pushdown,
                projection_pushdown,
                simplify_expression,
                slice_pushdown,
                comm_subplan_elim,
                comm_subexpr_elim,
                streaming,
                _eager=False,
            )
            return ldf.describe_optimized_plan()
        return self._ldf.describe_plan()
