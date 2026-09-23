def _is_leaf(tree: PyTree, is_leaf: Optional[Callable[[PyTree], bool]] = None) -> bool:
    return (is_leaf is not None and is_leaf(tree)) or _get_node_type(
        tree
    ) not in SUPPORTED_NODES
