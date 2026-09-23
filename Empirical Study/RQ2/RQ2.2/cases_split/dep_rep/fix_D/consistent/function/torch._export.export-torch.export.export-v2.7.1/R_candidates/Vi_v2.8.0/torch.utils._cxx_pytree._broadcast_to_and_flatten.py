def _broadcast_to_and_flatten(
    tree: PyTree,
    treespec: TreeSpec,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> Optional[list[Any]]:
    assert _is_pytreespec_instance(treespec)
    full_tree = tree_unflatten([0] * treespec.num_leaves, treespec)
    try:
        return broadcast_prefix(tree, full_tree, is_leaf=is_leaf)
    except ValueError:
        return None
