def kstat(data, n=2):
    """
    Return the nth k-statistic (1<=n<=4 so far).

    The nth k-statistic is the unique symmetric unbiased estimator of the nth
    cumulant kappa_n.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2, 3, 4}, optional
        Default is equal to 2.

    Returns
    -------
    kstat : float
        The nth k-statistic.

    See Also
    --------
    kstatvar: Returns an unbiased estimator of the variance of the k-statistic.

    Notes
    -----
    The cumulants are related to central moments but are specifically defined
    using a power series expansion of the logarithm of the characteristic
    function (which is the Fourier transform of the PDF).
    In particular let phi(t) be the characteristic function, then::

        ln phi(t) = > kappa_n (it)^n / n!    (sum from n=0 to inf)

    The first few cumulants (kappa_n)  in terms of central moments (mu_n) are::

        kappa_1 = mu_1
        kappa_2 = mu_2
        kappa_3 = mu_3
        kappa_4 = mu_4 - 3*mu_2**2
        kappa_5 = mu_5 - 10*mu_2 * mu_3

    References
    ----------
    http://mathworld.wolfram.com/k-Statistic.html

    http://mathworld.wolfram.com/Cumulant.html

    """
    if n > 4 or n < 1:
        raise ValueError("k-statistics only supported for 1<=n<=4")
    n = int(n)
    S = zeros(n + 1, 'd')
    data = ravel(data)
    N = len(data)
    for k in range(1, n + 1):
        S[k] = sum(data**k, axis=0)
    if n == 1:
        return S[1] * 1.0/N
    elif n == 2:
        return (N*S[2] - S[1]**2.0) / (N*(N - 1.0))
    elif n == 3:
        return (2*S[1]**3 - 3*N*S[1]*S[2] + N*N*S[3]) / (N*(N - 1.0)*(N - 2.0))
    elif n == 4:
        return ((-6*S[1]**4 + 12*N*S[1]**2 * S[2] - 3*N*(N-1.0)*S[2]**2 -
                 4*N*(N+1)*S[1]*S[3] + N*N*(N+1)*S[4]) /
                 (N*(N-1.0)*(N-2.0)*(N-3.0)))
    else:
        raise ValueError("Should not be here.")
