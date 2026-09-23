def collect_all(
    lazy_frames: Iterable[LazyFrame],
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
) -> list[DataFrame]:
    """
    Collect multiple LazyFrames at the same time.

    This runs all the computation graphs in parallel on the Polars threadpool.

    Parameters
    ----------
    lazy_frames
        A list of LazyFrames to collect.
    type_coercion
        Do type coercion optimization.
    predicate_pushdown
        Do predicate pushdown optimization.
    projection_pushdown
        Do projection pushdown optimization.
    simplify_expression
        Run simplify expressions optimization.
    no_optimization
        Turn off optimizations.
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

    Returns
    -------
    list of DataFrames
        The collected DataFrames, returned in the same order as the input LazyFrames.
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

    out = plr.collect_all(prepared)

    # wrap the pydataframes into dataframe
    result = [wrap_df(pydf) for pydf in out]

    return result
