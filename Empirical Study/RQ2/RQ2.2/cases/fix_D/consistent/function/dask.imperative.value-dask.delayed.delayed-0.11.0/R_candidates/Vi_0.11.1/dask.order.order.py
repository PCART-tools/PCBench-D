def order(dsk, dependencies=None):
    """ Order nodes in dask graph

    The ordering will be a toposort but will also have other convenient
    properties

    1.  Depth first search
    2.  DFS prefers nodes that enable the most data

    >>> dsk = {'a': 1, 'b': 2, 'c': (inc, 'a'), 'd': (add, 'b', 'c')}
    >>> order(dsk)
    {'a': 2, 'c': 1, 'b': 3, 'd': 0}
    """
    if dependencies is None:
        dependencies = dict((k, get_dependencies(dsk, k)) for k in dsk)
    dependents = reverse_dict(dependencies)

    ndeps = ndependents(dependencies, dependents)
    maxes = child_max(dependencies, dependents, ndeps)

    def key(x):
        return -maxes.get(x, 0), str(x)

    return dfs(dependencies, dependents, key=key)
