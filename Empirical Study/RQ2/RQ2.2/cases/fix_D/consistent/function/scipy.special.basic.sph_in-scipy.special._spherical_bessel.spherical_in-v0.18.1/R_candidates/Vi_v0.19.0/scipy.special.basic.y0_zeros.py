def y0_zeros(nt, complex=False):
    """Compute nt zeros of Bessel function Y0(z), and derivative at each zero.

    The derivatives are given by Y0'(z0) = -Y1(z0) at each zero z0.

    Parameters
    ----------
    nt : int
        Number of zeros to return
    complex : bool, default False
        Set to False to return only the real zeros; set to True to return only
        the complex zeros with negative real part and positive imaginary part.
        Note that the complex conjugates of the latter are also zeros of the
        function, but are not returned by this routine.

    Returns
    -------
    z0n : ndarray
        Location of nth zero of Y0(z)
    y0pz0n : ndarray
        Value of derivative Y0'(z0) for nth zero

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("Arguments must be scalar positive integer.")
    kf = 0
    kc = not complex
    return specfun.cyzo(nt, kf, kc)
