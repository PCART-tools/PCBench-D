def tvar(a, limits=None, inclusive=(True, True)):
    """
    Compute the trimmed variance

    This function computes the sample variance of an array of values,
    while ignoring values which are outside of given `limits`.

    Parameters
    ----------
    a : array_like
        Array of values.
    limits : None or (lower limit, upper limit), optional
        Values in the input array less than the lower limit or greater than the
        upper limit will be ignored. When limits is None, then all values are
        used. Either of the limit values in the tuple can also be None
        representing a half-open interval.  The default value is None.
    inclusive : (bool, bool), optional
        A tuple consisting of the (lower flag, upper flag).  These flags
        determine whether values exactly equal to the lower or upper limits
        are included.  The default value is (True, True).

    Returns
    -------
    tvar : float
        Trimmed variance.

    Notes
    -----
    `tvar` computes the unbiased sample variance, i.e. it uses a correction
    factor ``n / (n - 1)``.

    """
    a = asarray(a)
    a = a.astype(float).ravel()
    if limits is None:
        n = len(a)
        return a.var()*(n/(n-1.))
    am = mask_to_limits(a, limits, inclusive)
    return masked_var(am)
