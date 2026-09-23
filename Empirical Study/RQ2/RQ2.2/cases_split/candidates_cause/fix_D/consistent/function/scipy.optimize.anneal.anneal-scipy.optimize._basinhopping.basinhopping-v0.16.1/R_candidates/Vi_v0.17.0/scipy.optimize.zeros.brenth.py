def brenth(f, a, b, args=(),
           xtol=_xtol, rtol=_rtol, maxiter=_iter,
           full_output=False, disp=True):
    """Find root of f in [a,b].

    A variation on the classic Brent routine to find a zero of the function f
    between the arguments a and b that uses hyperbolic extrapolation instead of
    inverse quadratic extrapolation. There was a paper back in the 1980's ...
    f(a) and f(b) cannot have the same signs. Generally on a par with the
    brent routine, but not as heavily tested.  It is a safe version of the
    secant method that uses hyperbolic extrapolation. The version here is by
    Chuck Harris.

    Parameters
    ----------
    f : function
        Python function returning a number.  f must be continuous, and f(a) and
        f(b) must have opposite signs.
    a : number
        One end of the bracketing interval [a,b].
    b : number
        The other end of the bracketing interval [a,b].
    xtol : number, optional
        The routine converges when a root is known to lie within xtol of the
        value return. Should be >= 0.  The routine modifies this to take into
        account the relative precision of doubles.
    rtol : number, optional
        The routine converges when a root is known to lie within `rtol` times
        the value returned of the value returned. Should be >= 0. Defaults to
        ``np.finfo(float).eps * 2``.
    maxiter : number, optional
        if convergence is not achieved in maxiter iterations, an error is
        raised.  Must be >= 0.
    args : tuple, optional
        containing extra arguments for the function `f`.
        `f` is called by ``apply(f, (x)+args)``.
    full_output : bool, optional
        If `full_output` is False, the root is returned.  If `full_output` is
        True, the return value is ``(x, r)``, where `x` is the root, and `r` is
        a RootResults object.
    disp : bool, optional
        If True, raise RuntimeError if the algorithm didn't converge.

    Returns
    -------
    x0 : float
        Zero of `f` between `a` and `b`.
    r : RootResults (present if ``full_output = True``)
        Object containing information about the convergence.  In particular,
        ``r.converged`` is True if the routine converged.

    See Also
    --------
    fmin, fmin_powell, fmin_cg,
           fmin_bfgs, fmin_ncg : multivariate local optimizers

    leastsq : nonlinear least squares minimizer

    fmin_l_bfgs_b, fmin_tnc, fmin_cobyla : constrained multivariate optimizers

    basinhopping, differential_evolution, brute : global optimizers

    fminbound, brent, golden, bracket : local scalar minimizers

    fsolve : n-dimensional root-finding

    brentq, brenth, ridder, bisect, newton : one-dimensional root-finding

    fixed_point : scalar fixed-point finder

    """
    if not isinstance(args, tuple):
        args = (args,)
    if xtol <= 0:
        raise ValueError("xtol too small (%g <= 0)" % xtol)
    if rtol < _rtol:
        raise ValueError("rtol too small (%g < %g)" % (rtol, _rtol))
    r = _zeros._brenth(f,a, b, xtol, rtol, maxiter, args, full_output, disp)
    return results_c(full_output, r)
