    @substitute_in_graph(cxx_pytree.tree_map, can_constant_fold_through=True)
    def tree_map(
        func: Callable[..., Any],
        tree: PyTree,
        *rests: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> PyTree:
        leaves, treespec = tree_flatten(tree, is_leaf=is_leaf)
        flat_args = [leaves] + [treespec.flatten_up_to(r) for r in rests]
        return treespec.unflatten(map(func, *flat_args))
