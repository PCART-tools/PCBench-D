def factorialk(n, k, exact=True):
    """Multifactorial of n of order k, n(!!...!).

    This is the multifactorial of n skipping k values.  For example,

      factorialk(17, 4) = 17!!!! = 17 * 13 * 9 * 5 * 1

    In particular, for any integer ``n``, we have

      factorialk(n, 1) = factorial(n)

      factorialk(n, 2) = factorial2(n)

    Parameters
    ----------
    n : int
        Calculate multifactorial. If `n` < 0, the return value is 0.
    k : int
        Order of multifactorial.
    exact : bool, optional
        If exact is set to True, calculate the answer exactly using
        integer arithmetic.

    Returns
    -------
    val : int
        Multifactorial of `n`.

    Raises
    ------
    NotImplementedError
        Raises when exact is False

    Examples
    --------
    >>> from scipy.special import factorialk
    >>> factorialk(5, 1, exact=True)
    120L
    >>> factorialk(5, 3, exact=True)
    10L

    """
    if exact:
        if n < 1-k:
            return 0
        if n <= 0:
            return 1
        val = 1
        for j in xrange(n, 0, -k):
            val = val*j
        return val
    else:
        raise NotImplementedError
