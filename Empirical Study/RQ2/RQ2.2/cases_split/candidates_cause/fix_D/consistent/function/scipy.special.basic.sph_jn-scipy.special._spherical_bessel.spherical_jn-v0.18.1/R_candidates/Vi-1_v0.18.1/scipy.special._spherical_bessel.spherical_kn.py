def spherical_kn(n, z, derivative=False):
    r"""Modified spherical Bessel function of the second kind or its derivative.

    Defined as [1]_,

    .. math:: k_n(z) = \sqrt{\frac{\pi}{2z}} K_{n + 1/2}(z),

    where :math:`K_n` is the modified Bessel function of the second kind.

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
    kn : ndarray

    Notes
    -----
    The function is computed using its definitional relation to the
    modified cylindrical Bessel function of the second kind.

    The derivative is computed using the relations [2]_,

    .. math::
        k_n' = -k_{n-1} - \frac{n + 1}{2} k_n.

        k_0' = -k_1


    .. versionadded:: 0.18.0

    References
    ----------
    .. [1] http://dlmf.nist.gov/10.47.E9
    .. [2] http://dlmf.nist.gov/10.51.E5
    """
    if derivative:
        return _spherical_kn_d(n, z)
    else:
        return _spherical_kn(n, z)
