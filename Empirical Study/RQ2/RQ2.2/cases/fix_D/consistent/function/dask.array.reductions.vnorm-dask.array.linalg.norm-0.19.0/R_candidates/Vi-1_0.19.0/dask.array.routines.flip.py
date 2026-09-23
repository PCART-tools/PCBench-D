def flip(m, axis):
    """
    Reverse element order along axis.

    Parameters
    ----------
    axis : int
        Axis to reverse element order of.

    Returns
    -------
    reversed array : ndarray
    """

    m = asanyarray(m)

    sl = m.ndim * [slice(None)]
    try:
        sl[axis] = slice(None, None, -1)
    except IndexError:
        raise ValueError(
            "`axis` of %s invalid for %s-D array" % (str(axis), str(m.ndim))
        )
    sl = tuple(sl)

    return m[sl]
