def tsem(a, limits=None, inclusive=(True, True)):
    """
    Compute the trimmed standard error of the mean.

    This function finds the standard error of the mean for given
    values, ignoring values outside the given `limits`.

    Parameters
    ----------
    a : array_like
        array of values
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
    tsem : float

    Notes
    -----
    `tsem` uses unbiased sample standard deviation, i.e. it uses a
    correction factor ``n / (n - 1)``.

    """
    a = np.asarray(a).ravel()
    if limits is None:
        return a.std(ddof=1) / np.sqrt(a.size)

    am = mask_to_limits(a, limits, inclusive)
    sd = np.sqrt(masked_var(am))
    return sd / np.sqrt(am.count())
