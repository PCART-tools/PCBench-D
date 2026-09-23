def toposort(dsk, dependencies=None):
    """ Return a list of keys of dask sorted in topological order."""
    return _toposort(dsk, dependencies=dependencies)
