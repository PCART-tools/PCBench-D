    @substitute_in_graph(cxx_pytree.tree_iter, can_constant_fold_through=False)
    def tree_iter(
        tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> Iterable[Any]:
        stack = [tree]
        while stack:
            node = stack.pop()
            if tree_is_leaf(node, is_leaf=is_leaf):
                yield node
                continue

            children, *_ = optree.tree_flatten_one_level(
                node,
                is_leaf=is_leaf,
                none_is_leaf=True,
                namespace="torch",
            )
            stack.extend(reversed(children))
