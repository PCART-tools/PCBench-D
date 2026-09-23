def create_merge_tree(func, keys, token):
    """Create a task tree that merges all the keys with a reduction function.

    Parameters
    ----------
    func: callable
        Reduction function that accepts a single list of values to reduce.
    keys: iterable
        Keys to reduce from the source dask graph.
    token: object
        Included in each key of the returned dict.

    This creates a k-ary tree where k depends on the current level and is
    greater the further away a node is from the root node.  This reduces the
    total number of nodes (thereby reducing scheduler overhead), but still
    has beneficial properties of trees.

    For reasonable numbers of keys, N < 1e5, the total number of nodes in the
    tree is roughly ``N**0.78``.  For 1e5 < N < 2e5, is it roughly ``N**0.8``.
    """
    level = 0
    prev_width = len(keys)
    prev_keys = iter(keys)
    rv = {}
    while prev_width > 1:
        width = tree_width(prev_width)
        groups = tree_groups(prev_width, width)
        keys = [(token, level, i) for i in range(width)]
        rv.update((key, (func, list(take(num, prev_keys))))
                   for num, key in zip(groups, keys))
        prev_width = width
        prev_keys = iter(keys)
        level += 1
    return rv
