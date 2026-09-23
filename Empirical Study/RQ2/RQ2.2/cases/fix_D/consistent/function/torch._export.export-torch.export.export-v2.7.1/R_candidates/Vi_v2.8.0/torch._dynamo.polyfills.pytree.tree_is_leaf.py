    @substitute_in_graph(cxx_pytree.tree_is_leaf, can_constant_fold_through=True)
    def tree_is_leaf(
        tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> bool:
        if tree is None or (is_leaf is not None and is_leaf(tree)):
            return True
        if optree.register_pytree_node.get(type(tree), namespace="torch") is None:  # type: ignore[attr-defined]
            return True
        return False
