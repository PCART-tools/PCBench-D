def tree_flatten(
    tree: PyTree,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> tuple[list[Any], TreeSpec]:
    """Flattens a pytree into a list of values and a TreeSpec that can be used
    to reconstruct the pytree.
    """

    def helper(node: PyTree, leaves: list[Any]) -> TreeSpec:
        if _is_leaf(node, is_leaf=is_leaf):
            leaves.append(node)
            return _LEAF_SPEC

        node_type = _get_node_type(node)
        flatten_fn = SUPPORTED_NODES[node_type].flatten_fn
        children, context = flatten_fn(node)

        # Recursively flatten the children
        subspecs = [helper(child, leaves) for child in children]
        return TreeSpec(node_type, context, subspecs)

    leaves: list[Any] = []
    treespec = helper(tree, leaves)
    return leaves, treespec
