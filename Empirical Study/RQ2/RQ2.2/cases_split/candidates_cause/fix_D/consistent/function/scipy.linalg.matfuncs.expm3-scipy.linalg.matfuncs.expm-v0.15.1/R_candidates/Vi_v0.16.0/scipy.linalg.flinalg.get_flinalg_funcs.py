def get_flinalg_funcs(names,arrays=(),debug=0):
    """Return optimal available _flinalg function objects with
    names. arrays are used to determine optimal prefix."""
    ordering = []
    for i in range(len(arrays)):
        t = arrays[i].dtype.char
        if t not in _type_conv:
            t = 'd'
        ordering.append((t,i))
    if ordering:
        ordering.sort()
        required_prefix = _type_conv[ordering[0][0]]
    else:
        required_prefix = 'd'
    # Some routines may require special treatment.
    # Handle them here before the default lookup.

    # Default lookup:
    if ordering and has_column_major_storage(arrays[ordering[0][1]]):
        suffix1,suffix2 = '_c','_r'
    else:
        suffix1,suffix2 = '_r','_c'

    funcs = []
    for name in names:
        func_name = required_prefix + name
        func = getattr(_flinalg,func_name+suffix1,
                       getattr(_flinalg,func_name+suffix2,None))
        funcs.append(func)
    return tuple(funcs)
