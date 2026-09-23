def tree_iter(
    tree: PyTree,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> Iterable[Any]:
    """Get an iterator over the leaves of a pytree."""
    if _is_leaf(tree, is_leaf=is_leaf):
        yield tree
    else:
        node_type = _get_node_type(tree)
        flatten_fn = SUPPORTED_NODES[node_type].flatten_fn
        child_pytrees, _ = flatten_fn(tree)

        # Recursively flatten the children
        for child in child_pytrees:
            yield from tree_iter(child, is_leaf=is_leaf)
