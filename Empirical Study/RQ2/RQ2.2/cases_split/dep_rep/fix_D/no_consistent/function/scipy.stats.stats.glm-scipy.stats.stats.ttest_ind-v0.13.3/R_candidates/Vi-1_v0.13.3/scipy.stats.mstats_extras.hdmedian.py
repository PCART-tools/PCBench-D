def hdmedian(data, axis=-1, var=False):
    """
    Returns the Harrell-Davis estimate of the median along the given axis.

    Parameters
    ----------
    data : ndarray
        Data array.
    axis : int
        Axis along which to compute the quantiles. If None, use a flattened
        array.
    var : boolean
        Whether to return the variance of the estimate.

    """
    result = hdquantiles(data,[0.5], axis=axis, var=var)
    return result.squeeze()
