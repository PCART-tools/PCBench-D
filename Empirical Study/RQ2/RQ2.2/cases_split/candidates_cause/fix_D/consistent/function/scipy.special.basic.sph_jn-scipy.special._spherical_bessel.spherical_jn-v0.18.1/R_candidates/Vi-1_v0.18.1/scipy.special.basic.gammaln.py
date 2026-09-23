def gammaln(x):
    """
    Logarithm of the absolute value of the Gamma function for real inputs.

    Parameters
    ----------
    x : array-like
        Values on the real line at which to compute ``gammaln``

    Returns
    -------
    gammaln : ndarray
        Values of ``gammaln`` at x.

    See Also
    --------
    gammasgn : sign of the gamma function
    loggamma : principal branch of the logarithm of the gamma function

    Notes
    -----
    When used in conjunction with `gammasgn`, this function is useful
    for working in logspace on the real axis without having to deal with
    complex numbers, via the relation ``exp(gammaln(x)) = gammasgn(x)*gamma(x)``.

    Note that `gammaln` currently accepts complex-valued inputs, but it is not
    the same function as for real-valued inputs, and the branch is not
    well-defined --- using `gammaln` with complex is deprecated and will be
    disallowed in future Scipy versions.

    For complex-valued log-gamma, use `loggamma` instead of `gammaln`.

    """
    if np.iscomplexobj(x):
        warnings.warn(("Use of gammaln for complex arguments is "
                       "deprecated as of scipy 0.18.0. Use "
                       "scipy.special.loggamma instead."),
                      DeprecationWarning)
    return _gammaln(x)
