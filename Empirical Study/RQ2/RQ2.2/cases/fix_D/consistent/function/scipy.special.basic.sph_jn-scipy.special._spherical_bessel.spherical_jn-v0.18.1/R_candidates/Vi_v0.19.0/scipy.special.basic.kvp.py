def kvp(v, z, n=1):
    """Compute nth derivative of real-order modified Bessel function Kv(z)

    Kv(z) is the modified Bessel function of the second kind.
    Derivative is calculated with respect to `z`.

    Parameters
    ----------
    v : array_like of float
        Order of Bessel function
    z : array_like of complex
        Argument at which to evaluate the derivative
    n : int
        Order of derivative.  Default is first derivative.

    Returns
    -------
    out : ndarray
        The results

    Examples
    --------
    Calculate multiple values at order 5:

    >>> from scipy.special import kvp
    >>> kvp(5, (1, 2, 3+5j))
    array([-1849.0354+0.j    ,   -25.7735+0.j    ,    -0.0307+0.0875j])

    Calculate for a single value at multiple orders:

    >>> kvp((4, 4.5, 5), 1)
    array([ -184.0309,  -568.9585, -1849.0354])

    Notes
    -----
    The derivative is computed using the relation DLFM 10.29.5 [2]_.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 6.
           http://jin.ece.illinois.edu/specfunc.html
    .. [2] NIST Digital Library of Mathematical Functions.
           http://dlmf.nist.gov/10.29.E5

    """
    if not isinstance(n, int) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if n == 0:
        return kv(v, z)
    else:
        return (-1)**n * _bessel_diff_formula(v, z, n, kv, 1)
