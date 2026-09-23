def optimize(dsk, keys, **kwargs):
    """ Optimize dask for array computation

    1.  Cull tasks not necessary to evaluate keys
    2.  Remove full slicing, e.g. x[:]
    3.  Inline fast functions like getitem and np.transpose
    """
    keys = list(flatten(keys))
    fast_functions = kwargs.get('fast_functions',
                                set([getarray, np.transpose]))
    dsk2, dependencies = cull(dsk, keys)
    dsk4, dependencies = fuse(dsk2, keys, dependencies)
    dsk5 = optimize_slices(dsk4)
    dsk6 = inline_functions(dsk5, keys, fast_functions=fast_functions,
                            dependencies=dependencies)
    return dsk6
