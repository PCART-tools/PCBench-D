    @substitute_in_graph(  # type: ignore[arg-type]
        cxx_pytree.tree_structure,
        # We need to disable constant folding here because we want the function to reference the
        # PyTreeSpec class defined above, not the one in the C++ module.
        can_constant_fold_through=False,
    )
    def tree_structure(
        tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> PyTreeSpec:
        return tree_flatten(tree, is_leaf=is_leaf)[1]  # type: ignore[return-value]
