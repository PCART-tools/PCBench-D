def _union(
    parent: EdgeOrNode,
    child: EdgeOrNode,
    shared_with_map: dict[EdgeOrNode, EdgeOrNode],
) -> None:
    """Merge the subtree for `child` with `parent`, the order is important here"""
    root_parent = _find_root_edge_or_node(parent, shared_with_map)
    root_child = _find_root_edge_or_node(child, shared_with_map)
    # union the two trees by pointing the root of child to root of parent
    shared_with_map[root_child] = root_parent
