def clpmn(m, n, z, type=3):
    """Associated Legendre function of the first kind, Pmn(z).

    Computes the associated Legendre function of the first kind of order m and
    degree n, ``Pmn(z)`` = :math:`P_n^m(z)`, and its derivative, ``Pmn'(z)``.
    Returns two arrays of size ``(m+1, n+1)`` containing ``Pmn(z)`` and
    ``Pmn'(z)`` for all orders from ``0..m`` and degrees from ``0..n``.

    Parameters
    ----------
    m : int
       ``|m| <= n``; the order of the Legendre function.
    n : int
       where ``n >= 0``; the degree of the Legendre function.  Often
       called ``l`` (lower case L) in descriptions of the associated
       Legendre function
    z : float or complex
        Input value.
    type : int, optional
       takes values 2 or 3
       2: cut on the real axis ``|x| > 1``
       3: cut on the real axis ``-1 < x < 1`` (default)

    Returns
    -------
    Pmn_z : (m+1, n+1) array
       Values for all orders ``0..m`` and degrees ``0..n``
    Pmn_d_z : (m+1, n+1) array
       Derivatives for all orders ``0..m`` and degrees ``0..n``

    See Also
    --------
    lpmn: associated Legendre functions of the first kind for real z

    Notes
    -----
    By default, i.e. for ``type=3``, phase conventions are chosen according
    to [1]_ such that the function is analytic. The cut lies on the interval
    (-1, 1). Approaching the cut from above or below in general yields a phase
    factor with respect to Ferrer's function of the first kind
    (cf. `lpmn`).

    For ``type=2`` a cut at ``|x| > 1`` is chosen. Approaching the real values
    on the interval (-1, 1) in the complex plane yields Ferrer's function
    of the first kind.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           http://jin.ece.illinois.edu/specfunc.html
    .. [2] NIST Digital Library of Mathematical Functions
           http://dlmf.nist.gov/14.21

    """
    if not isscalar(m) or (abs(m) > n):
        raise ValueError("m must be <= n.")
    if not isscalar(n) or (n < 0):
        raise ValueError("n must be a non-negative integer.")
    if not isscalar(z):
        raise ValueError("z must be scalar.")
    if not(type == 2 or type == 3):
        raise ValueError("type must be either 2 or 3.")
    if (m < 0):
        mp = -m
        mf, nf = mgrid[0:mp+1, 0:n+1]
        sv = errprint(0)
        if type == 2:
            fixarr = where(mf > nf, 0.0,
                           (-1)**mf * gamma(nf-mf+1) / gamma(nf+mf+1))
        else:
            fixarr = where(mf > nf, 0.0, gamma(nf-mf+1) / gamma(nf+mf+1))
        sv = errprint(sv)
    else:
        mp = m
    p, pd = specfun.clpmn(mp, n, real(z), imag(z), type)
    if (m < 0):
        p = p * fixarr
        pd = pd * fixarr
    return p, pd
