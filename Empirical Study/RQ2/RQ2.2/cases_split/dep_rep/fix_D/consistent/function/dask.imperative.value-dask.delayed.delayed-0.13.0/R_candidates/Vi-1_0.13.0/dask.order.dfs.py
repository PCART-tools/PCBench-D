def dfs(dependencies, dependents, key=lambda x: x):
    """ Depth First Search of dask graph

    This traverses from root/output nodes down to leaf/input nodes in a depth
    first manner.  At each node it traverses down its immediate children by the
    order determined by maximizing the key function.

    As inputs it takes dependencies and dependents as can be computed from
    ``get_deps(dsk)``.

    Examples
    --------

    >>> dsk = {'a': 1, 'b': 2, 'c': (inc, 'a'), 'd': (add, 'b', 'c')}
    >>> dependencies, dependents = get_deps(dsk)

    >>> sorted(dfs(dependencies, dependents).items())
    [('a', 3), ('b', 1), ('c', 2), ('d', 0)]
    """
    result = dict()
    i = 0

    roots = [k for k, v in dependents.items() if not v]
    stack = sorted(roots, key=key, reverse=True)
    seen = set()

    while stack:
        item = stack.pop()
        if item in seen:
            continue
        seen.add(item)

        result[item] = i
        deps = dependencies[item]
        if deps:
            deps = deps - seen
            deps = sorted(deps, key=key, reverse=True)
            stack.extend(deps)
        i += 1

    return result
