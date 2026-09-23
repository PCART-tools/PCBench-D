def get_deps(dsk):
    """ Get dependencies and dependents from dask dask graph

    >>> dsk = {'a': 1, 'b': (inc, 'a'), 'c': (inc, 'b')}
    >>> dependencies, dependents = get_deps(dsk)
    >>> dependencies
    {'a': set([]), 'c': set(['b']), 'b': set(['a'])}
    >>> dependents
    {'a': set(['b']), 'c': set([]), 'b': set(['c'])}
    """
    dependencies = {k: get_dependencies(dsk, task=v)
                    for k, v in dsk.items()}
    dependents = reverse_dict(dependencies)
    return dependencies, dependents
