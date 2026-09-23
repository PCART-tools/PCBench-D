def optimize(dsk, keys, fuse_keys=None, fast_functions=None,
             inline_functions_fast_functions=None, **kwargs):
    """ Optimize dask for array computation

    1.  Cull tasks not necessary to evaluate keys
    2.  Remove full slicing, e.g. x[:]
    3.  Inline fast functions like getitem and np.transpose
    """
    keys = list(flatten(keys))
    if fast_functions is not None:
        inline_functions_fast_functions = fast_functions

    if inline_functions_fast_functions is None:
        inline_functions_fast_functions = {getarray, getarray_nofancy,
                                           np.transpose}

    dsk2, dependencies = cull(dsk, keys)
    dsk4, dependencies = fuse(dsk2, keys + (fuse_keys or []), dependencies)
    dsk5 = optimize_slices(dsk4)
    dsk6 = inline_functions(dsk5, keys, dependencies=dependencies,
                            fast_functions=inline_functions_fast_functions)

    return dsk6
