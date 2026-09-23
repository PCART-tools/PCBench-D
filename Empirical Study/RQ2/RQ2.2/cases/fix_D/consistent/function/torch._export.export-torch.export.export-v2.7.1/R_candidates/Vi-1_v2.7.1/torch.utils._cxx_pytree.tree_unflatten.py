def tree_unflatten(leaves: Iterable[Any], treespec: TreeSpec) -> PyTree:
    """Reconstruct a pytree from the treespec and the leaves.

    The inverse of :func:`tree_flatten`.

    >>> tree = {"b": (2, [3, 4]), "a": 1, "c": None, "d": 5}
    >>> leaves, treespec = tree_flatten(tree)
    >>> tree == tree_unflatten(leaves, treespec)
    True

    Args:
        leaves (iterable): The list of leaves to use for reconstruction. The list must match the
            number of leaves of the treespec.
        treespec (TreeSpec): The treespec to reconstruct.

    Returns:
        The reconstructed pytree, containing the ``leaves`` placed in the structure described by
        ``treespec``.
    """
    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"tree_unflatten(leaves, treespec): Expected `treespec` to be instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )
    return optree.tree_unflatten(treespec, leaves)  # type: ignore[arg-type]
