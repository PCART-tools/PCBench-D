    @substitute_in_graph(  # type: ignore[arg-type]
        cxx_pytree.tree_unflatten,
        # We need to disable constant folding here because we want the function to reference the
        # PyTreeSpec class defined above, not the one in the C++ module.
        can_constant_fold_through=False,
    )
    def tree_unflatten(leaves: Iterable[Any], treespec: PyTreeSpec) -> PyTree:
        if not _is_pytreespec_instance(treespec):
            raise TypeError(
                f"tree_unflatten(leaves, treespec): Expected `treespec` to be instance of "
                f"PyTreeSpec but got item of type {type(treespec)}."
            )
        return treespec.unflatten(leaves)
