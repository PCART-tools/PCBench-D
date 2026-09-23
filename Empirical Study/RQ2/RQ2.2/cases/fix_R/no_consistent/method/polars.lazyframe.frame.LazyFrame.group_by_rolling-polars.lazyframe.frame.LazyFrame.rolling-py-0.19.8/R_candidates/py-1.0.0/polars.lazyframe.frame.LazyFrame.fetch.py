    @deprecate_function(
        "`LazyFrame.fetch` is deprecated; use `LazyFrame.collect` "
        "instead, in conjunction with a call to `head`.",
        version="1.0",
    )
    def fetch(
        self,
        n_rows: int = 500,
        *,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        no_optimization: bool = False,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        cluster_with_columns: bool = True,
        streaming: bool = False,
    ) -> DataFrame:
        """
        Collect a small number of rows for debugging purposes.

        .. deprecated:: 1.0
            Use :meth:`collect` instead, in conjunction with a call to :meth:`head`.`

        Notes
        -----
        This is similar to a :func:`collect` operation, but it overwrites the number of
        rows read by *every* scan operation. Be aware that `fetch` does not guarantee
        the final number of rows in the DataFrame. Filters, join operations and fewer
        rows being available in the scanned data will all influence the final number
        of rows (joins are especially susceptible to this, and may return no data
        at all if `n_rows` is too small as the join keys may not be present).

        Warnings
        --------
        This is strictly a utility function that can help to debug queries using a
        smaller number of rows, and should *not* be used in production code.
        """
        return self._fetch(
            n_rows=n_rows,
            type_coercion=type_coercion,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            simplify_expression=simplify_expression,
            no_optimization=no_optimization,
            slice_pushdown=slice_pushdown,
            comm_subplan_elim=comm_subplan_elim,
            comm_subexpr_elim=comm_subexpr_elim,
            cluster_with_columns=cluster_with_columns,
            streaming=streaming,
        )
