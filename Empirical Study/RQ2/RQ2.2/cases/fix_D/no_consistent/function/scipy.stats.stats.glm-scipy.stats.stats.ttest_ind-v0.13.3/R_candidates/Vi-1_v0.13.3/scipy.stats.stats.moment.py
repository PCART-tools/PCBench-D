def moment(a, moment=1, axis=0):
    """
    Calculates the nth moment about the mean for a sample.

    Generally used to calculate coefficients of skewness and
    kurtosis.

    Parameters
    ----------
    a : array_like
       data
    moment : int
       order of central moment that is returned
    axis : int or None
       Axis along which the central moment is computed. If None, then the data
       array is raveled. The default axis is zero.

    Returns
    -------
    n-th central moment : ndarray or float
       The appropriate moment along the given axis or over all values if axis
       is None. The denominator for the moment calculation is the number of
       observations, no degrees of freedom correction is done.

    """
    a, axis = _chk_asarray(a, axis)
    if moment == 1:
        # By definition the first moment about the mean is 0.
        shape = list(a.shape)
        del shape[axis]
        if shape:
            # return an actual array of the appropriate shape
            return np.zeros(shape, dtype=float)
        else:
            # the input was 1D, so return a scalar instead of a rank-0 array
            return np.float64(0.0)
    else:
        mn = np.expand_dims(np.mean(a,axis), axis)
        s = np.power((a-mn), moment)
        return np.mean(s, axis)
