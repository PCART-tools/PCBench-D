def _has_conv_bias_filter(
    match: "InternalMatch",
    original_graph: Graph,
    pattern_graph: Graph,
) -> bool:
    """
    Match filter for the subgraph rewriter that returns True if the conv node in
    the original graph has bias.
    """
    for n in match.nodes_map.values():
        if _is_conv_or_conv_transpose_node(n):
            return len(n.args) > 2 and n.args[2] is not None
    raise ValueError("Could not find conv node in matched conv + bn pattern")
