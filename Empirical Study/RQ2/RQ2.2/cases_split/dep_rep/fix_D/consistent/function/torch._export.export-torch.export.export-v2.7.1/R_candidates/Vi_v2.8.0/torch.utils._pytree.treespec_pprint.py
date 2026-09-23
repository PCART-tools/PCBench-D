def treespec_pprint(treespec: TreeSpec) -> str:
    dummy_tree = tree_unflatten(
        [_DummyLeaf() for _ in range(treespec.num_leaves)],
        treespec,
    )
    return repr(dummy_tree)
