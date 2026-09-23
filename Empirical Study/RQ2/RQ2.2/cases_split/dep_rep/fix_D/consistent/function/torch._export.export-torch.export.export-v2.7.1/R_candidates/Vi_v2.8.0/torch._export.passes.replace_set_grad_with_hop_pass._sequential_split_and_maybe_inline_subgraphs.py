def _sequential_split_and_maybe_inline_subgraphs(
    gm: torch.fx.GraphModule, graph_signature: Optional[ExportGraphSignature]
) -> tuple[torch.fx.GraphModule, Optional[ExportGraphSignature]]:
    """
    Helper function for replace_set_grad_with_hop_pass().
    Split the graph module into multiple subgraphs based on the set_grad_enabled nodes.
    For each subgraph, decides whether to construct a HOO subgraph, or inline the calls
    back into the parent graph module.
    """
    need_replacing = any(_is_set_grad_enabled_node(node) for node in gm.graph.nodes)
    if not need_replacing:
        return gm, graph_signature

    # sequential_split returns a new graph module that could have different output
    # args names. We need to fix the graph signature.
    new_gm = sequential_split(gm, _is_set_grad_enabled_node)

    def _maybe_inline_or_replace_with_hop(node: torch.fx.Node):
        if _is_set_grad_enabled_sub_mod(node, omit_if_same_with_ambient=True):
            _replace_with_hop(node)
        else:
            _remove_set_grad_and_inline(node)

    return _sequential_split_and_maybe_inline_subgraphs_helper(
        new_gm, graph_signature, _maybe_inline_or_replace_with_hop
    )
