def spherical_jn(n, z, derivative=False):
    r"""Spherical Bessel function of the first kind or its derivative.

    Defined as [1]_,

    .. math:: j_n(z) = \sqrt{\frac{\pi}{2z}} J_{n + 1/2}(z),

    where :math:`J_n` is the Bessel function of the first kind.

    Parameters
    ----------
    n : int, array_like
        Order of the Bessel function (n >= 0).
    z : complex or float, array_like
        Argument of the Bessel function.
    derivative : bool, optional
        If True, the value of the derivative (rather than the function
        itself) is returned.

    Returns
    -------
    jn : ndarray

    Notes
    -----
    For real arguments greater than the order, the function is computed
    using the ascending recurrence [2]_.  For small real or complex
    arguments, the definitional relation to the cylindrical Bessel function
    of the first kind is used.

    The derivative is computed using the relations [3]_,

    .. math::
        j_n' = j_{n-1} - \frac{n + 1}{2} j_n.

        j_0' = -j_1


    .. versionadded:: 0.18.0

    References
    ----------
    .. [1] http://dlmf.nist.gov/10.47.E3
    .. [2] http://dlmf.nist.gov/10.51.E1
    .. [3] http://dlmf.nist.gov/10.51.E2
    """
    if derivative:
        return _spherical_jn_d(n, z)
    else:
        return _spherical_jn(n, z)
