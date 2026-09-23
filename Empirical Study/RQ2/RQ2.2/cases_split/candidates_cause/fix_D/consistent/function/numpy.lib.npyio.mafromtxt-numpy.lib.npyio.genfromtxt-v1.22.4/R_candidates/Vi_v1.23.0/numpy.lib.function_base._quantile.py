def _quantile(
        arr: np.array,
        quantiles: np.array,
        axis: int = -1,
        method="linear",
        out=None,
):
    """
    Private function that doesn't support extended axis or keepdims.
    These methods are extended to this function using _ureduce
    See nanpercentile for parameter usage
    It computes the quantiles of the array for the given axis.
    A linear interpolation is performed based on the `interpolation`.

    By default, the method is "linear" where alpha == beta == 1 which
    performs the 7th method of Hyndman&Fan.
    With "median_unbiased" we get alpha == beta == 1/3
    thus the 8th method of Hyndman&Fan.
    """
    # --- Setup
    arr = np.asanyarray(arr)
    values_count = arr.shape[axis]
    # The dimensions of `q` are prepended to the output shape, so we need the
    # axis being sampled from `arr` to be last.
    DATA_AXIS = 0
    if axis != DATA_AXIS:  # But moveaxis is slow, so only call it if axis!=0.
        arr = np.moveaxis(arr, axis, destination=DATA_AXIS)
    # --- Computation of indexes
    # Index where to find the value in the sorted array.
    # Virtual because it is a floating point value, not an valid index.
    # The nearest neighbours are used for interpolation
    try:
        method = _QuantileMethods[method]
    except KeyError:
        raise ValueError(
            f"{method!r} is not a valid method. Use one of: "
            f"{_QuantileMethods.keys()}") from None
    virtual_indexes = method["get_virtual_index"](values_count, quantiles)
    virtual_indexes = np.asanyarray(virtual_indexes)
    if np.issubdtype(virtual_indexes.dtype, np.integer):
        # No interpolation needed, take the points along axis
        if np.issubdtype(arr.dtype, np.inexact):
            # may contain nan, which would sort to the end
            arr.partition(concatenate((virtual_indexes.ravel(), [-1])), axis=0)
            slices_having_nans = np.isnan(arr[-1])
        else:
            # cannot contain nan
            arr.partition(virtual_indexes.ravel(), axis=0)
            slices_having_nans = np.array(False, dtype=bool)
        result = take(arr, virtual_indexes, axis=0, out=out)
    else:
        previous_indexes, next_indexes = _get_indexes(arr,
                                                      virtual_indexes,
                                                      values_count)
        # --- Sorting
        arr.partition(
            np.unique(np.concatenate(([0, -1],
                                      previous_indexes.ravel(),
                                      next_indexes.ravel(),
                                      ))),
            axis=DATA_AXIS)
        if np.issubdtype(arr.dtype, np.inexact):
            slices_having_nans = np.isnan(
                take(arr, indices=-1, axis=DATA_AXIS)
            )
        else:
            slices_having_nans = None
        # --- Get values from indexes
        previous = np.take(arr, previous_indexes, axis=DATA_AXIS)
        next = np.take(arr, next_indexes, axis=DATA_AXIS)
        # --- Linear interpolation
        gamma = _get_gamma(virtual_indexes, previous_indexes, method)
        result_shape = virtual_indexes.shape + (1,) * (arr.ndim - 1)
        gamma = gamma.reshape(result_shape)
        result = _lerp(previous,
                       next,
                       gamma,
                       out=out)
    if np.any(slices_having_nans):
        if result.ndim == 0 and out is None:
            # can't write to a scalar
            result = arr.dtype.type(np.nan)
        else:
            result[..., slices_having_nans] = np.nan
    return result
