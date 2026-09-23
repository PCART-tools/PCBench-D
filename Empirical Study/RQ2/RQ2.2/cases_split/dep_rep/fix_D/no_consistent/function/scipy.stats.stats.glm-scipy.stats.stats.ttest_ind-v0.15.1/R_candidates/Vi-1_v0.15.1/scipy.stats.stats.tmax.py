def tmax(a, upperlimit=None, axis=0, inclusive=True):
    """
    Compute the trimmed maximum

    This function computes the maximum value of an array along a given axis,
    while ignoring values larger than a specified upper limit.

    Parameters
    ----------
    a : array_like
        array of values
    upperlimit : None or float, optional
        Values in the input array greater than the given limit will be ignored.
        When upperlimit is None, then all values are used. The default value
        is None.
    axis : None or int, optional
        Operate along this axis.  None means to use the flattened array and
        the default is zero.
    inclusive : {True, False}, optional
        This flag determines whether values exactly equal to the upper limit
        are included.  The default value is True.

    Returns
    -------
    tmax : float

    """
    a, axis = _chk_asarray(a, axis)
    am = mask_to_limits(a, (None, upperlimit), (False, inclusive))
    return ma.maximum.reduce(am, axis)
