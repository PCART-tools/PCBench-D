    def collect_async(
        self,
        *,
        gevent: bool = False,
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
    ) -> Awaitable[DataFrame] | _GeventDataFrameResult[DataFrame]:
        """
        Collect DataFrame asynchronously in thread pool.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Collects into a DataFrame (like :func:`collect`) but, instead of returning
        a DataFrame directly, it is scheduled to be collected inside a thread pool,
        while this method returns almost instantly.

        This can be useful if you use `gevent` or `asyncio` and want to release
        control to other greenlets/tasks while LazyFrames are being collected.

        Parameters
        ----------
        gevent
            Return wrapper to `gevent.event.AsyncResult` instead of Awaitable
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        no_optimization
            Turn off (certain) optimizations.
        slice_pushdown
            Slice pushdown optimization.
        comm_subplan_elim
            Will try to cache branching subplans that occur on self-joins or unions.
        comm_subexpr_elim
            Common subexpressions will be cached and reused.
        cluster_with_columns
            Combine sequential independent calls to with_columns
        streaming
            Process the query in batches to handle larger-than-memory data.
            If set to `False` (default), the entire query is processed in a single
            batch.

            .. warning::
                Streaming mode is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

            .. note::
                Use :func:`explain` to see if Polars can process the query in
                streaming mode.

        Returns
        -------
        If `gevent=False` (default) then returns an awaitable.

        If `gevent=True` then returns wrapper that has a
        `.get(block=True, timeout=None)` method.

        See Also
        --------
        polars.collect_all : Collect multiple LazyFrames at the same time.
        polars.collect_all_async : Collect multiple LazyFrames at the same time lazily.

        Notes
        -----
        In case of error `set_exception` is used on
        `asyncio.Future`/`gevent.event.AsyncResult` and will be reraised by them.

        Examples
        --------
        >>> import asyncio
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["a", "b", "a", "b", "b", "c"],
        ...         "b": [1, 2, 3, 4, 5, 6],
        ...         "c": [6, 5, 4, 3, 2, 1],
        ...     }
        ... )
        >>> async def main():
        ...     return await (
        ...         lf.group_by("a", maintain_order=True)
        ...         .agg(pl.all().sum())
        ...         .collect_async()
        ...     )
        >>> asyncio.run(main())
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
        if no_optimization:
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
            _eager=False,
            new_streaming=False,
        )

        result = _GeventDataFrameResult() if gevent else _AioDataFrameResult()
        ldf.collect_with_callback(result._callback)  # type: ignore[attr-defined]
        return result  # type: ignore[return-value]
