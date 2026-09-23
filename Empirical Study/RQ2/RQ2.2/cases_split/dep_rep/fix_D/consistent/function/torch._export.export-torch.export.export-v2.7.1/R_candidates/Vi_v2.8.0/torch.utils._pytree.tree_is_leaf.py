def tree_is_leaf(
    tree: PyTree,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> bool:
    """Check if a pytree is a leaf.

    >>> tree_is_leaf(1)
    True
    >>> tree_is_leaf(None)
    True
    >>> tree_is_leaf([1, 2, 3])
    False
    >>> tree_is_leaf((1, 2, 3), is_leaf=lambda x: isinstance(x, tuple))
    True
    >>> tree_is_leaf({'a': 1, 'b': 2, 'c': 3})
    False
    >>> tree_is_leaf({'a': 1, 'b': 2, 'c': None})
    False
    """
    if is_leaf is not None and is_leaf(tree):
        return True
    return _get_node_type(tree) not in SUPPORTED_NODES
