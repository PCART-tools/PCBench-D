def _maybe_convert_scalar(values):
    """
    Convert a python scalar to the appropriate numpy dtype if possible
    This avoids numpy directly converting according to platform preferences
    """
    if lib.isscalar(values):
        dtype, values = _infer_dtype_from_scalar(values)
        try:
            values = dtype(values)
        except TypeError:
            pass
    return values
