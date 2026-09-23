def reinplace_inplaceable_ops(graph: torch.fx.Graph) -> None:
    with enable_python_dispatcher():
        canonicalize_view_scatter_ops(graph)
        reinplace_inplaceable_ops_core(graph)
        decompose_generalized_scatter(graph)
