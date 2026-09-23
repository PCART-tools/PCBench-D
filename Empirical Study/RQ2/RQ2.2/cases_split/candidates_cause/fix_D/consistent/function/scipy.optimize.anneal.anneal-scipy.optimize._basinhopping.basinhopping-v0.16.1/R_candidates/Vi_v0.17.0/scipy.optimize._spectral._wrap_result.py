def _wrap_result(result, is_complex, shape=None):
    """
    Convert from real to complex and reshape result arrays.
    """
    if is_complex:
        z = _real2complex(result)
    else:
        z = result
    if shape is not None:
        z = z.reshape(shape)
    return z
