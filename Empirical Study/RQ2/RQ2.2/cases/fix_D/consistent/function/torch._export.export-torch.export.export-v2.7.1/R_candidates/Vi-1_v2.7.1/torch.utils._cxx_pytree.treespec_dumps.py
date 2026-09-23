def treespec_dumps(treespec: TreeSpec, protocol: Optional[int] = None) -> str:
    """Serialize a treespec to a JSON string."""
    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"treespec_dumps(treespec): Expected `treespec` to be instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )

    dummy_tree = tree_unflatten([0] * treespec.num_leaves, treespec)
    orig_treespec = python_pytree.tree_structure(dummy_tree)
    return python_pytree.treespec_dumps(orig_treespec, protocol=protocol)
