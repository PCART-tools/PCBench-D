def tstd(a, limits=None, inclusive=(True, True)):
    """
    Compute the trimmed sample standard deviation

    This function finds the sample standard deviation of given values,
    ignoring values outside the given `limits`.

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
    tstd : float

    """
    return np.sqrt(tvar(a, limits, inclusive))
