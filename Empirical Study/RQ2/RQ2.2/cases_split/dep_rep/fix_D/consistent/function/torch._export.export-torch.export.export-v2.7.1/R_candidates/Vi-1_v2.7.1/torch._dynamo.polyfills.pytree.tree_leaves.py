    @substitute_in_graph(cxx_pytree.tree_leaves, can_constant_fold_through=True)
    def tree_leaves(
        tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> list[Any]:
        return list(tree_iter(tree, is_leaf=is_leaf))
