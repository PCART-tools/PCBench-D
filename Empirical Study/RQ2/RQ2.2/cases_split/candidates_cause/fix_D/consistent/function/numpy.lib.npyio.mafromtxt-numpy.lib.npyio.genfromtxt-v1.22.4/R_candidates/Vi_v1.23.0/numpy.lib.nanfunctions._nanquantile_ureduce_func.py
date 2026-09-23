def _nanquantile_ureduce_func(a, q, axis=None, out=None, overwrite_input=False,
                              method="linear"):
    """
    Private function that doesn't support extended axis or keepdims.
    These methods are extended to this function using _ureduce
    See nanpercentile for parameter usage
    """
    if axis is None or a.ndim == 1:
        part = a.ravel()
        result = _nanquantile_1d(part, q, overwrite_input, method)
    else:
        result = np.apply_along_axis(_nanquantile_1d, axis, a, q,
                                     overwrite_input, method)
        # apply_along_axis fills in collapsed axis with results.
        # Move that axis to the beginning to match percentile's
        # convention.
        if q.ndim != 0:
            result = np.moveaxis(result, axis, 0)

    if out is not None:
        out[...] = result
    return result
