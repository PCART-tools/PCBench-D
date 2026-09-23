@torch.no_grad()
def fwd_only(
    fn: Callable[..., Any],
    args: Sequence[Any],
    *,
    run_functional_passes: bool = True,
    get_decomp_fn: Optional[Callable[..., Any]] = None,
) -> torch.fx.GraphModule:
    """Build a normalized inference graph, for use with fx_to_pattern"""
    # TODO - look into using aot autograd, asserting no mutating ops here
    with enable_python_dispatcher():
        decompositions = (
            get_decomp_fn() if get_decomp_fn is not None else select_decomp_table()
        )
        gm = make_fx(fn, decompositions, tracing_mode="real")(*args)

    from .fx_passes.post_grad import remove_noop_ops

    if run_functional_passes:
        remove_noop_ops(gm.graph)
        gm.graph.eliminate_dead_code()

    gm.recompile()
    return gm
