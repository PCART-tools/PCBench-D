def invalidate_string_dtypes(dtype_set: Set[DtypeObj]):
    """
    Change string like dtypes to object for
    ``DataFrame.select_dtypes()``.
    """
    non_string_dtypes = dtype_set - {np.dtype("S").type, np.dtype("<U").type}
    if non_string_dtypes != dtype_set:
        raise TypeError("string dtypes are not allowed, use 'object' instead")
