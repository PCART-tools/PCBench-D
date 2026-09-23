    def explain(
        self,
        *,
        format: ExplainFormat = "plain",
        optimized: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        cluster_with_columns: bool = True,
        streaming: bool = False,
        tree_format: bool | None = None,
    ) -> str:
        """
        Create a string representation of the query plan.

        Different optimizations can be turned on or off.

        Parameters
        ----------
        format : {'plain', 'tree'}
            The format to use for displaying the logical plan.
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
        cluster_with_columns
            Combine sequential independent calls to with_columns
        streaming
            Run parts of the query in a streaming fashion (this is in an alpha state)

            .. warning::
                Streaming mode is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

        tree_format
            Format the output as a tree.

            .. deprecated:: 0.20.30
                Use `format="tree"` instead.

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
        if tree_format is not None:
            issue_deprecation_warning(
                "The `tree_format` parameter for `LazyFrame.explain` is deprecated"
                " Use the `format` parameter instead.",
                version="0.20.30",
            )
            if tree_format:
                format = "tree"

        if streaming:
            issue_unstable_warning("Streaming mode is considered unstable.")

        if optimized:
            ldf = self._ldf.optimization_toggle(
                type_coercion,
                predicate_pushdown,
                projection_pushdown,
                simplify_expression,
                slice_pushdown,
                comm_subplan_elim,
                comm_subexpr_elim,
                cluster_with_columns,
                streaming,
                _eager=False,
                new_streaming=False,
            )
            if format == "tree":
                return ldf.describe_optimized_plan_tree()
            else:
                return ldf.describe_optimized_plan()

        if format == "tree":
            return self._ldf.describe_plan_tree()
        else:
            return self._ldf.describe_plan()
