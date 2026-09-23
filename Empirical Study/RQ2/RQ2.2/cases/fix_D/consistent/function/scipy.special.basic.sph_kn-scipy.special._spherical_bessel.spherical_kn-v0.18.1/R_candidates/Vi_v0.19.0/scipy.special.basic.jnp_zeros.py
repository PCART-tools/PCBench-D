def jnp_zeros(n, nt):
    """Compute zeros of integer-order Bessel function derivative Jn'(x).

    Parameters
    ----------
    n : int
        Order of Bessel function
    nt : int
        Number of zeros to return

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           http://jin.ece.illinois.edu/specfunc.html

    """
    return jnyn_zeros(n, nt)[1]
