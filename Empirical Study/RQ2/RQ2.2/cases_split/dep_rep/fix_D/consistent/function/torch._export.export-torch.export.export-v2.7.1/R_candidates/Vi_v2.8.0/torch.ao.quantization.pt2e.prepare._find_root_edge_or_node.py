def _find_root_edge_or_node(
    edge_or_node: EdgeOrNode, shared_with_map: dict[EdgeOrNode, EdgeOrNode]
) -> EdgeOrNode:
    """Find the root node for the sharing tree
    Args:
        edge_or_node: edge/node that we want to find the root
        shared_with_map: each edge/node points to the parent, the root node will points to itself

    Returns:
        root edge/node
    """
    parent = shared_with_map[edge_or_node]
    if parent == edge_or_node:
        return edge_or_node
    root = _find_root_edge_or_node(parent, shared_with_map)
    # path compression
    shared_with_map[edge_or_node] = root
    return root
