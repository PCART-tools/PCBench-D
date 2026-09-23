def spherical_yn(n, z, derivative=False):
    r"""Spherical Bessel function of the second kind or its derivative.

    Defined as [1]_,

    .. math:: y_n(z) = \sqrt{\frac{\pi}{2z}} Y_{n + 1/2}(z),

    where :math:`Y_n` is the Bessel function of the second kind.

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
    yn : ndarray

    Notes
    -----
    For real arguments, the function is computed using the ascending
    recurrence [2]_.  For complex arguments, the definitional relation to
    the cylindrical Bessel function of the second kind is used.

    The derivative is computed using the relations [3]_,

    .. math::
        y_n' = y_{n-1} - \frac{n + 1}{2} y_n.

        y_0' = -y_1


    .. versionadded:: 0.18.0

    References
    ----------
    .. [1] http://dlmf.nist.gov/10.47.E4
    .. [2] http://dlmf.nist.gov/10.51.E1
    .. [3] http://dlmf.nist.gov/10.51.E2
    """
    if derivative:
        return _spherical_yn_d(n, z)
    else:
        return _spherical_yn(n, z)
