def _no_conv_bias_filter(
    match: "InternalMatch",
    original_graph: Graph,
    pattern_graph: Graph,
) -> bool:
    """
    Match filter for the subgraph rewriter that returns True if the conv node in
    the original graph does NOT have bias.
    """
    return not _has_conv_bias_filter(match, original_graph, pattern_graph)
