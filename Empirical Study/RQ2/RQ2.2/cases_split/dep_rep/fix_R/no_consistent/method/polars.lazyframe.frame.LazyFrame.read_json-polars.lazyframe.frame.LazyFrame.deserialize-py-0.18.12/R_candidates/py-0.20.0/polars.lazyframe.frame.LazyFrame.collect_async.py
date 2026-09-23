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
        streaming: bool = False,
    ) -> Awaitable[DataFrame] | _GeventDataFrameResult[DataFrame]:
        """
        Collect DataFrame asynchronously in thread pool.

        Collects into a DataFrame (like :func:`collect`), but instead of returning
        DataFrame directly, they are scheduled to be collected inside thread pool,
        while this method returns almost instantly.

        May be useful if you use gevent or asyncio and want to release control to other
        greenlets/tasks while LazyFrames are being collected.

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
        streaming
            Run parts of the query in a streaming fashion (this is in an alpha state)

        Notes
        -----
        In case of error `set_exception` is used on
        `asyncio.Future`/`gevent.event.AsyncResult` and will be reraised by them.

        Warnings
        --------
        This functionality is experimental and may change without it being considered a
        breaking change.

        See Also
        --------
        polars.collect_all : Collect multiple LazyFrames at the same time.
        polars.collect_all_async: Collect multiple LazyFrames at the same time lazily.

        Returns
        -------
        If `gevent=False` (default) then returns awaitable.

        If `gevent=True` then returns wrapper that has
        `.get(block=True, timeout=None)` method.

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
        ...
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

        if streaming:
            comm_subplan_elim = False

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

        result = _GeventDataFrameResult() if gevent else _AioDataFrameResult()
        ldf.collect_with_callback(result._callback)  # type: ignore[attr-defined]
        return result  # type: ignore[return-value]
