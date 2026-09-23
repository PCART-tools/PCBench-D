@torch.enable_grad()
def joint_fwd_bwd(fn: Callable[..., Any], args: Sequence[Any]) -> torch.fx.GraphModule:
    """Build a normalized training graph, for use with fx_to_pattern"""
    gm: Optional[torch.fx.GraphModule] = None

    def record_joint_graph(
        joint_graph: torch.fx.GraphModule, inputs: Sequence[Any], **kwargs: Any
    ) -> tuple[torch.fx.GraphModule, torch.fx.GraphModule]:
        nonlocal gm
        assert not gm
        gm = clone_graph(joint_graph)
        return default_partition(joint_graph, inputs, **kwargs)

    with torch._guards.tracing(None):
        aot_function(
            fn,
            lambda g, i: make_boxed_func(g),
            partition_fn=record_joint_graph,
            decompositions=select_decomp_table(),
            keep_inference_input_mutations=True,
            enable_log=False,
        )(*args)
    assert gm

    from .fx_passes.post_grad import remove_noop_ops

    remove_noop_ops(gm.graph)

    from .fx_passes.joint_graph import pointless_view

    matcher_pass = PatternMatcherPass()

    pattern = CallFunction(
        torch.ops.aten.view.default, KeywordArg("arg"), KeywordArg("size")
    )
    GraphPatternEntry(
        pattern=pattern, handler=pointless_view, extra_check=_return_true
    ).register(matcher_pass.patterns)
    matcher_pass.apply(gm.graph)

    # remove in/out specs
    gm.graph._codegen = torch.fx.graph.CodeGen()
    gm.graph.eliminate_dead_code()
    gm.recompile()
    return gm
