def _get_dtype_kinds(arrays) -> Set[str]:
    """
    Parameters
    ----------
    arrays : list of arrays

    Returns
    -------
    set[str]
        A set of kinds that exist in this list of arrays.
    """
    typs: Set[str] = set()
    for arr in arrays:
        # Note: we use dtype.kind checks because they are much more performant
        #  than is_foo_dtype

        dtype = arr.dtype
        if not isinstance(dtype, np.dtype):
            # ExtensionDtype so we get
            #  e.g. "categorical", "datetime64[ns, US/Central]", "Sparse[itn64, 0]"
            typ = str(dtype)
        elif isinstance(arr, ABCRangeIndex):
            typ = "range"
        elif dtype.kind == "M":
            typ = "datetime"
        elif dtype.kind == "m":
            typ = "timedelta"
        elif dtype.kind in ["O", "b"]:
            typ = str(dtype)  # i.e. "object", "bool"
        else:
            typ = dtype.kind

        typs.add(typ)
    return typs
