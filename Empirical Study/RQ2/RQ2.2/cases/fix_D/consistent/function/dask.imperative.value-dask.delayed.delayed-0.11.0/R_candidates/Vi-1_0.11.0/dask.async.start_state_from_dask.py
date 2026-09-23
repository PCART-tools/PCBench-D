def start_state_from_dask(dsk, cache=None, sortkey=None):
    """ Start state from a dask

    Examples
    --------

    >>> dsk = {'x': 1, 'y': 2, 'z': (inc, 'x'), 'w': (add, 'z', 'y')}
    >>> from pprint import pprint
    >>> pprint(start_state_from_dask(dsk)) # doctest: +NORMALIZE_WHITESPACE
    {'cache': {'x': 1, 'y': 2},
     'dependencies': {'w': set(['y', 'z']),
                      'x': set([]),
                      'y': set([]),
                      'z': set(['x'])},
     'dependents': {'w': set([]),
                    'x': set(['z']),
                    'y': set(['w']),
                    'z': set(['w'])},
     'finished': set([]),
     'ready': ['z'],
     'released': set([]),
     'running': set([]),
     'waiting': {'w': set(['z'])},
     'waiting_data': {'x': set(['z']),
                      'y': set(['w']),
                      'z': set(['w'])}}
    """
    if sortkey is None:
        sortkey = order(dsk).get
    if cache is None:
        cache = _globals['cache']
    if cache is None:
        cache = dict()
    data_keys = set()
    for k, v in dsk.items():
        if not has_tasks(dsk, v):
            cache[k] = v
            data_keys.add(k)

    dsk2 = dsk.copy()
    dsk2.update(cache)

    dependencies = dict((k, get_dependencies(dsk2, k)) for k in dsk)
    waiting = dict((k, v.copy()) for k, v in dependencies.items()
                                 if k not in data_keys)

    dependents = reverse_dict(dependencies)
    for a in cache:
        for b in dependents.get(a, ()):
            waiting[b].remove(a)
    waiting_data = dict((k, v.copy()) for k, v in dependents.items() if v)

    ready_set = set([k for k, v in waiting.items() if not v])
    ready = sorted(ready_set, key=sortkey, reverse=True)
    waiting = dict((k, v) for k, v in waiting.items() if v)

    state = {'dependencies': dependencies,
             'dependents': dependents,
             'waiting': waiting,
             'waiting_data': waiting_data,
             'cache': cache,
             'ready': ready,
             'running': set(),
             'finished': set(),
             'released': set()}

    return state
