def _invalidate_string_dtypes(dtype_set):
    """Change string like dtypes to object for ``DataFrame.select_dtypes()``."""
    non_string_dtypes = dtype_set - _string_dtypes
    if non_string_dtypes != dtype_set:
        raise TypeError("string dtypes are not allowed, use 'object' instead")
