def get_dtype_kinds(l):
    """
    Parameters
    ----------
    l : list of arrays

    Returns
    -------
    a set of kinds that exist in this list of arrays
    """

    typs = set()
    for arr in l:

        dtype = arr.dtype
        if is_categorical_dtype(dtype):
            typ = 'category'
        elif isinstance(arr, ABCSparseArray):
            typ = 'sparse'
        elif is_datetime64_dtype(dtype):
            typ = 'datetime'
        elif is_timedelta64_dtype(dtype):
            typ = 'timedelta'
        elif is_object_dtype(dtype):
            typ = 'object'
        elif is_bool_dtype(dtype):
            typ = 'bool'
        else:
            typ = dtype.kind
        typs.add(typ)
    return typs
