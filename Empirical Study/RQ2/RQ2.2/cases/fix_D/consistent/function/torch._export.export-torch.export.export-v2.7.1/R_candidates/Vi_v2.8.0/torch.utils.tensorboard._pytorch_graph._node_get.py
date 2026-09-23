def _node_get(node: torch._C.Node, key: str):
    """Get attributes of a node which is polymorphic over return type."""
    sel = node.kindOf(key)
    return getattr(node, sel)(key)
