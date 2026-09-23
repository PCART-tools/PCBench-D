def _replace_list_with_tuple(spec: pytree.TreeSpec) -> pytree.TreeSpec:
    def replace_list_with_tuple(x: Any) -> Any:
        if type(x) is list:
            return pytree.tree_map(
                replace_list_with_tuple,
                tuple(x),
                is_leaf=lambda x: type(x) is list,
            )
        return x

    dummy_leaf = _DummyLeaf()
    dummy_tree = pytree.tree_unflatten([dummy_leaf] * spec.num_leaves, spec)
    dummy_tree = pytree.tree_map(
        replace_list_with_tuple,
        dummy_tree,
        is_leaf=lambda x: type(x) is list,
    )
    return pytree.tree_structure(dummy_tree)
