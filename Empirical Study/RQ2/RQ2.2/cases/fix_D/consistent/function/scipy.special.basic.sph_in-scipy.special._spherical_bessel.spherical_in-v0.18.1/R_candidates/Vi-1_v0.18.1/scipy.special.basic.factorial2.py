def factorial2(n, exact=False):
    """Double factorial.

    This is the factorial with every second value skipped.  E.g., ``7!! = 7 * 5
    * 3 * 1``.  It can be approximated numerically as::

      n!! = special.gamma(n/2+1)*2**((m+1)/2)/sqrt(pi)  n odd
          = 2**(n/2) * (n/2)!                           n even

    Parameters
    ----------
    n : int or array_like
        Calculate ``n!!``.  Arrays are only supported with `exact` set
        to False.  If ``n < 0``, the return value is 0.
    exact : bool, optional
        The result can be approximated rapidly using the gamma-formula
        above (default).  If `exact` is set to True, calculate the
        answer exactly using integer arithmetic.

    Returns
    -------
    nff : float or int
        Double factorial of `n`, as an int or a float depending on
        `exact`.

    Examples
    --------
    >>> from scipy.special import factorial2
    >>> factorial2(7, exact=False)
    array(105.00000000000001)
    >>> factorial2(7, exact=True)
    105L

    """
    if exact:
        if n < -1:
            return 0
        if n <= 0:
            return 1
        val = 1
        for k in xrange(n, 0, -2):
            val *= k
        return val
    else:
        n = asarray(n)
        vals = zeros(n.shape, 'd')
        cond1 = (n % 2) & (n >= -1)
        cond2 = (1-(n % 2)) & (n >= -1)
        oddn = extract(cond1, n)
        evenn = extract(cond2, n)
        nd2o = oddn / 2.0
        nd2e = evenn / 2.0
        place(vals, cond1, gamma(nd2o + 1) / sqrt(pi) * pow(2.0, nd2o + 0.5))
        place(vals, cond2, gamma(nd2e + 1) * pow(2.0, nd2e))
        return vals
