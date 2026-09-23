    def _set_sink_optimizations(
        self,
        *,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        no_optimization: bool = False,
    ) -> PyLazyFrame:
        if no_optimization:
            predicate_pushdown = False
            projection_pushdown = False
            slice_pushdown = False

        return self._ldf.optimization_toggle(
            type_coercion,
            predicate_pushdown,
            projection_pushdown,
            simplify_expression,
            slice_pushdown,
            comm_subplan_elim=False,
            comm_subexpr_elim=False,
            cluster_with_columns=False,
            streaming=True,
            _eager=False,
            new_streaming=False,
        )
