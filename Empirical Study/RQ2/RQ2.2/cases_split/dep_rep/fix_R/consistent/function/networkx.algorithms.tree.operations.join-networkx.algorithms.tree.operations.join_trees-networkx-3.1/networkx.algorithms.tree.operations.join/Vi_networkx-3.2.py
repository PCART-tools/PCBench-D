def join(rooted_trees, label_attribute=None):
    """A deprecated name for `join_trees`

    Returns a new rooted tree with a root node joined with the roots
    of each of the given rooted trees.

    .. deprecated:: 3.2

       `join` is deprecated in NetworkX v3.2 and will be removed in v3.4.
       It has been renamed join_trees with the same syntax/interface.

    """
    import warnings

    warnings.warn(
        "The function `join` is deprecated and is renamed `join_trees`.\n"
        "The ``join`` function itself will be removed in v3.4",
        DeprecationWarning,
        stacklevel=2,
    )

    return join_trees(rooted_trees, label_attribute=label_attribute)
