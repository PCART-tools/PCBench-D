def _median_nancheck(data, result, axis):
    """
    Utility function to check median result from data for NaN values at the end
    and return NaN in that case. Input result can also be a MaskedArray.

    Parameters
    ----------
    data : array
        Sorted input data to median function
    result : Array or MaskedArray
        Result of median function.
    axis : int
        Axis along which the median was computed.

    Returns
    -------
    result : scalar or ndarray
        Median or NaN in axes which contained NaN in the input.  If the input
        was an array, NaN will be inserted in-place.  If a scalar, either the
        input itself or a scalar NaN.
    """
    if data.size == 0:
        return result
    n = np.isnan(data.take(-1, axis=axis))
    # masked NaN values are ok
    if np.ma.isMaskedArray(n):
        n = n.filled(False)
    if np.count_nonzero(n.ravel()) > 0:
        # Without given output, it is possible that the current result is a
        # numpy scalar, which is not writeable.  If so, just return nan.
        if isinstance(result, np.generic):
            return data.dtype.type(np.nan)

        result[n] = np.nan
    return result
