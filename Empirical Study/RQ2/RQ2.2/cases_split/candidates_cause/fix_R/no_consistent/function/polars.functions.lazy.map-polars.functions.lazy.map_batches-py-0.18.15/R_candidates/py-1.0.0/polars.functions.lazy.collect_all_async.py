@unstable()
def collect_all_async(
    lazy_frames: Iterable[LazyFrame],
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
) -> Awaitable[list[DataFrame]] | _GeventDataFrameResult[list[DataFrame]]:
    """
    Collect multiple LazyFrames at the same time asynchronously in thread pool.

    .. warning::
        This functionality is considered **unstable**. It may be changed
        at any point without it being considered a breaking change.

    Collects into a list of DataFrame (like :func:`polars.collect_all`),
    but instead of returning them directly, they are scheduled to be collected
    inside thread pool, while this method returns almost instantly.

    May be useful if you use gevent or asyncio and want to release control to other
    greenlets/tasks while LazyFrames are being collected.

    Parameters
    ----------
    lazy_frames
        A list of LazyFrames to collect.
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
            Use :func:`explain` to see if Polars can process the query in streaming
            mode.

    See Also
    --------
    polars.collect_all : Collect multiple LazyFrames at the same time.
    LazyFrame.collect_async : To collect single frame.

    Notes
    -----
    In case of error `set_exception` is used on
    `asyncio.Future`/`gevent.event.AsyncResult` and will be reraised by them.

    Returns
    -------
    If `gevent=False` (default) then returns awaitable.

    If `gevent=True` then returns wrapper that has
    `.get(block=True, timeout=None)` method.
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
        comm_subplan_elim = False

    prepared = []

    for lf in lazy_frames:
        ldf = lf._ldf.optimization_toggle(
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
        prepared.append(ldf)

    result = _GeventDataFrameResult() if gevent else _AioDataFrameResult()
    plr.collect_all_with_callback(prepared, result._callback_all)  # type: ignore[attr-defined]
    return result  # type: ignore[return-value]
