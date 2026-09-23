def tmean(a, limits=None, inclusive=(True, True)):
    """
    Compute the trimmed mean

    This function finds the arithmetic mean of given values, ignoring values
    outside the given `limits`.

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
    tmean : float

    """
    a = asarray(a)

    # Cast to a float if this is an integer array. If it is already a float
    # array, leave it as is to preserve its precision.
    if issubclass(a.dtype.type, np.integer):
        a = a.astype(float)

    # No trimming.
    if limits is None:
        return np.mean(a,None)

    am = mask_to_limits(a.ravel(), limits, inclusive)
    return am.mean()
