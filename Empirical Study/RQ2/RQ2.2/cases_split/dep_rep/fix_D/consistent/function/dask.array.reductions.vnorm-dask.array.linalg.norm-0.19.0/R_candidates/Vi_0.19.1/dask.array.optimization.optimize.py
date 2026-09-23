def optimize(dsk, keys, fuse_keys=None, fast_functions=None,
             inline_functions_fast_functions=(getter_inline,), rename_fused_keys=True,
             **kwargs):
    """ Optimize dask for array computation

    1.  Cull tasks not necessary to evaluate keys
    2.  Remove full slicing, e.g. x[:]
    3.  Inline fast functions like getitem and np.transpose
    """
    dsk = ensure_dict(dsk)
    keys = list(flatten(keys))
    if fast_functions is not None:
        inline_functions_fast_functions = fast_functions

    dsk2, dependencies = cull(dsk, keys)
    hold = hold_keys(dsk2, dependencies)

    dsk3, dependencies = fuse(dsk2, hold + keys + (fuse_keys or []),
                              dependencies, rename_keys=rename_fused_keys)
    if inline_functions_fast_functions:
        dsk4 = inline_functions(dsk3, keys, dependencies=dependencies,
                                fast_functions=inline_functions_fast_functions)
    else:
        dsk4 = dsk3
    dsk5 = optimize_slices(dsk4)

    return dsk5
