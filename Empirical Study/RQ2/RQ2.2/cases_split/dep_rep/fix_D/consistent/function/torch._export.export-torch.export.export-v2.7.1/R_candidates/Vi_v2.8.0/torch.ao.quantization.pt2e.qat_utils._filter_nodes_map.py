def _filter_nodes_map(nodes_map: dict[Node, Node]) -> dict[Node, Node]:
    """
    Return a filtered `nodes_map` returned from the subgraph rewriter.
    The filtered `nodes_map` will contain only nodes that are actually
    matched in the pattern, excluding None or placeholder nodes.
    """
    new_nodes_map: dict[Node, Node] = {}
    for pattern_node, graph_node in nodes_map.items():
        # bias can be None
        if graph_node is None:
            continue
        # skip pattern placeholder nodes
        if pattern_node.op == "placeholder":
            continue
        new_nodes_map[pattern_node] = graph_node
    return new_nodes_map
