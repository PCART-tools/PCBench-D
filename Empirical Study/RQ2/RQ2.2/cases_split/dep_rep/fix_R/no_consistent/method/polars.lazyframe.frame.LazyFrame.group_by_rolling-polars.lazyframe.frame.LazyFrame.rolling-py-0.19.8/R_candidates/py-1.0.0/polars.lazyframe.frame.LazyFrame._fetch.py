    def _fetch(
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

        Do not confuse with `collect`; this function will frequently return
        incorrect data (see the warning for additional details).

        Parameters
        ----------
        n_rows
            Collect n_rows from the data sources.
        type_coercion
            Run type coercion optimization.
        predicate_pushdown
            Run predicate pushdown optimization.
        projection_pushdown
            Run projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        no_optimization
            Turn off optimizations.
        slice_pushdown
            Slice pushdown optimization
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

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [1, 2, 3, 4, 5, 6],
        ...         "c": [6, 5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> lf.group_by("a", maintain_order=True).agg(pl.all().sum())._fetch(2)
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 1   ┆ 6   │
        │ b   ┆ 2   ┆ 5   │
        └─────┴─────┴─────┘
        """
        if no_optimization:
            predicate_pushdown = False
            projection_pushdown = False
            slice_pushdown = False
            comm_subplan_elim = False
            comm_subexpr_elim = False
            cluster_with_columns = False

        if streaming:
            issue_unstable_warning("Streaming mode is considered unstable.")

        lf = self._ldf.optimization_toggle(
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
        return wrap_df(lf.fetch(n_rows))
