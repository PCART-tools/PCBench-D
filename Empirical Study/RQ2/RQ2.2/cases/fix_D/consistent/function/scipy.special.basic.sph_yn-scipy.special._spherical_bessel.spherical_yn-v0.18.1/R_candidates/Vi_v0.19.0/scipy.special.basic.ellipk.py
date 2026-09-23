def ellipk(m):
    """Complete elliptic integral of the first kind.

    This function is defined as

    .. math:: K(m) = \\int_0^{\\pi/2} [1 - m \\sin(t)^2]^{-1/2} dt

    Parameters
    ----------
    m : array_like
        The parameter of the elliptic integral.

    Returns
    -------
    K : array_like
        Value of the elliptic integral.

    Notes
    -----
    For more precision around point m = 1, use `ellipkm1`, which this
    function calls.

    See Also
    --------
    ellipkm1 : Complete elliptic integral of the first kind around m = 1
    ellipkinc : Incomplete elliptic integral of the first kind
    ellipe : Complete elliptic integral of the second kind
    ellipeinc : Incomplete elliptic integral of the second kind


    """
    return ellipkm1(1 - asarray(m))
