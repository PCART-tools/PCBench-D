def _broadcast_to_and_flatten(
    tree: PyTree,
    treespec: TreeSpec,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> Optional[list[Any]]:
    assert isinstance(treespec, TreeSpec)

    if tree_is_leaf(tree, is_leaf=is_leaf):
        return [tree] * treespec.num_leaves
    if treespec.is_leaf():
        return None
    node_type = _get_node_type(tree)
    if node_type != treespec.type:
        return None

    flatten_fn = SUPPORTED_NODES[node_type].flatten_fn
    child_pytrees, ctx = flatten_fn(tree)

    # Check if the Node is different from the spec
    if len(child_pytrees) != treespec.num_children or ctx != treespec.context:
        return None

    # Recursively flatten the children
    result: list[Any] = []
    for child, child_spec in zip(child_pytrees, treespec.children_specs):
        flat = _broadcast_to_and_flatten(child, child_spec, is_leaf=is_leaf)
        if flat is not None:
            result += flat
        else:
            return None

    return result
