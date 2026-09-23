def polygamma(n, x):
    """Polygamma function n.

    This is the nth derivative of the digamma (psi) function.

    Parameters
    ----------
    n : array_like of int
        The order of the derivative of `psi`.
    x : array_like
        Where to evaluate the polygamma function.

    Returns
    -------
    polygamma : ndarray
        The result.

    Examples
    --------
    >>> from scipy import special
    >>> x = [2, 3, 25.5]
    >>> special.polygamma(1, x)
    array([ 0.64493407,  0.39493407,  0.03999467])
    >>> special.polygamma(0, x) == special.psi(x)
    array([ True,  True,  True], dtype=bool)

    """
    n, x = asarray(n), asarray(x)
    fac2 = (-1.0)**(n+1) * gamma(n+1.0) * zeta(n+1, x)
    return where(n == 0, psi(x), fac2)
