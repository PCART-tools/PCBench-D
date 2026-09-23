    def collect(
        self,
        *,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        comm_subplan_elim: bool = True,
        comm_subexpr_elim: bool = True,
        cluster_with_columns: bool = True,
        no_optimization: bool = False,
        streaming: bool = False,
        background: bool = False,
        _eager: bool = False,
        **_kwargs: Any,
    ) -> DataFrame | InProcessQuery:
        """
        Materialize this LazyFrame into a DataFrame.

        By default, all query optimizations are enabled. Individual optimizations may
        be disabled by setting the corresponding parameter to `False`.

        Parameters
        ----------
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
        no_optimization
            Turn off (certain) optimizations.
        streaming
            Process the query in batches to handle larger-than-memory data.
            If set to `False` (default), the entire query is processed in a single
            batch.

            .. warning::
                Streaming mode is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

            .. note::
                Use :func:`explain` to see if Polars can process the query in streaming
                mode.
        background
            Run the query in the background and get a handle to the query.
            This handle can be used to fetch the result or cancel the query.

            .. warning::
                Background mode is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

        Returns
        -------
        DataFrame

        See Also
        --------
        fetch: Run the query on the first `n` rows only for debugging purposes.
        explain : Print the query plan that is evaluated with collect.
        profile : Collect the LazyFrame and time each node in the computation graph.
        polars.collect_all : Collect multiple LazyFrames at the same time.
        polars.Config.set_streaming_chunk_size : Set the size of streaming batches.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [1, 2, 3, 4, 5, 6],
        ...         "c": [6, 5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> lf.group_by("a").agg(pl.all().sum()).collect()  # doctest: +SKIP
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 4   ┆ 10  │
        │ b   ┆ 11  ┆ 10  │
        │ c   ┆ 6   ┆ 1   │
        └─────┴─────┴─────┘

        Collect in streaming mode

        >>> lf.group_by("a").agg(pl.all().sum()).collect(
        ...     streaming=True
        ... )  # doctest: +SKIP
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ str ┆ i64 ┆ i64 │
        ╞═════╪═════╪═════╡
        │ a   ┆ 4   ┆ 10  │
        │ b   ┆ 11  ┆ 10  │
        │ c   ┆ 6   ┆ 1   │
        └─────┴─────┴─────┘
        """
        new_streaming = _kwargs.get("new_streaming", False)

        if no_optimization or _eager:
            predicate_pushdown = False
            projection_pushdown = False
            slice_pushdown = False
            comm_subplan_elim = False
            comm_subexpr_elim = False
            cluster_with_columns = False

        if streaming:
            issue_unstable_warning("Streaming mode is considered unstable.")

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
            _eager,
            new_streaming,
        )

        if background:
            issue_unstable_warning("Background mode is considered unstable.")
            return InProcessQuery(ldf.collect_concurrently())

        # Only for testing purposes atm.
        callback = _kwargs.get("post_opt_callback")

        return wrap_df(ldf.collect(callback))
