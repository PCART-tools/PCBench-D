@functools.lru_cache
def treespec_loads(serialized: str) -> TreeSpec:
    """Deserialize a treespec from a JSON string."""
    orig_treespec = python_pytree.treespec_loads(serialized)
    dummy_tree = python_pytree.tree_unflatten(
        [0] * orig_treespec.num_leaves,
        orig_treespec,
    )
    treespec = tree_structure(dummy_tree)
    return treespec
