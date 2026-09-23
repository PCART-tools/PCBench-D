def ndependents(dependencies, dependents):
    """ Number of total data elements that depend on key

    For each key we return the number of data that can only be run after this
    key is run.  The root nodes have value 1 while deep child nodes will have
    larger values.

    Examples
    --------

    >>> dsk = {'a': 1, 'b': (inc, 'a'), 'c': (inc, 'b')}
    >>> dependencies, dependents = get_deps(dsk)

    >>> sorted(ndependents(dependencies, dependents).items())
    [('a', 3), ('b', 2), ('c', 1)]
    """
    result = dict()
    num_needed = dict((k, len(v)) for k, v in dependents.items())
    current = set(k for k, v in num_needed.items() if v == 0)
    while current:
        key = current.pop()
        result[key] = 1 + sum(result[parent] for parent in dependents[key])
        for child in dependencies[key]:
            num_needed[child] -= 1
            if num_needed[child] == 0:
                current.add(child)
    return result
