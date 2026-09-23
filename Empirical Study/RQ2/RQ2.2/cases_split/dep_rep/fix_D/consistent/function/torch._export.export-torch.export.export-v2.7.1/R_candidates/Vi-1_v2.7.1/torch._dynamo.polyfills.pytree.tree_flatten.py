    @substitute_in_graph(  # type: ignore[arg-type]
        cxx_pytree.tree_flatten,
        # We need to disable constant folding here because we want the function to reference the
        # PyTreeSpec class defined above, not the one in the C++ module.
        can_constant_fold_through=False,
    )
    def tree_flatten(
        tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> tuple[list[Any], PyTreeSpec]:
        def helper(node: PyTree, leaves: list[Any]) -> PyTreeSpec:
            if tree_is_leaf(node, is_leaf=is_leaf):
                leaves.append(node)
                return _LEAF_SPEC

            (
                children,
                metadata,
                entries,
                unflatten_func,
            ) = optree.tree_flatten_one_level(
                node,
                is_leaf=is_leaf,
                none_is_leaf=True,
                namespace="torch",
            )

            # Recursively flatten the children
            subspecs = tuple(helper(child, leaves) for child in children)
            return PyTreeSpec(subspecs, type(node), metadata, entries, unflatten_func)  # type: ignore[arg-type]

        leaves: list[Any] = []
        treespec = helper(tree, leaves)
        return leaves, treespec
