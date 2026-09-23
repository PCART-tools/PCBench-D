def collections_to_dsk(collections, optimize_graph=True, **kwargs):
    """
    Convert many collections into a single dask graph, after optimization
    """
    optimizations = (kwargs.pop('optimizations', None) or
                     _globals.get('optimizations', []))
    if optimize_graph:
        groups = groupby(lambda x: x._optimize, collections)
        groups = {opt: _extract_graph_and_keys(val)
                  for opt, val in groups.items()}
        for opt in optimizations:
            groups = {k: [opt(dict(dsk), keys), keys]
                      for k, (dsk, keys) in groups.items()}
        dsk = merge([opt(dsk, keys, **kwargs)
                     for opt, (dsk, keys) in groups.items()])
    else:
        dsk = merge(dict(c.dask) for c in collections)

    return dsk
