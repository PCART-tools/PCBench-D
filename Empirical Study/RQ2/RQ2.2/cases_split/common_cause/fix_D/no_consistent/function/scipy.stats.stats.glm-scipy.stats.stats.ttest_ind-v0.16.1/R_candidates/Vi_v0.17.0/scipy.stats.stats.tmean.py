def tmean(a, limits=None, inclusive=(True, True), axis=None):
    """
    Compute the trimmed mean.

    This function finds the arithmetic mean of given values, ignoring values
    outside the given `limits`.

    Parameters
    ----------
    a : array_like
        Array of values.
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored.  When limits is None (default), then all
        values are used.  Either of the limit values in the tuple can also be
        None representing a half-open interval.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).
    axis : int or None, optional
        Axis along which to compute test. Default is None.

    Returns
    -------
    tmean : float

    See also
    --------
    trim_mean : returns mean after trimming a proportion from both tails.

    Examples
    --------
    >>> from scipy import stats
    >>> x = np.arange(20)
    >>> stats.tmean(x)
    9.5
    >>> stats.tmean(x, (3,17))
    10.0

    """
    a = asarray(a)
    if limits is None:
        return np.mean(a, None)

    am = _mask_to_limits(a.ravel(), limits, inclusive)
    return am.mean(axis=axis)
