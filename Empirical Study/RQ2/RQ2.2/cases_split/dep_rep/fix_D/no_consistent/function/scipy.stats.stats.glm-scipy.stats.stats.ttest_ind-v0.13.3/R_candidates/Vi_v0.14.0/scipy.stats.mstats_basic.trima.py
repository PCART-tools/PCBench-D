def trima(a, limits=None, inclusive=(True,True)):
    """Trims an array by masking the data outside some given limits.
    Returns a masked version of the input array.

    Parameters
    ----------
    a : sequence
        Input array.
    limits : {None, tuple}, optional
        Tuple of (lower limit, upper limit) in absolute values.
        Values of the input array lower (greater) than the lower (upper) limit
        will be masked. A limit is None indicates an open interval.
    inclusive : {(True,True) tuple}, optional
        Tuple of (lower flag, upper flag), indicating whether values exactly
        equal to the lower (upper) limit are allowed.

    """
    a = ma.asarray(a)
    a.unshare_mask()
    if limits is None:
        return a
    (lower_lim, upper_lim) = limits
    (lower_in, upper_in) = inclusive
    condition = False
    if lower_lim is not None:
        if lower_in:
            condition |= (a < lower_lim)
        else:
            condition |= (a <= lower_lim)
    if upper_lim is not None:
        if upper_in:
            condition |= (a > upper_lim)
        else:
            condition |= (a >= upper_lim)
    a[condition.filled(True)] = masked
    return a
