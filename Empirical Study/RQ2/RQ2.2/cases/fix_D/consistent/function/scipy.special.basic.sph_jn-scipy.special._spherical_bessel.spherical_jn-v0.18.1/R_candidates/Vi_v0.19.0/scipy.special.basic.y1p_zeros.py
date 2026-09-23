def y1p_zeros(nt, complex=False):
    """Compute nt zeros of Bessel derivative Y1'(z), and value at each zero.

    The values are given by Y1(z1) at each z1 where Y1'(z1)=0.

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
    z1pn : ndarray
        Location of nth zero of Y1'(z)
    y1z1pn : ndarray
        Value of derivative Y1(z1) for nth zero

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996, chapter 5.
           http://jin.ece.illinois.edu/specfunc.html

    """
    if not isscalar(nt) or (floor(nt) != nt) or (nt <= 0):
        raise ValueError("Arguments must be scalar positive integer.")
    kf = 2
    kc = not complex
    return specfun.cyzo(nt, kf, kc)
