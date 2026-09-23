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
            typ = "category"
        elif is_sparse(dtype):
            typ = "sparse"
        elif isinstance(arr, ABCRangeIndex):
            typ = "range"
        elif is_datetime64tz_dtype(dtype):
            # if to_concat contains different tz,
            # the result must be object dtype
            typ = str(dtype)
        elif is_datetime64_dtype(dtype):
            typ = "datetime"
        elif is_timedelta64_dtype(dtype):
            typ = "timedelta"
        elif is_object_dtype(dtype):
            typ = "object"
        elif is_bool_dtype(dtype):
            typ = "bool"
        elif is_extension_array_dtype(dtype):
            typ = str(dtype)
        else:
            typ = dtype.kind
        typs.add(typ)
    return typs
