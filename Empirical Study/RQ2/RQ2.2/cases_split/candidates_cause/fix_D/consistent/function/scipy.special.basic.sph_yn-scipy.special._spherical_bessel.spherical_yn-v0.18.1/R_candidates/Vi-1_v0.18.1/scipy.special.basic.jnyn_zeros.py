def jnyn_zeros(n, nt):
    """Compute nt zeros of Bessel functions Jn(x), Jn'(x), Yn(x), and Yn'(x).

    Returns 4 arrays of length `nt`, corresponding to the first `nt` zeros of
    Jn(x), Jn'(x), Yn(x), and Yn'(x), respectively.

    Parameters
    ----------
    n : int
        Order of the Bessel functions
    nt : int
        Number (<=1200) of zeros to compute

    See jn_zeros, jnp_zeros, yn_zeros, ynp_zeros to get separate arrays.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if not (isscalar(nt) and isscalar(n)):
        raise ValueError("Arguments must be scalars.")
    if (floor(n) != n) or (floor(nt) != nt):
        raise ValueError("Arguments must be integers.")
    if (nt <= 0):
        raise ValueError("nt > 0")
    return specfun.jyzo(abs(n), nt)
