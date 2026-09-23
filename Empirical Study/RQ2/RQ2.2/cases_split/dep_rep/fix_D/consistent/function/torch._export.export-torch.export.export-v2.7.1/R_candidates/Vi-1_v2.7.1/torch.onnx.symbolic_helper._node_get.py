def _node_get(node: _C.Node, key: str):
    """Gets attributes of a node which is polymorphic over return type."""
    assert isinstance(node, _C.Node)
    sel = node.kindOf(key)
    return getattr(node, sel)(key)
