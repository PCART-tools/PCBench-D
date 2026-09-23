def _sequential_split_and_maybe_inline_subgraphs(
    gm: torch.fx.GraphModule, graph_signature: Optional[ExportGraphSignature]
) -> tuple[torch.fx.GraphModule, Optional[ExportGraphSignature]]:
    """
    Helper function for replace_autocast_with_hop_pass().
    Split the graph module into multiple subgraphs based on the autocast nodes.
    For each subgraph, decides whether to construct a HOO subgraph, or inline the calls
    back into the parent graph module.
    Nodes between `_enter_autocast` and `_exit_autocast(_enter_autocast)` are considered
    as a subgraph.
    """
    need_replacing = any(_is_autocast_node(node) for node in gm.graph.nodes)
    if not need_replacing:
        return gm, graph_signature

    # split_autocast returns a new graph module that could have different output
    # args names. We need to fix the graph signature in `_sequential_split_and_maybe_inline_subgraphs_helper`.
    new_gm = _split_autocast(gm)

    def _maybe_inline_or_replace_with_hop(node: torch.fx.Node) -> None:
        if _is_autocast_sub_mod(node):
            _replace_with_hop(node)
        else:
            assert node.op == "call_module"
            assert isinstance(node.target, str)
            node_inline_(node)

    return _sequential_split_and_maybe_inline_subgraphs_helper(
        new_gm, graph_signature, _maybe_inline_or_replace_with_hop
    )
