def tsem(a, limits=None, inclusive=(True, True)):
    """
    Compute the trimmed standard error of the mean

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

    """
    a = np.asarray(a).ravel()
    if limits is None:
        n = float(len(a))
        return a.std()/np.sqrt(n)
    am = mask_to_limits(a.ravel(), limits, inclusive)
    sd = np.sqrt(masked_var(am))
    return sd / am.count()
